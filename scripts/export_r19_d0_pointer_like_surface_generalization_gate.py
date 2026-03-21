"""Export the bounded admitted-plus-heldout runtime gate for R19."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import re
from statistics import median
import time
from typing import Any, Callable, Iterable

from bytecode import (
    checkpoint_replay_long_program,
    helper_checkpoint_braid_long_program,
    helper_checkpoint_braid_program,
    indirect_counter_bank_program,
    iterated_helper_accumulator_program,
    stack_memory_braid_program,
    subroutine_braid_long_program,
    subroutine_braid_program,
)
from exec_trace import Program, TraceInterpreter
from model import compare_execution_to_reference
from model.exact_hardmax import extract_memory_operations
from model.free_running_executor import FreeRunningTraceExecutor
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
R17_OUT_DIR = ROOT / "results" / "R17_d0_full_surface_runtime_bridge"
OUT_DIR = ROOT / "results" / "R19_d0_pointer_like_surface_generalization_gate"
PROFILE_REPEATS = 1
PARTIAL_RUNTIME_ROWS_PATH = OUT_DIR / "runtime_rows.partial.json"
PARTIAL_ADDRESS_PROFILES_PATH = OUT_DIR / "address_profiles.partial.json"


@dataclass(frozen=True, slots=True)
class ManifestRecord:
    source_lane: str
    family: str
    baseline_stage: str
    baseline_program_name: str
    baseline_horizon_multiplier: int
    baseline_start: int
    retrieval_horizon_multiplier: int
    scaled_start: int
    comparison_mode: str
    max_steps: int
    boundary_family: bool
    cohort: str
    variant_id: str
    variant_group: str
    envelope_rule: str
    program_name: str
    address_signature: str


@dataclass(frozen=True, slots=True)
class StrategyImplementation:
    strategy_id: str
    prefix: str
    stack_strategy: str
    memory_strategy: str


@dataclass(frozen=True, slots=True)
class StrategyProfileResult:
    strategy_id: str
    prefix: str
    runtime_mode: str
    stack_strategy: str
    memory_strategy: str
    median_seconds: float
    samples: tuple[float, ...]
    ns_per_step: float | None
    exact_trace_match: bool
    exact_final_state_match: bool
    first_mismatch_step: int | None
    failure_reason: str | None
    read_observation_count: int
    memory_read_count: int
    stack_read_count: int


LINEAR_EXACT = StrategyImplementation("linear_exact", "linear", "linear", "linear")
ACCELERATED_EXACT = StrategyImplementation("accelerated", "accelerated", "accelerated", "accelerated")
POINTER_LIKE_EXACT = StrategyImplementation(
    "pointer_like_exact",
    "pointer_like",
    "pointer_like_exact",
    "pointer_like_exact",
)
STRATEGIES: tuple[StrategyImplementation, ...] = (
    LINEAR_EXACT,
    ACCELERATED_EXACT,
    POINTER_LIKE_EXACT,
)


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def median_or_none(values: Iterable[float | None]) -> float | None:
    filtered = [value for value in values if value is not None]
    return median(filtered) if filtered else None


def safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in {None, 0.0}:
        return None
    return numerator / denominator


def profile_callable(fn):
    samples: list[float] = []
    result = None
    error: Exception | None = None
    for _ in range(PROFILE_REPEATS):
        start = time.perf_counter()
        try:
            result = fn()
        except Exception as exc:  # pragma: no cover - exercised in real exporter runs
            error = exc
            result = None
        samples.append(time.perf_counter() - start)
        if error is not None:
            break
    return median(samples), samples, result, error


def load_r17_runtime_baselines() -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    with (R17_OUT_DIR / "runtime_bridge_rows.csv").open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows[str(row["program_name"])] = {
                "lowered_ns_per_step": float(row["lowered_ns_per_step"]),
                "linear_ns_per_step": float(row["linear_ns_per_step"]),
                "accelerated_ns_per_step": float(row["accelerated_ns_per_step"]),
            }
    if len(rows) != 8:
        raise RuntimeError(f"R19 expected 8 runtime baseline rows from R17, found {len(rows)}.")
    return rows


def load_admitted_surface_records() -> tuple[ManifestRecord, ...]:
    payload = read_json(R17_OUT_DIR / "runtime_surface_index.json")
    rows: list[ManifestRecord] = []
    for row in payload["rows"]:
        program_name = str(row["program_name"])
        rows.append(
            ManifestRecord(
                source_lane=str(row["source_lane"]),
                family=str(row["family"]),
                baseline_stage=str(row["baseline_stage"]),
                baseline_program_name=str(row["baseline_program_name"]),
                baseline_horizon_multiplier=int(row["baseline_horizon_multiplier"]),
                baseline_start=int(row["baseline_start"]),
                retrieval_horizon_multiplier=int(row["retrieval_horizon_multiplier"]),
                scaled_start=int(row["scaled_start"]),
                comparison_mode=str(row["comparison_mode"]),
                max_steps=int(row["max_steps"]),
                boundary_family=bool(row["boundary_bearing_stream"]),
                cohort="admitted",
                variant_id="r17_admitted_surface",
                variant_group="admitted_surface",
                envelope_rule="r17_admitted_runtime_surface",
                program_name=program_name,
                address_signature=_address_signature_from_case(program_name),
            )
        )
    if len(rows) != 8:
        raise RuntimeError(f"R19 expected 8 admitted surface rows, found {len(rows)}.")
    return tuple(sorted(rows, key=lambda item: (item.family, item.program_name)))


def _address_signature_from_case(program_name: str) -> str:
    if "_a" not in program_name:
        return "no_address_suffix"
    suffix = program_name.split("_a", maxsplit=1)[1]
    return f"a{suffix}"


def _heldout_record(
    source: ManifestRecord,
    *,
    variant_id: str,
    variant_group: str,
    envelope_rule: str,
    program_name: str,
    address_signature: str,
) -> ManifestRecord:
    return ManifestRecord(
        source_lane=source.source_lane,
        family=source.family,
        baseline_stage=source.baseline_stage,
        baseline_program_name=source.baseline_program_name,
        baseline_horizon_multiplier=source.baseline_horizon_multiplier,
        baseline_start=source.baseline_start,
        retrieval_horizon_multiplier=source.retrieval_horizon_multiplier,
        scaled_start=source.scaled_start,
        comparison_mode=source.comparison_mode,
        max_steps=source.max_steps,
        boundary_family=source.boundary_family,
        cohort="heldout",
        variant_id=variant_id,
        variant_group=variant_group,
        envelope_rule=envelope_rule,
        program_name=program_name,
        address_signature=address_signature,
    )


def _helper_long_variants(record: ManifestRecord) -> list[ManifestRecord]:
    start = record.scaled_start
    return [
        _heldout_record(
            record,
            variant_id="selector_seed_flip",
            variant_group="seed_equivalent",
            envelope_rule="same_endpoint_seed_flip",
            program_name=helper_checkpoint_braid_long_program(start, base_address=312, selector_seed=1).name,
            address_signature="a312_s1",
        ),
        _heldout_record(
            record,
            variant_id="address_shift_plus_16",
            variant_group="address_equivalent",
            envelope_rule="same_endpoint_address_translation",
            program_name=helper_checkpoint_braid_long_program(start, base_address=328, selector_seed=0).name,
            address_signature="a328_s0",
        ),
    ]


def _helper_variants(record: ManifestRecord) -> list[ManifestRecord]:
    start = record.scaled_start
    return [
        _heldout_record(
            record,
            variant_id="selector_seed_flip",
            variant_group="seed_equivalent",
            envelope_rule="same_endpoint_seed_flip",
            program_name=helper_checkpoint_braid_program(start, base_address=280, selector_seed=1).name,
            address_signature="a280_s1",
        ),
        _heldout_record(
            record,
            variant_id="address_shift_plus_16",
            variant_group="address_equivalent",
            envelope_rule="same_endpoint_address_translation",
            program_name=helper_checkpoint_braid_program(start, base_address=296, selector_seed=0).name,
            address_signature="a296_s0",
        ),
    ]


def _two_address_shift_variants(
    record: ManifestRecord,
    *,
    small_program: Callable[[], str],
    large_program: Callable[[], str],
    small_signature: str,
    large_signature: str,
) -> list[ManifestRecord]:
    return [
        _heldout_record(
            record,
            variant_id="address_shift_plus_16",
            variant_group="address_equivalent",
            envelope_rule="same_endpoint_address_translation",
            program_name=small_program(),
            address_signature=small_signature,
        ),
        _heldout_record(
            record,
            variant_id="address_shift_plus_32",
            variant_group="address_equivalent",
            envelope_rule="same_endpoint_address_translation",
            program_name=large_program(),
            address_signature=large_signature,
        ),
    ]


def build_heldout_surface_records(admitted_rows: tuple[ManifestRecord, ...]) -> tuple[ManifestRecord, ...]:
    heldout_rows: list[ManifestRecord] = []
    for record in admitted_rows:
        start = record.scaled_start
        if record.family == "helper_checkpoint_braid_long":
            heldout_rows.extend(_helper_long_variants(record))
        elif record.family == "helper_checkpoint_braid":
            heldout_rows.extend(_helper_variants(record))
        elif record.family == "checkpoint_replay_long":
            heldout_rows.extend(
                _two_address_shift_variants(
                    record,
                    small_program=lambda: checkpoint_replay_long_program(start, base_address=144).name,
                    large_program=lambda: checkpoint_replay_long_program(start, base_address=160).name,
                    small_signature="a144",
                    large_signature="a160",
                )
            )
        elif record.family == "iterated_helper_accumulator":
            heldout_rows.extend(
                _two_address_shift_variants(
                    record,
                    small_program=lambda: iterated_helper_accumulator_program(
                        start,
                        counter_address=160,
                        accumulator_address=161,
                    ).name,
                    large_program=lambda: iterated_helper_accumulator_program(
                        start,
                        counter_address=176,
                        accumulator_address=177,
                    ).name,
                    small_signature="a160_b161",
                    large_signature="a176_b177",
                )
            )
        elif record.family == "subroutine_braid_long":
            heldout_rows.extend(
                _two_address_shift_variants(
                    record,
                    small_program=lambda: subroutine_braid_long_program(start, base_address=192).name,
                    large_program=lambda: subroutine_braid_long_program(start, base_address=208).name,
                    small_signature="a192",
                    large_signature="a208",
                )
            )
        elif record.family == "indirect_counter_bank":
            heldout_rows.extend(
                _two_address_shift_variants(
                    record,
                    small_program=lambda: indirect_counter_bank_program(
                        start,
                        counter_address=48,
                        accumulator_address=49,
                    ).name,
                    large_program=lambda: indirect_counter_bank_program(
                        start,
                        counter_address=64,
                        accumulator_address=65,
                    ).name,
                    small_signature="a48_b49",
                    large_signature="a64_b65",
                )
            )
        elif record.family == "subroutine_braid":
            heldout_rows.extend(
                _two_address_shift_variants(
                    record,
                    small_program=lambda: subroutine_braid_program(start, base_address=112).name,
                    large_program=lambda: subroutine_braid_program(start, base_address=128).name,
                    small_signature="a112",
                    large_signature="a128",
                )
            )
        elif record.family == "stack_memory_braid":
            heldout_rows.extend(
                _two_address_shift_variants(
                    record,
                    small_program=lambda: stack_memory_braid_program(start, base_address=128).name,
                    large_program=lambda: stack_memory_braid_program(start, base_address=144).name,
                    small_signature="a128",
                    large_signature="a144",
                )
            )
        else:
            raise ValueError(f"Unsupported R19 family: {record.family}")
    if len(heldout_rows) != len(admitted_rows) * 2:
        raise RuntimeError(
            f"R19 expected two heldout rows per admitted family, found {len(heldout_rows)} rows for {len(admitted_rows)} families."
        )
    admitted_program_names = {row.program_name for row in admitted_rows}
    if admitted_program_names & {row.program_name for row in heldout_rows}:
        raise RuntimeError("R19 heldout rows must not reuse admitted program names.")
    return tuple(sorted(heldout_rows, key=lambda item: (item.family, item.variant_id, item.program_name)))


def build_family_summary(rows: tuple[ManifestRecord, ...]) -> list[dict[str, object]]:
    grouped: dict[str, list[ManifestRecord]] = defaultdict(list)
    for row in rows:
        grouped[row.family].append(row)

    summary_rows: list[dict[str, object]] = []
    for family, family_rows in sorted(grouped.items()):
        admitted_count = sum(row.cohort == "admitted" for row in family_rows)
        heldout_count = sum(row.cohort == "heldout" for row in family_rows)
        summary_rows.append(
            {
                "family": family,
                "admitted_count": admitted_count,
                "heldout_count": heldout_count,
                "variant_ids": sorted({row.variant_id for row in family_rows if row.cohort == "heldout"}),
                "variant_groups": sorted({row.variant_group for row in family_rows if row.cohort == "heldout"}),
                "boundary_family": any(row.boundary_family for row in family_rows),
            }
        )
    return summary_rows


def materialize_program(program_name: str) -> Program:
    helper_long_match = re.fullmatch(r"bytecode_helper_checkpoint_braid_long_(\d+)_a(\d+)_s(\d+)", program_name)
    if helper_long_match:
        start, base_address, selector_seed = (int(group) for group in helper_long_match.groups())
        return helper_checkpoint_braid_long_program(start, base_address=base_address, selector_seed=selector_seed)

    helper_match = re.fullmatch(r"bytecode_helper_checkpoint_braid_(\d+)_a(\d+)_s(\d+)", program_name)
    if helper_match:
        start, base_address, selector_seed = (int(group) for group in helper_match.groups())
        return helper_checkpoint_braid_program(start, base_address=base_address, selector_seed=selector_seed)

    checkpoint_match = re.fullmatch(r"bytecode_checkpoint_replay_long_(\d+)_a(\d+)", program_name)
    if checkpoint_match:
        start, base_address = (int(group) for group in checkpoint_match.groups())
        return checkpoint_replay_long_program(start, base_address=base_address)

    iterated_match = re.fullmatch(r"bytecode_iterated_helper_accumulator_(\d+)_a(\d+)_b(\d+)", program_name)
    if iterated_match:
        start, counter_address, accumulator_address = (int(group) for group in iterated_match.groups())
        return iterated_helper_accumulator_program(
            start,
            counter_address=counter_address,
            accumulator_address=accumulator_address,
        )

    indirect_match = re.fullmatch(r"bytecode_indirect_counter_bank_(\d+)_a(\d+)_b(\d+)", program_name)
    if indirect_match:
        start, counter_address, accumulator_address = (int(group) for group in indirect_match.groups())
        return indirect_counter_bank_program(
            start,
            counter_address=counter_address,
            accumulator_address=accumulator_address,
        )

    subroutine_long_match = re.fullmatch(r"bytecode_subroutine_braid_long_(\d+)_a(\d+)", program_name)
    if subroutine_long_match:
        start, base_address = (int(group) for group in subroutine_long_match.groups())
        return subroutine_braid_long_program(start, base_address=base_address)

    subroutine_match = re.fullmatch(r"bytecode_subroutine_braid_(\d+)_a(\d+)", program_name)
    if subroutine_match:
        start, base_address = (int(group) for group in subroutine_match.groups())
        return subroutine_braid_program(start, base_address=base_address)

    stack_memory_match = re.fullmatch(r"bytecode_stack_memory_braid_(\d+)_a(\d+)", program_name)
    if stack_memory_match:
        start, base_address = (int(group) for group in stack_memory_match.groups())
        return stack_memory_braid_program(start, base_address=base_address)

    raise ValueError(f"Unsupported R19 program name: {program_name}")


def profile_strategy_runtime(
    lowered_program: Program,
    *,
    max_steps: int,
    reference,
    strategy: StrategyImplementation,
) -> StrategyProfileResult:
    median_seconds, samples, execution, error = profile_callable(
        lambda: FreeRunningTraceExecutor(
            stack_strategy=strategy.stack_strategy,
            memory_strategy=strategy.memory_strategy,
            validate_exact_reads=False,
        ).run(lowered_program, max_steps=max_steps)
    )

    if execution is None:
        return StrategyProfileResult(
            strategy_id=strategy.strategy_id,
            prefix=strategy.prefix,
            runtime_mode="measured",
            stack_strategy=strategy.stack_strategy,
            memory_strategy=strategy.memory_strategy,
            median_seconds=median_seconds,
            samples=tuple(samples),
            ns_per_step=None,
            exact_trace_match=False,
            exact_final_state_match=False,
            first_mismatch_step=None,
            failure_reason=None if error is None else f"{type(error).__name__}: {error}",
            read_observation_count=0,
            memory_read_count=0,
            stack_read_count=0,
        )

    outcome = compare_execution_to_reference(lowered_program, execution, reference=reference)
    program_steps = max(1, int(outcome.program_steps))
    memory_read_count = sum(observation.space == "memory" for observation in execution.read_observations)
    stack_read_count = sum(observation.space == "stack" for observation in execution.read_observations)
    return StrategyProfileResult(
        strategy_id=strategy.strategy_id,
        prefix=strategy.prefix,
        runtime_mode="measured",
        stack_strategy=strategy.stack_strategy,
        memory_strategy=strategy.memory_strategy,
        median_seconds=median_seconds,
        samples=tuple(samples),
        ns_per_step=(median_seconds / program_steps) * 1e9,
        exact_trace_match=outcome.exact_trace_match,
        exact_final_state_match=outcome.exact_final_state_match,
        first_mismatch_step=outcome.first_mismatch_step,
        failure_reason=outcome.failure_reason,
        read_observation_count=len(execution.read_observations),
        memory_read_count=memory_read_count,
        stack_read_count=stack_read_count,
    )


def strategy_profile_is_exact(profile: StrategyProfileResult) -> bool:
    return profile.failure_reason is None and profile.exact_trace_match and profile.exact_final_state_match


def build_address_profile(record: ManifestRecord, reference) -> dict[str, object]:
    operations = extract_memory_operations(reference.events)
    by_address: dict[int, dict[str, int]] = defaultdict(lambda: {"loads": 0, "stores": 0})
    load_count = 0
    store_count = 0
    for operation in operations:
        if operation.kind == "load":
            by_address[operation.address]["loads"] += 1
            load_count += 1
        elif operation.kind == "store":
            by_address[operation.address]["stores"] += 1
            store_count += 1
    address_rows = [
        {
            "address": address,
            "loads": counts["loads"],
            "stores": counts["stores"],
            "total_ops": counts["loads"] + counts["stores"],
        }
        for address, counts in sorted(by_address.items())
    ]
    hottest_address_row = (
        max(
            address_rows,
            key=lambda row: (int(row["total_ops"]), int(row["loads"]), -int(row["address"])),
        )
        if address_rows
        else {"address": None, "loads": 0, "stores": 0, "total_ops": 0}
    )
    return {
        "source_lane": record.source_lane,
        "family": record.family,
        "cohort": record.cohort,
        "variant_id": record.variant_id,
        "variant_group": record.variant_group,
        "program_name": record.program_name,
        "boundary_family": record.boundary_family,
        "reference_step_count": int(reference.final_state.steps),
        "memory_operation_count": len(operations),
        "memory_load_count": load_count,
        "memory_store_count": store_count,
        "unique_address_count": len(address_rows),
        "hottest_address": hottest_address_row["address"],
        "hottest_address_loads": hottest_address_row["loads"],
        "hottest_address_stores": hottest_address_row["stores"],
        "address_rows": address_rows,
    }


def profile_manifest_record(
    record: ManifestRecord,
    r17_runtime_baselines: dict[str, dict[str, float]],
) -> tuple[dict[str, object], dict[str, object]]:
    from bytecode import lower_program

    program = materialize_program(record.program_name)
    lowered_program = lower_program(program)
    reference = TraceInterpreter().run(lowered_program, max_steps=record.max_steps)
    address_profile = build_address_profile(record, reference)
    r17_baseline = r17_runtime_baselines.get(record.program_name)
    strategy_profiles = {
        strategy.prefix: profile_strategy_runtime(
            lowered_program,
            max_steps=record.max_steps,
            reference=reference,
            strategy=strategy,
        )
        for strategy in STRATEGIES
    }
    linear_profile = strategy_profiles["linear"]
    accelerated_profile = strategy_profiles["accelerated"]
    pointer_profile = strategy_profiles["pointer_like"]

    row = {
        "source_lane": record.source_lane,
        "family": record.family,
        "baseline_stage": record.baseline_stage,
        "baseline_program_name": record.baseline_program_name,
        "baseline_horizon_multiplier": record.baseline_horizon_multiplier,
        "baseline_start": record.baseline_start,
        "retrieval_horizon_multiplier": record.retrieval_horizon_multiplier,
        "scaled_start": record.scaled_start,
        "comparison_mode": record.comparison_mode,
        "max_steps": record.max_steps,
        "boundary_family": record.boundary_family,
        "cohort": record.cohort,
        "variant_id": record.variant_id,
        "variant_group": record.variant_group,
        "envelope_rule": record.envelope_rule,
        "program_name": record.program_name,
        "address_signature": record.address_signature,
        "reference_step_count": int(reference.final_state.steps),
        "profile_repeats": PROFILE_REPEATS,
        "memory_operation_count": address_profile["memory_operation_count"],
        "memory_load_count": address_profile["memory_load_count"],
        "memory_store_count": address_profile["memory_store_count"],
        "unique_address_count": address_profile["unique_address_count"],
        "hottest_address": address_profile["hottest_address"],
        "r17_baseline_lowered_ns_per_step": None if r17_baseline is None else r17_baseline["lowered_ns_per_step"],
        "r17_baseline_linear_ns_per_step": None if r17_baseline is None else r17_baseline["linear_ns_per_step"],
        "r17_baseline_accelerated_ns_per_step": None
        if r17_baseline is None
        else r17_baseline["accelerated_ns_per_step"],
    }

    for prefix, profile in strategy_profiles.items():
        row.update(
            {
                f"{prefix}_strategy_id": profile.strategy_id,
                f"{prefix}_runtime_mode": profile.runtime_mode,
                f"{prefix}_stack_strategy": profile.stack_strategy,
                f"{prefix}_memory_strategy": profile.memory_strategy,
                f"{prefix}_median_seconds": profile.median_seconds,
                f"{prefix}_samples": list(profile.samples),
                f"{prefix}_ns_per_step": profile.ns_per_step,
                f"{prefix}_exact_trace_match": profile.exact_trace_match,
                f"{prefix}_exact_final_state_match": profile.exact_final_state_match,
                f"{prefix}_first_mismatch_step": profile.first_mismatch_step,
                f"{prefix}_failure_reason": profile.failure_reason,
                f"{prefix}_read_observation_count": profile.read_observation_count,
                f"{prefix}_memory_read_count": profile.memory_read_count,
                f"{prefix}_stack_read_count": profile.stack_read_count,
                f"{prefix}_exact": strategy_profile_is_exact(profile),
            }
        )

    row.update(
        {
            "accelerated_speedup_vs_linear": safe_ratio(linear_profile.ns_per_step, accelerated_profile.ns_per_step),
            "pointer_like_speedup_vs_linear": safe_ratio(linear_profile.ns_per_step, pointer_profile.ns_per_step),
            "pointer_like_speedup_vs_current_accelerated": safe_ratio(
                accelerated_profile.ns_per_step,
                pointer_profile.ns_per_step,
            ),
            "pointer_like_speedup_vs_r17_accelerated": safe_ratio(
                row["r17_baseline_accelerated_ns_per_step"],
                pointer_profile.ns_per_step,
            ),
            "current_accelerated_ratio_vs_r17_accelerated": safe_ratio(
                accelerated_profile.ns_per_step,
                row["r17_baseline_accelerated_ns_per_step"],
            ),
        }
    )
    return row, address_profile


def execute_runtime_rows(
    manifest_rows: tuple[ManifestRecord, ...],
    r17_runtime_baselines: dict[str, dict[str, float]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    partial_runtime_rows, partial_address_profiles = load_partial_runtime_state()
    ordered_program_names = [record.program_name for record in manifest_rows]

    for index, record in enumerate(manifest_rows, start=1):
        if record.program_name in partial_runtime_rows and record.program_name in partial_address_profiles:
            continue
        runtime_row, address_profile = profile_manifest_record(record, r17_runtime_baselines)
        partial_runtime_rows[record.program_name] = runtime_row
        partial_address_profiles[record.program_name] = address_profile
        write_partial_runtime_state(partial_runtime_rows, partial_address_profiles, ordered_program_names)
        print(f"[R19] completed {index}/{len(manifest_rows)} {record.program_name}", flush=True)

    runtime_rows = [partial_runtime_rows[program_name] for program_name in ordered_program_names]
    address_profiles = [partial_address_profiles[program_name] for program_name in ordered_program_names]
    return runtime_rows, address_profiles


def load_partial_runtime_state() -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    runtime_rows: dict[str, dict[str, object]] = {}
    address_profiles: dict[str, dict[str, object]] = {}
    if PARTIAL_RUNTIME_ROWS_PATH.exists():
        payload = read_json(PARTIAL_RUNTIME_ROWS_PATH)
        runtime_rows = {str(row["program_name"]): row for row in payload.get("rows", [])}
    if PARTIAL_ADDRESS_PROFILES_PATH.exists():
        payload = read_json(PARTIAL_ADDRESS_PROFILES_PATH)
        address_profiles = {str(row["program_name"]): row for row in payload.get("rows", [])}
    return runtime_rows, address_profiles


def write_partial_runtime_state(
    runtime_rows: dict[str, dict[str, object]],
    address_profiles: dict[str, dict[str, object]],
    ordered_program_names: list[str],
) -> None:
    ordered_runtime_rows = [runtime_rows[name] for name in ordered_program_names if name in runtime_rows]
    ordered_address_profiles = [address_profiles[name] for name in ordered_program_names if name in address_profiles]
    write_json(
        PARTIAL_RUNTIME_ROWS_PATH,
        {
            "experiment": "r19_pointer_like_surface_generalization_runtime_rows_partial",
            "rows": ordered_runtime_rows,
        },
    )
    write_json(
        PARTIAL_ADDRESS_PROFILES_PATH,
        {
            "experiment": "r19_pointer_like_surface_generalization_address_profiles_partial",
            "rows": ordered_address_profiles,
        },
    )


def row_strategy_is_exact(row: dict[str, object], prefix: str) -> bool:
    return bool(row[f"{prefix}_exact"])


def build_cohort_runtime_summary(runtime_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in runtime_rows:
        grouped[str(row["cohort"])].append(row)

    summary_rows: list[dict[str, object]] = []
    for cohort, cohort_rows in sorted(grouped.items()):
        summary_rows.append(
            {
                "cohort": cohort,
                "row_count": len(cohort_rows),
                "linear_exact_count": sum(row_strategy_is_exact(row, "linear") for row in cohort_rows),
                "accelerated_exact_count": sum(row_strategy_is_exact(row, "accelerated") for row in cohort_rows),
                "pointer_like_exact_count": sum(row_strategy_is_exact(row, "pointer_like") for row in cohort_rows),
                "median_accelerated_speedup_vs_linear": median_or_none(
                    row["accelerated_speedup_vs_linear"] for row in cohort_rows
                ),
                "median_pointer_like_speedup_vs_linear": median_or_none(
                    row["pointer_like_speedup_vs_linear"] for row in cohort_rows
                ),
                "median_pointer_like_speedup_vs_current_accelerated": median_or_none(
                    row["pointer_like_speedup_vs_current_accelerated"] for row in cohort_rows
                ),
                "median_pointer_like_speedup_vs_r17_accelerated": median_or_none(
                    row["pointer_like_speedup_vs_r17_accelerated"] for row in cohort_rows
                ),
                "pointer_like_failure_program_names": [
                    str(row["program_name"]) for row in cohort_rows if not row_strategy_is_exact(row, "pointer_like")
                ],
            }
        )
    return summary_rows


def build_family_runtime_summary(runtime_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in runtime_rows:
        grouped[str(row["family"])].append(row)

    summary_rows: list[dict[str, object]] = []
    for family, family_rows in sorted(grouped.items()):
        admitted_rows = [row for row in family_rows if row["cohort"] == "admitted"]
        heldout_rows = [row for row in family_rows if row["cohort"] == "heldout"]
        summary_rows.append(
            {
                "family": family,
                "boundary_family": any(bool(row["boundary_family"]) for row in family_rows),
                "admitted_row_count": len(admitted_rows),
                "heldout_row_count": len(heldout_rows),
                "admitted_pointer_like_exact_count": sum(
                    row_strategy_is_exact(row, "pointer_like") for row in admitted_rows
                ),
                "heldout_pointer_like_exact_count": sum(
                    row_strategy_is_exact(row, "pointer_like") for row in heldout_rows
                ),
                "heldout_failure_program_names": [
                    str(row["program_name"]) for row in heldout_rows if not row_strategy_is_exact(row, "pointer_like")
                ],
                "median_heldout_pointer_like_speedup_vs_current_accelerated": median_or_none(
                    row["pointer_like_speedup_vs_current_accelerated"] for row in heldout_rows
                ),
            }
        )
    return summary_rows


def build_pointer_like_failures(runtime_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    failure_rows: list[dict[str, object]] = []
    for row in runtime_rows:
        if row_strategy_is_exact(row, "pointer_like"):
            continue
        failure_rows.append(
            {
                "cohort": row["cohort"],
                "family": row["family"],
                "variant_id": row["variant_id"],
                "program_name": row["program_name"],
                "pointer_like_first_mismatch_step": row["pointer_like_first_mismatch_step"],
                "pointer_like_failure_reason": row["pointer_like_failure_reason"],
            }
        )
    return failure_rows


def assess_runtime_gate(
    runtime_rows: list[dict[str, object]],
    cohort_runtime_rows: list[dict[str, object]],
) -> dict[str, object]:
    admitted_rows = [row for row in runtime_rows if row["cohort"] == "admitted"]
    heldout_rows = [row for row in runtime_rows if row["cohort"] == "heldout"]

    admitted_linear_exact_count = sum(row_strategy_is_exact(row, "linear") for row in admitted_rows)
    admitted_accelerated_exact_count = sum(row_strategy_is_exact(row, "accelerated") for row in admitted_rows)
    admitted_pointer_like_exact_count = sum(row_strategy_is_exact(row, "pointer_like") for row in admitted_rows)
    heldout_linear_exact_count = sum(row_strategy_is_exact(row, "linear") for row in heldout_rows)
    heldout_accelerated_exact_count = sum(row_strategy_is_exact(row, "accelerated") for row in heldout_rows)
    heldout_pointer_like_exact_count = sum(row_strategy_is_exact(row, "pointer_like") for row in heldout_rows)

    admitted_reference_gate_passed = (
        admitted_linear_exact_count == len(admitted_rows)
        and admitted_accelerated_exact_count == len(admitted_rows)
    )
    heldout_reference_gate_passed = (
        heldout_linear_exact_count == len(heldout_rows)
        and heldout_accelerated_exact_count == len(heldout_rows)
    )
    admitted_regression_gate_passed = (
        admitted_reference_gate_passed and admitted_pointer_like_exact_count == len(admitted_rows)
    )
    heldout_generalization_gate_passed = (
        heldout_reference_gate_passed and heldout_pointer_like_exact_count == len(heldout_rows)
    )

    if admitted_regression_gate_passed and heldout_generalization_gate_passed:
        lane_verdict = "same_endpoint_generalization_confirmed"
        next_priority_lane = "r20_d0_runtime_mechanism_ablation_matrix"
        reason = "Pointer-like execution stayed exact on every admitted and heldout row inside the fixed D0 envelope."
    elif admitted_regression_gate_passed:
        lane_verdict = "same_endpoint_generalization_not_confirmed"
        next_priority_lane = "r20_d0_runtime_mechanism_ablation_matrix"
        reason = "Pointer-like execution preserved the admitted R17 surface but failed on at least one heldout row."
    else:
        lane_verdict = "admitted_surface_regression_detected"
        next_priority_lane = "h19_refreeze_and_next_scope_decision"
        reason = "Pointer-like execution no longer preserves the admitted R17 surface, so the mainline cannot advance."

    admitted_cohort = next(row for row in cohort_runtime_rows if row["cohort"] == "admitted")
    heldout_cohort = next(row for row in cohort_runtime_rows if row["cohort"] == "heldout")

    return {
        "lane_verdict": lane_verdict,
        "reason": reason,
        "admitted_reference_gate_passed": admitted_reference_gate_passed,
        "heldout_reference_gate_passed": heldout_reference_gate_passed,
        "admitted_regression_gate_passed": admitted_regression_gate_passed,
        "heldout_generalization_gate_passed": heldout_generalization_gate_passed,
        "admitted_case_count": len(admitted_rows),
        "heldout_case_count": len(heldout_rows),
        "admitted_linear_exact_count": admitted_linear_exact_count,
        "admitted_accelerated_exact_count": admitted_accelerated_exact_count,
        "admitted_pointer_like_exact_count": admitted_pointer_like_exact_count,
        "heldout_linear_exact_count": heldout_linear_exact_count,
        "heldout_accelerated_exact_count": heldout_accelerated_exact_count,
        "heldout_pointer_like_exact_count": heldout_pointer_like_exact_count,
        "admitted_pointer_like_median_speedup_vs_current_accelerated": admitted_cohort[
            "median_pointer_like_speedup_vs_current_accelerated"
        ],
        "heldout_pointer_like_median_speedup_vs_current_accelerated": heldout_cohort[
            "median_pointer_like_speedup_vs_current_accelerated"
        ],
        "admitted_pointer_like_median_speedup_vs_r17_accelerated": admitted_cohort[
            "median_pointer_like_speedup_vs_r17_accelerated"
        ],
        "pointer_like_failures": build_pointer_like_failures(runtime_rows),
        "next_priority_lane": next_priority_lane,
    }


def build_summary(
    admitted_rows: tuple[ManifestRecord, ...],
    heldout_rows: tuple[ManifestRecord, ...],
    family_manifest_rows: list[dict[str, object]],
    cohort_runtime_rows: list[dict[str, object]],
    family_runtime_rows: list[dict[str, object]],
    gate: dict[str, object],
) -> dict[str, object]:
    supported_here = [
        "R19 stayed inside the fixed D0 endpoint and reused the exact admitted R17 runtime surface plus deterministic same-envelope heldout variants.",
        f"Linear exact remained exact on {gate['admitted_linear_exact_count']}/{len(admitted_rows)} admitted rows and {gate['heldout_linear_exact_count']}/{len(heldout_rows)} heldout rows.",
        f"Accelerated exact remained exact on {gate['admitted_accelerated_exact_count']}/{len(admitted_rows)} admitted rows and {gate['heldout_accelerated_exact_count']}/{len(heldout_rows)} heldout rows.",
        f"Pointer-like exact matched {gate['admitted_pointer_like_exact_count']}/{len(admitted_rows)} admitted rows and {gate['heldout_pointer_like_exact_count']}/{len(heldout_rows)} heldout rows.",
    ]
    unsupported_here = [
        "R19 does not authorize any widened frontend, unseen family, or broader systems claim beyond the fixed same-endpoint envelope.",
        "A positive R19 result would still be a bounded runtime generalization result, not a general replacement claim for softmax, MHA, or arbitrary compiled execution.",
    ]
    if gate["lane_verdict"] != "same_endpoint_generalization_confirmed":
        unsupported_here.append("R19 did not close as a full heldout generalization confirmation packet.")

    return {
        "status": "r19_runtime_gate_complete",
        "current_frozen_stage": "h17_refreeze_and_conditional_frontier_recheck",
        "source_runtime_stage": "r17_d0_full_surface_runtime_bridge",
        "manifest_status": "retained",
        "admitted_case_count": len(admitted_rows),
        "heldout_case_count": len(heldout_rows),
        "family_count": len(family_manifest_rows),
        "heldout_variants_per_family": 2,
        "gate": gate,
        "cohort_runtime_summary": cohort_runtime_rows,
        "family_runtime_summary": family_runtime_rows,
        "next_priority_lane": gate["next_priority_lane"],
        "recommended_next_action": (
            "Advance to R20 to ablate the mechanism boundary under the same fixed envelope."
            if gate["admitted_regression_gate_passed"]
            else "Refreeze the mainline state and inspect the admitted regression before any further runtime widening."
        ),
        "claim_impact": {
            "status": f"r19_{gate['lane_verdict']}",
            "next_lane": gate["next_priority_lane"],
            "supported_here": supported_here,
            "unsupported_here": unsupported_here,
            "distilled_result": {
                "admitted_pointer_like_exact_count": gate["admitted_pointer_like_exact_count"],
                "heldout_pointer_like_exact_count": gate["heldout_pointer_like_exact_count"],
                "admitted_case_count": len(admitted_rows),
                "heldout_case_count": len(heldout_rows),
                "admitted_pointer_like_median_speedup_vs_current_accelerated": gate[
                    "admitted_pointer_like_median_speedup_vs_current_accelerated"
                ],
                "heldout_pointer_like_median_speedup_vs_current_accelerated": gate[
                    "heldout_pointer_like_median_speedup_vs_current_accelerated"
                ],
                "admitted_pointer_like_median_speedup_vs_r17_accelerated": gate[
                    "admitted_pointer_like_median_speedup_vs_r17_accelerated"
                ],
            },
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    admitted_rows = load_admitted_surface_records()
    heldout_rows = build_heldout_surface_records(admitted_rows)
    all_rows = admitted_rows + heldout_rows
    family_manifest_rows = build_family_summary(all_rows)
    r17_runtime_baselines = load_r17_runtime_baselines()
    runtime_rows, address_profiles = execute_runtime_rows(all_rows, r17_runtime_baselines)
    cohort_runtime_rows = build_cohort_runtime_summary(runtime_rows)
    family_runtime_rows = build_family_runtime_summary(runtime_rows)
    gate = assess_runtime_gate(runtime_rows, cohort_runtime_rows)
    summary = build_summary(
        admitted_rows,
        heldout_rows,
        family_manifest_rows,
        cohort_runtime_rows,
        family_runtime_rows,
        gate,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_payload = [
        {
            "source_lane": row.source_lane,
            "family": row.family,
            "baseline_stage": row.baseline_stage,
            "baseline_program_name": row.baseline_program_name,
            "baseline_horizon_multiplier": row.baseline_horizon_multiplier,
            "baseline_start": row.baseline_start,
            "retrieval_horizon_multiplier": row.retrieval_horizon_multiplier,
            "scaled_start": row.scaled_start,
            "comparison_mode": row.comparison_mode,
            "max_steps": row.max_steps,
            "boundary_family": row.boundary_family,
            "cohort": row.cohort,
            "variant_id": row.variant_id,
            "variant_group": row.variant_group,
            "envelope_rule": row.envelope_rule,
            "program_name": row.program_name,
            "address_signature": row.address_signature,
        }
        for row in all_rows
    ]
    write_json(
        OUT_DIR / "manifest_rows.json",
        {
            "experiment": "r19_pointer_like_surface_generalization_manifest_rows",
            "environment": environment.as_dict(),
            "rows": manifest_payload,
        },
    )
    write_csv(OUT_DIR / "manifest_rows.csv", manifest_payload)
    write_json(
        OUT_DIR / "family_manifest_summary.json",
        {
            "experiment": "r19_pointer_like_surface_generalization_family_summary",
            "environment": environment.as_dict(),
            "rows": family_manifest_rows,
        },
    )
    write_json(
        OUT_DIR / "runtime_rows.json",
        {
            "experiment": "r19_pointer_like_surface_generalization_runtime_rows",
            "environment": environment.as_dict(),
            "rows": runtime_rows,
        },
    )
    write_csv(OUT_DIR / "runtime_rows.csv", runtime_rows)
    write_json(
        OUT_DIR / "address_profiles.json",
        {
            "experiment": "r19_pointer_like_surface_generalization_address_profiles",
            "environment": environment.as_dict(),
            "rows": address_profiles,
        },
    )
    write_json(
        OUT_DIR / "cohort_runtime_summary.json",
        {
            "experiment": "r19_pointer_like_surface_generalization_cohort_runtime_summary",
            "environment": environment.as_dict(),
            "rows": cohort_runtime_rows,
        },
    )
    write_json(
        OUT_DIR / "family_runtime_summary.json",
        {
            "experiment": "r19_pointer_like_surface_generalization_family_runtime_summary",
            "environment": environment.as_dict(),
            "rows": family_runtime_rows,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r19_d0_pointer_like_surface_generalization_gate",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/R17_d0_full_surface_runtime_bridge/runtime_surface_index.json",
                "results/R17_d0_full_surface_runtime_bridge/runtime_bridge_rows.csv",
                "results/R18_d0_same_endpoint_runtime_repair_counterfactual/summary.json",
                "results/R8_d0_retrieval_pressure_gate/exact_suite_rows.json",
                "results/R15_d0_remaining_family_retrieval_pressure_gate/exact_suite_rows.json",
                "src/bytecode/datasets.py",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# R19 D0 Pointer-Like Surface Generalization Gate\n\n"
        "Bounded admitted-plus-heldout runtime gate for the next same-endpoint generalization lane.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `manifest_rows.json`\n"
        "- `manifest_rows.csv`\n"
        "- `family_manifest_summary.json`\n"
        "- `runtime_rows.json`\n"
        "- `runtime_rows.csv`\n"
        "- `address_profiles.json`\n"
        "- `cohort_runtime_summary.json`\n"
        "- `family_runtime_summary.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
