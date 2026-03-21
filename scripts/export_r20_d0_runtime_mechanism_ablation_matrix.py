"""Export the bounded runtime mechanism ablation matrix for R20."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import json
import os
from pathlib import Path
import re
from statistics import median
import time
from typing import Any, Iterable

from bytecode import (
    checkpoint_replay_long_program,
    helper_checkpoint_braid_long_program,
    helper_checkpoint_braid_program,
    indirect_counter_bank_program,
    iterated_helper_accumulator_program,
    lower_program,
    stack_memory_braid_program,
    subroutine_braid_long_program,
    subroutine_braid_program,
)
from exec_trace import Program, TraceEvent, TraceInterpreter, replay_trace
from model import compare_execution_to_reference
from model.free_running_executor import (
    FreeRunningExecutionResult,
    FreeRunningTraceExecutor,
    ReadObservation,
    _LatestWriteSpace,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
R19_OUT_DIR = ROOT / "results" / "R19_d0_pointer_like_surface_generalization_gate"
OUT_DIR = ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix"
PROFILE_REPEATS = 1


@dataclass(frozen=True, slots=True)
class StrategySpec:
    strategy_id: str
    control_class: str
    implementation_state: str
    expected_behavior: str
    runtime_mode: str
    imported_prefix: str | None = None


LINEAR_EXACT = StrategySpec(
    strategy_id="linear_exact",
    control_class="exact_baseline",
    implementation_state="imported_r19_baseline",
    expected_behavior="must_stay_exact",
    runtime_mode="imported_r19_baseline",
    imported_prefix="linear",
)
ACCELERATED = StrategySpec(
    strategy_id="accelerated",
    control_class="exact_baseline",
    implementation_state="imported_r19_baseline",
    expected_behavior="must_stay_exact",
    runtime_mode="imported_r19_baseline",
    imported_prefix="accelerated",
)
POINTER_LIKE_EXACT = StrategySpec(
    strategy_id="pointer_like_exact",
    control_class="target_mechanism",
    implementation_state="implemented",
    expected_behavior="must_stay_exact",
    runtime_mode="measured_r20",
)
POINTER_LIKE_SHUFFLED = StrategySpec(
    strategy_id="pointer_like_shuffled",
    control_class="negative_control",
    implementation_state="implemented",
    expected_behavior="should_break_speed_or_exactness",
    runtime_mode="measured_r20",
)
ADDRESS_OBLIVIOUS_CONTROL = StrategySpec(
    strategy_id="address_oblivious_control",
    control_class="negative_control",
    implementation_state="implemented",
    expected_behavior="should_break_speed_or_exactness",
    runtime_mode="measured_r20",
)

IMPORTED_BASELINES: tuple[StrategySpec, ...] = (LINEAR_EXACT, ACCELERATED)
MEASURED_STRATEGIES: tuple[StrategySpec, ...] = (
    POINTER_LIKE_EXACT,
    POINTER_LIKE_SHUFFLED,
    ADDRESS_OBLIVIOUS_CONTROL,
)
ALL_STRATEGIES: tuple[StrategySpec, ...] = IMPORTED_BASELINES + MEASURED_STRATEGIES
STRATEGY_ORDER = {spec.strategy_id: index for index, spec in enumerate(ALL_STRATEGIES)}


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


def remove_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def median_or_none(values: Iterable[float | None]) -> float | None:
    filtered = [value for value in values if value is not None]
    return median(filtered) if filtered else None


def rate_or_none(true_count: int, total_count: int) -> float | None:
    if total_count == 0:
        return None
    return true_count / total_count


def safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in {None, 0.0}:
        return None
    return numerator / denominator


def should_write_probe_read_rows() -> bool:
    return os.environ.get("R20_EXPORT_PROBE_READ_ROWS", "").strip() == "1"


def load_r19_runtime_rows() -> list[dict[str, Any]]:
    payload = read_json(R19_OUT_DIR / "runtime_rows.json")
    rows = list(payload["rows"])
    if len(rows) != 24:
        raise RuntimeError(f"R20 expected 24 runtime rows from R19, found {len(rows)}.")
    return rows


def build_sample_set(runtime_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    admitted_rows = [
        {
            **row,
            "selection_bucket": "admitted_regression_gate",
            "selection_reason": "preserve every admitted R19 row as the no-regression comparator set",
        }
        for row in runtime_rows
        if row["cohort"] == "admitted"
    ]
    if len(admitted_rows) != 8:
        raise RuntimeError(f"R20 expected 8 admitted rows from R19, found {len(admitted_rows)}.")

    heldout_by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in runtime_rows:
        if row["cohort"] != "heldout":
            continue
        if not bool(row["pointer_like_exact"]):
            continue
        heldout_by_family[str(row["family"])].append(row)

    heldout_focus_rows: list[dict[str, Any]] = []
    for family in sorted(heldout_by_family):
        family_rows = heldout_by_family[family]
        selected_row = min(
            family_rows,
            key=lambda item: (
                float(item["pointer_like_speedup_vs_current_accelerated"]),
                str(item["variant_id"]),
                str(item["program_name"]),
            ),
        )
        heldout_focus_rows.append(
            {
                **selected_row,
                "selection_bucket": "heldout_family_focus",
                "selection_reason": "select the exact heldout row with the lowest pointer-like speedup for this family",
            }
        )

    if len(heldout_focus_rows) != 8:
        raise RuntimeError(
            f"R20 expected 8 heldout focus rows from R19, found {len(heldout_focus_rows)}."
        )

    return sorted(
        admitted_rows + heldout_focus_rows,
        key=lambda row: (
            str(row["selection_bucket"]),
            str(row["family"]),
            str(row["cohort"]),
            str(row["program_name"]),
        ),
    )


def build_family_selection_summary(sample_rows: list[dict[str, Any]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in sample_rows:
        grouped[str(row["family"])].append(row)

    summary_rows: list[dict[str, object]] = []
    for family, family_rows in sorted(grouped.items()):
        admitted_rows = [row for row in family_rows if row["cohort"] == "admitted"]
        heldout_rows = [row for row in family_rows if row["cohort"] == "heldout"]
        summary_rows.append(
            {
                "family": family,
                "boundary_family": any(bool(row["boundary_family"]) for row in family_rows),
                "selected_row_count": len(family_rows),
                "admitted_selected_count": len(admitted_rows),
                "heldout_selected_count": len(heldout_rows),
                "heldout_variant_ids": sorted({str(row["variant_id"]) for row in heldout_rows}),
                "heldout_variant_groups": sorted({str(row["variant_group"]) for row in heldout_rows}),
                "min_pointer_like_speedup_vs_current_accelerated": min(
                    float(row["pointer_like_speedup_vs_current_accelerated"]) for row in family_rows
                ),
            }
        )
    return summary_rows


def build_control_matrix(sample_rows: list[dict[str, Any]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for sample_row in sample_rows:
        for spec in ALL_STRATEGIES:
            rows.append(
                {
                    "family": sample_row["family"],
                    "cohort": sample_row["cohort"],
                    "program_name": sample_row["program_name"],
                    "selection_bucket": sample_row["selection_bucket"],
                    "strategy_id": spec.strategy_id,
                    "control_class": spec.control_class,
                    "implementation_state": spec.implementation_state,
                    "runtime_mode": spec.runtime_mode,
                    "expected_behavior": spec.expected_behavior,
                }
            )
    return rows


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

    raise ValueError(f"Unsupported R20 program name: {program_name}")


class ProbeLatestWriteSpace(_LatestWriteSpace):
    """Expose deterministic control helpers for local mechanism probes."""

    def latest_candidate_for(self, address: int):
        self._ensure_readable_address(address)
        return self._candidates[self._latest_candidate_index_by_address[address]]

    def shuffled_address_for(self, address: int) -> int:
        self._ensure_readable_address(address)
        seen_addresses = sorted(self._seen_addresses)
        if len(seen_addresses) < 2:
            return address
        current_index = seen_addresses.index(address)
        return seen_addresses[(current_index + 1) % len(seen_addresses)]

    def latest_global_candidate(self):
        if not self._candidates:
            raise RuntimeError("Global latest candidate requested before any candidate exists.")
        return self._candidates[-1]


class MechanismProbeExecutor(FreeRunningTraceExecutor):
    """Local executor that records address-sensitive control metadata."""

    def __init__(self, *, strategy_id: str, hottest_address: int | None, default_memory_value: int = 0) -> None:
        super().__init__(
            stack_strategy="pointer_like_exact",
            memory_strategy="pointer_like_exact",
            default_memory_value=default_memory_value,
            validate_exact_reads=False,
        )
        self.strategy_id = strategy_id
        self.hottest_address = hottest_address
        self.probe_read_rows: list[dict[str, object]] = []
        self.retrieval_seconds = 0.0

    def run(self, program: Program, *, max_steps: int = 10_000) -> FreeRunningExecutionResult:
        epsilon = Fraction(1, max_steps + 2)
        stack_history = ProbeLatestWriteSpace(
            epsilon=epsilon,
            default_value=0,
            allow_default_reads=False,
        )
        memory_history = ProbeLatestWriteSpace(
            epsilon=epsilon,
            default_value=self.default_memory_value,
            allow_default_reads=True,
        )

        events: list[TraceEvent] = []
        read_observations: list[ReadObservation] = []
        step = 0
        pc = 0
        stack_depth = 0
        call_stack: list[int] = []
        halted = False

        while not halted:
            if step >= max_steps:
                raise RuntimeError(f"Maximum step budget exceeded for program {program.name!r}.")
            if not (0 <= pc < len(program)):
                raise RuntimeError(f"Program counter out of range: {pc}")

            instruction = program.instructions[pc]
            popped, pushed, branch_taken, memory_read, memory_write, next_pc, halted = self._execute_instruction(
                step=step,
                pc=pc,
                stack_depth=stack_depth,
                call_stack=call_stack,
                instruction=instruction.opcode,
                arg=instruction.arg,
                stack_history=stack_history,
                memory_history=memory_history,
                read_observations=read_observations,
            )

            event = TraceEvent(
                step=step,
                pc=pc,
                opcode=instruction.opcode,
                arg=instruction.arg,
                popped=popped,
                pushed=pushed,
                branch_taken=branch_taken,
                memory_read_address=None if memory_read is None else memory_read[0],
                memory_read_value=None if memory_read is None else memory_read[1],
                memory_write=memory_write,
                next_pc=next_pc,
                stack_depth_before=stack_depth,
                stack_depth_after=stack_depth - len(popped) + len(pushed),
                halted=halted,
            )
            events.append(event)

            write_base = stack_depth - len(popped)
            for offset, value in enumerate(pushed):
                stack_history.write(write_base + offset, value, step)
            if memory_write is not None:
                memory_history.write(memory_write[0], memory_write[1], step)

            step += 1
            pc = next_pc
            stack_depth = event.stack_depth_after

        final_state = replay_trace(program, tuple(events))
        return FreeRunningExecutionResult(
            program=program,
            events=tuple(events),
            final_state=final_state,
            read_observations=tuple(read_observations),
            stack_strategy="pointer_like_exact",
            memory_strategy="pointer_like_exact",
        )

    def _read_from_space(
        self,
        *,
        step: int,
        address: int,
        space: str,
        strategy: str,
        history: ProbeLatestWriteSpace,
        scorer,
        read_observations: list[ReadObservation],
    ) -> int:
        del strategy, scorer

        read_started = time.perf_counter()
        history._ensure_readable_address(address)
        pointer_candidate = history.latest_candidate_for(address)
        pointer_value = int(pointer_candidate.value)
        linear_value = pointer_value
        accelerated_value = pointer_value

        if self.strategy_id == POINTER_LIKE_EXACT.strategy_id:
            selected_address = address
            selected_candidate = pointer_candidate
            control_note = "exact_latest_write"
        elif self.strategy_id == POINTER_LIKE_SHUFFLED.strategy_id:
            selected_address = history.shuffled_address_for(address)
            selected_candidate = history.latest_candidate_for(selected_address)
            control_note = (
                "identity_only_one_seen_address"
                if selected_address == address
                else "cyclic_seen_address_permutation"
            )
        elif self.strategy_id == ADDRESS_OBLIVIOUS_CONTROL.strategy_id:
            selected_candidate = history.latest_global_candidate()
            selected_address = int(selected_candidate.address)
            control_note = "global_latest_candidate"
        else:  # pragma: no cover - guarded by exporter configuration
            raise RuntimeError(f"Unsupported mechanism probe strategy: {self.strategy_id}")

        chosen_value = int(selected_candidate.value)
        self.retrieval_seconds += time.perf_counter() - read_started

        read_observations.append(
            ReadObservation(
                step=step,
                space=space,
                address=address,
                source="pointer_like_exact",
                chosen_value=chosen_value,
                linear_value=linear_value,
                accelerated_value=accelerated_value,
            )
        )

        selected_step = int(selected_candidate.step)
        correct_step = int(pointer_candidate.step)
        self.probe_read_rows.append(
            {
                "strategy_id": self.strategy_id,
                "step": step,
                "space": space,
                "query_address": address,
                "selected_address": selected_address,
                "linear_value": linear_value,
                "accelerated_value": accelerated_value,
                "pointer_value": pointer_value,
                "chosen_value": chosen_value,
                "retrieval_correct": chosen_value == linear_value,
                "address_match": selected_address == address,
                "hottest_address": self.hottest_address,
                "hottest_address_hit": None if self.hottest_address is None else selected_address == self.hottest_address,
                "selected_candidate_step": selected_step,
                "correct_candidate_step": correct_step,
                "selected_step_gap": step - selected_step,
                "correct_step_gap": step - correct_step,
                "step_gap_delta": (step - selected_step) - (step - correct_step),
                "selected_candidate_is_default": bool(selected_candidate.is_default),
                "correct_candidate_is_default": bool(pointer_candidate.is_default),
                "control_note": control_note,
            }
        )
        return chosen_value


def build_imported_baseline_row(sample_row: dict[str, Any], strategy: StrategySpec) -> dict[str, object]:
    if strategy.imported_prefix is None:
        raise RuntimeError(f"R20 baseline strategy {strategy.strategy_id} is missing an imported prefix.")
    prefix = strategy.imported_prefix
    return {
        "source_runtime_stage": "r19_d0_pointer_like_surface_generalization_gate",
        "family": sample_row["family"],
        "cohort": sample_row["cohort"],
        "variant_id": sample_row["variant_id"],
        "variant_group": sample_row["variant_group"],
        "program_name": sample_row["program_name"],
        "selection_bucket": sample_row["selection_bucket"],
        "selection_reason": sample_row["selection_reason"],
        "comparison_mode": sample_row["comparison_mode"],
        "max_steps": sample_row["max_steps"],
        "boundary_family": sample_row["boundary_family"],
        "memory_operation_count": sample_row["memory_operation_count"],
        "unique_address_count": sample_row["unique_address_count"],
        "hottest_address": sample_row["hottest_address"],
        "strategy_id": strategy.strategy_id,
        "control_class": strategy.control_class,
        "implementation_state": strategy.implementation_state,
        "runtime_mode": strategy.runtime_mode,
        "expected_behavior": strategy.expected_behavior,
        "profile_repeats": PROFILE_REPEATS,
        "median_seconds": sample_row[f"{prefix}_median_seconds"],
        "samples": sample_row[f"{prefix}_samples"],
        "ns_per_step": sample_row[f"{prefix}_ns_per_step"],
        "exact_trace_match": sample_row[f"{prefix}_exact_trace_match"],
        "exact_final_state_match": sample_row[f"{prefix}_exact_final_state_match"],
        "first_mismatch_step": sample_row[f"{prefix}_first_mismatch_step"],
        "failure_reason": sample_row[f"{prefix}_failure_reason"],
        "read_observation_count": sample_row[f"{prefix}_read_observation_count"],
        "memory_read_count": sample_row[f"{prefix}_memory_read_count"],
        "stack_read_count": sample_row[f"{prefix}_stack_read_count"],
        "exact": sample_row[f"{prefix}_exact"],
        "retrieval_seconds": None,
        "non_retrieval_seconds": None,
        "retrieval_share": None,
        "ns_per_read": None,
    }


def measure_strategy_on_sample_row(sample_row: dict[str, Any], strategy: StrategySpec) -> tuple[dict[str, object], list[dict[str, object]]]:
    program = materialize_program(str(sample_row["program_name"]))
    lowered_program = lower_program(program)
    max_steps = int(sample_row["max_steps"])
    reference = TraceInterpreter().run(lowered_program, max_steps=max_steps)

    executor = MechanismProbeExecutor(
        strategy_id=strategy.strategy_id,
        hottest_address=None if sample_row["hottest_address"] is None else int(sample_row["hottest_address"]),
    )
    started = time.perf_counter()
    execution: FreeRunningExecutionResult | None = None
    error: Exception | None = None
    try:
        execution = executor.run(lowered_program, max_steps=max_steps)
    except Exception as exc:  # pragma: no cover - exercised in exporter runs
        error = exc
    total_seconds = time.perf_counter() - started

    if execution is None:
        probe_rows = [
            {
                **probe_row,
                "family": sample_row["family"],
                "cohort": sample_row["cohort"],
                "variant_id": sample_row["variant_id"],
                "variant_group": sample_row["variant_group"],
                "program_name": sample_row["program_name"],
                "selection_bucket": sample_row["selection_bucket"],
                "comparison_mode": sample_row["comparison_mode"],
                "boundary_family": sample_row["boundary_family"],
            }
            for probe_row in executor.probe_read_rows
        ]
        runtime_row = {
            "source_runtime_stage": "r20_d0_runtime_mechanism_ablation_matrix",
            "family": sample_row["family"],
            "cohort": sample_row["cohort"],
            "variant_id": sample_row["variant_id"],
            "variant_group": sample_row["variant_group"],
            "program_name": sample_row["program_name"],
            "selection_bucket": sample_row["selection_bucket"],
            "selection_reason": sample_row["selection_reason"],
            "comparison_mode": sample_row["comparison_mode"],
            "max_steps": sample_row["max_steps"],
            "boundary_family": sample_row["boundary_family"],
            "memory_operation_count": sample_row["memory_operation_count"],
            "unique_address_count": sample_row["unique_address_count"],
            "hottest_address": sample_row["hottest_address"],
            "strategy_id": strategy.strategy_id,
            "control_class": strategy.control_class,
            "implementation_state": strategy.implementation_state,
            "runtime_mode": strategy.runtime_mode,
            "expected_behavior": strategy.expected_behavior,
            "profile_repeats": PROFILE_REPEATS,
            "median_seconds": total_seconds,
            "samples": [total_seconds],
            "ns_per_step": None,
            "exact_trace_match": False,
            "exact_final_state_match": False,
            "first_mismatch_step": None,
            "failure_reason": f"{type(error).__name__}: {error}" if error is not None else None,
            "read_observation_count": 0,
            "memory_read_count": 0,
            "stack_read_count": 0,
            "exact": False,
            "retrieval_seconds": executor.retrieval_seconds,
            "non_retrieval_seconds": None,
            "retrieval_share": None,
            "ns_per_read": None,
        }
        return runtime_row, probe_rows

    outcome = compare_execution_to_reference(lowered_program, execution, reference=reference)
    program_steps = max(1, int(outcome.program_steps))
    read_observation_count = len(execution.read_observations)
    memory_read_count = sum(observation.space == "memory" for observation in execution.read_observations)
    stack_read_count = sum(observation.space == "stack" for observation in execution.read_observations)

    runtime_row = {
        "source_runtime_stage": "r20_d0_runtime_mechanism_ablation_matrix",
        "family": sample_row["family"],
        "cohort": sample_row["cohort"],
        "variant_id": sample_row["variant_id"],
        "variant_group": sample_row["variant_group"],
        "program_name": sample_row["program_name"],
        "selection_bucket": sample_row["selection_bucket"],
        "selection_reason": sample_row["selection_reason"],
        "comparison_mode": sample_row["comparison_mode"],
        "max_steps": sample_row["max_steps"],
        "boundary_family": sample_row["boundary_family"],
        "memory_operation_count": sample_row["memory_operation_count"],
        "unique_address_count": sample_row["unique_address_count"],
        "hottest_address": sample_row["hottest_address"],
        "strategy_id": strategy.strategy_id,
        "control_class": strategy.control_class,
        "implementation_state": strategy.implementation_state,
        "runtime_mode": strategy.runtime_mode,
        "expected_behavior": strategy.expected_behavior,
        "profile_repeats": PROFILE_REPEATS,
        "median_seconds": total_seconds,
        "samples": [total_seconds],
        "ns_per_step": (total_seconds / program_steps) * 1e9,
        "exact_trace_match": outcome.exact_trace_match,
        "exact_final_state_match": outcome.exact_final_state_match,
        "first_mismatch_step": outcome.first_mismatch_step,
        "failure_reason": outcome.failure_reason,
        "read_observation_count": read_observation_count,
        "memory_read_count": memory_read_count,
        "stack_read_count": stack_read_count,
        "exact": bool(outcome.exact_trace_match and outcome.exact_final_state_match and outcome.failure_reason is None),
        "retrieval_seconds": executor.retrieval_seconds,
        "non_retrieval_seconds": total_seconds - executor.retrieval_seconds,
        "retrieval_share": safe_ratio(executor.retrieval_seconds, total_seconds),
        "ns_per_read": None if read_observation_count == 0 else (executor.retrieval_seconds / read_observation_count) * 1e9,
    }

    probe_rows = [
        {
            **probe_row,
            "family": sample_row["family"],
            "cohort": sample_row["cohort"],
            "variant_id": sample_row["variant_id"],
            "variant_group": sample_row["variant_group"],
            "program_name": sample_row["program_name"],
            "selection_bucket": sample_row["selection_bucket"],
            "comparison_mode": sample_row["comparison_mode"],
            "boundary_family": sample_row["boundary_family"],
        }
        for probe_row in executor.probe_read_rows
    ]
    return runtime_row, probe_rows


def execute_mechanism_rows(sample_rows: list[dict[str, Any]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    runtime_rows: list[dict[str, object]] = []
    probe_rows: list[dict[str, object]] = []
    total_jobs = len(sample_rows) * len(MEASURED_STRATEGIES)
    completed_jobs = 0
    for sample_row in sample_rows:
        for strategy in MEASURED_STRATEGIES:
            runtime_row, row_probe_rows = measure_strategy_on_sample_row(sample_row, strategy)
            runtime_rows.append(runtime_row)
            probe_rows.extend(row_probe_rows)
            completed_jobs += 1
            print(
                f"[R20] completed {completed_jobs}/{total_jobs} {sample_row['program_name']} {strategy.strategy_id}",
                flush=True,
            )
    return runtime_rows, probe_rows


def build_runtime_matrix_rows(
    sample_rows: list[dict[str, Any]],
    measured_runtime_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    imported_rows = [
        build_imported_baseline_row(sample_row, strategy)
        for sample_row in sample_rows
        for strategy in IMPORTED_BASELINES
    ]
    runtime_rows = imported_rows + measured_runtime_rows
    accelerated_ns_by_program = {
        str(row["program_name"]): row["ns_per_step"]
        for row in runtime_rows
        if row["strategy_id"] == ACCELERATED.strategy_id
    }
    linear_ns_by_program = {
        str(row["program_name"]): row["ns_per_step"]
        for row in runtime_rows
        if row["strategy_id"] == LINEAR_EXACT.strategy_id
    }

    for row in runtime_rows:
        program_name = str(row["program_name"])
        row["speedup_vs_imported_accelerated"] = safe_ratio(
            accelerated_ns_by_program.get(program_name),
            row["ns_per_step"],
        )
        row["speedup_vs_imported_linear"] = safe_ratio(
            linear_ns_by_program.get(program_name),
            row["ns_per_step"],
        )

    return sorted(
        runtime_rows,
        key=lambda row: (
            str(row["selection_bucket"]),
            str(row["family"]),
            str(row["cohort"]),
            str(row["program_name"]),
            STRATEGY_ORDER[str(row["strategy_id"])],
        ),
    )


def build_row_mechanism_summary(
    runtime_matrix_rows: list[dict[str, object]],
    probe_read_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    probe_by_row: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for probe_row in probe_read_rows:
        probe_by_row[(str(probe_row["program_name"]), str(probe_row["strategy_id"]))].append(probe_row)

    summary_rows: list[dict[str, object]] = []
    for runtime_row in runtime_matrix_rows:
        key = (str(runtime_row["program_name"]), str(runtime_row["strategy_id"]))
        probes = probe_by_row.get(key, [])
        memory_probes = [probe for probe in probes if probe["space"] == "memory"]
        stack_probes = [probe for probe in probes if probe["space"] == "stack"]
        hottest_known_count = sum(probe["hottest_address_hit"] is not None for probe in probes)

        summary_rows.append(
            {
                "family": runtime_row["family"],
                "cohort": runtime_row["cohort"],
                "variant_id": runtime_row["variant_id"],
                "program_name": runtime_row["program_name"],
                "selection_bucket": runtime_row["selection_bucket"],
                "strategy_id": runtime_row["strategy_id"],
                "control_class": runtime_row["control_class"],
                "runtime_mode": runtime_row["runtime_mode"],
                "probe_observation_count": len(probes),
                "memory_probe_count": len(memory_probes),
                "stack_probe_count": len(stack_probes),
                "retrieval_correct_rate": rate_or_none(sum(bool(probe["retrieval_correct"]) for probe in probes), len(probes)),
                "memory_retrieval_correct_rate": rate_or_none(
                    sum(bool(probe["retrieval_correct"]) for probe in memory_probes),
                    len(memory_probes),
                ),
                "stack_retrieval_correct_rate": rate_or_none(
                    sum(bool(probe["retrieval_correct"]) for probe in stack_probes),
                    len(stack_probes),
                ),
                "address_match_rate": rate_or_none(sum(bool(probe["address_match"]) for probe in probes), len(probes)),
                "memory_address_match_rate": rate_or_none(
                    sum(bool(probe["address_match"]) for probe in memory_probes),
                    len(memory_probes),
                ),
                "stack_address_match_rate": rate_or_none(
                    sum(bool(probe["address_match"]) for probe in stack_probes),
                    len(stack_probes),
                ),
                "hottest_address_hit_rate": rate_or_none(
                    sum(bool(probe["hottest_address_hit"]) for probe in probes if probe["hottest_address_hit"] is not None),
                    hottest_known_count,
                ),
                "selected_default_rate": rate_or_none(
                    sum(bool(probe["selected_candidate_is_default"]) for probe in probes),
                    len(probes),
                ),
                "correct_default_rate": rate_or_none(
                    sum(bool(probe["correct_candidate_is_default"]) for probe in probes),
                    len(probes),
                ),
                "median_selected_step_gap": median_or_none(int(probe["selected_step_gap"]) for probe in probes),
                "median_correct_step_gap": median_or_none(int(probe["correct_step_gap"]) for probe in probes),
                "median_step_gap_delta": median_or_none(int(probe["step_gap_delta"]) for probe in probes),
            }
        )
    return summary_rows


def build_strategy_summary(
    runtime_matrix_rows: list[dict[str, object]],
    row_mechanism_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    runtime_by_strategy: dict[str, list[dict[str, object]]] = defaultdict(list)
    mechanism_by_strategy: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in runtime_matrix_rows:
        runtime_by_strategy[str(row["strategy_id"])].append(row)
    for row in row_mechanism_rows:
        mechanism_by_strategy[str(row["strategy_id"])].append(row)

    summary_rows: list[dict[str, object]] = []
    for strategy in ALL_STRATEGIES:
        runtime_rows = runtime_by_strategy[strategy.strategy_id]
        mechanism_rows = mechanism_by_strategy[strategy.strategy_id]
        exact_failures = [str(row["program_name"]) for row in runtime_rows if not bool(row["exact"])]
        row_count = len(runtime_rows)
        exact_case_count = sum(bool(row["exact"]) for row in runtime_rows)
        median_retrieval_correct_rate = median_or_none(row["retrieval_correct_rate"] for row in mechanism_rows)
        median_address_match_rate = median_or_none(row["address_match_rate"] for row in mechanism_rows)
        claim_relevant_failure = False
        if strategy.control_class == "negative_control":
            claim_relevant_failure = (
                exact_case_count < row_count
                or (median_retrieval_correct_rate is not None and median_retrieval_correct_rate < 1.0)
                or (median_address_match_rate is not None and median_address_match_rate < 1.0)
            )

        summary_rows.append(
            {
                "strategy_id": strategy.strategy_id,
                "control_class": strategy.control_class,
                "runtime_mode": strategy.runtime_mode,
                "row_count": row_count,
                "exact_case_count": exact_case_count,
                "exact_case_rate": rate_or_none(exact_case_count, row_count),
                "median_ns_per_step": median_or_none(row["ns_per_step"] for row in runtime_rows),
                "median_speedup_vs_imported_accelerated": median_or_none(
                    row["speedup_vs_imported_accelerated"] for row in runtime_rows
                ),
                "median_speedup_vs_imported_linear": median_or_none(
                    row["speedup_vs_imported_linear"] for row in runtime_rows
                ),
                "median_retrieval_share": median_or_none(row["retrieval_share"] for row in runtime_rows),
                "median_retrieval_correct_rate": median_retrieval_correct_rate,
                "median_address_match_rate": median_address_match_rate,
                "median_hottest_address_hit_rate": median_or_none(
                    row["hottest_address_hit_rate"] for row in mechanism_rows
                ),
                "median_selected_step_gap": median_or_none(
                    row["median_selected_step_gap"] for row in mechanism_rows
                ),
                "median_correct_step_gap": median_or_none(
                    row["median_correct_step_gap"] for row in mechanism_rows
                ),
                "median_step_gap_delta": median_or_none(
                    row["median_step_gap_delta"] for row in mechanism_rows
                ),
                "claim_relevant_failure": claim_relevant_failure,
                "exact_failure_program_names": exact_failures,
            }
        )

    return summary_rows


def assess_mechanism_gate(strategy_summary_rows: list[dict[str, object]], *, total_case_count: int) -> dict[str, object]:
    by_strategy = {str(row["strategy_id"]): row for row in strategy_summary_rows}
    pointer_row = by_strategy[POINTER_LIKE_EXACT.strategy_id]
    negative_control_rows = [
        by_strategy[POINTER_LIKE_SHUFFLED.strategy_id],
        by_strategy[ADDRESS_OBLIVIOUS_CONTROL.strategy_id],
    ]
    pointer_like_exact_gate_passed = int(pointer_row["exact_case_count"]) == total_case_count
    negative_controls_with_claim_relevant_failure = [
        str(row["strategy_id"]) for row in negative_control_rows if bool(row["claim_relevant_failure"])
    ]

    if pointer_like_exact_gate_passed and negative_controls_with_claim_relevant_failure:
        lane_verdict = "mechanism_supported"
        next_priority_lane = "r21_d0_exact_executor_boundary_break_map"
        reason = (
            "Pointer-like exact stayed exact on the bounded sample set, and at least one negative control failed in a claim-relevant way."
        )
    elif pointer_like_exact_gate_passed:
        lane_verdict = "speed_only_without_mechanism_support"
        next_priority_lane = "r21_d0_exact_executor_boundary_break_map"
        reason = (
            "Pointer-like exact stayed exact, but the bounded negative controls did not yet produce a clear claim-relevant break."
        )
    else:
        lane_verdict = "mechanism_not_supported"
        next_priority_lane = "h19_refreeze_and_next_scope_decision"
        reason = (
            "Pointer-like exact did not preserve exact execution on the fixed R20 sample set, so the mechanism lane cannot support the intended claim."
        )

    return {
        "lane_verdict": lane_verdict,
        "reason": reason,
        "pointer_like_exact_gate_passed": pointer_like_exact_gate_passed,
        "pointer_like_exact_case_count": int(pointer_row["exact_case_count"]),
        "total_case_count": total_case_count,
        "negative_controls_with_claim_relevant_failure": negative_controls_with_claim_relevant_failure,
        "pointer_like_exact_median_speedup_vs_imported_accelerated": pointer_row[
            "median_speedup_vs_imported_accelerated"
        ],
        "next_priority_lane": next_priority_lane,
    }


def build_summary(
    sample_rows: list[dict[str, Any]],
    family_selection_rows: list[dict[str, object]],
    strategy_summary_rows: list[dict[str, object]],
    gate: dict[str, object],
) -> dict[str, object]:
    admitted_case_count = sum(row["cohort"] == "admitted" for row in sample_rows)
    heldout_case_count = sum(row["cohort"] == "heldout" for row in sample_rows)
    by_strategy = {str(row["strategy_id"]): row for row in strategy_summary_rows}
    pointer_row = by_strategy[POINTER_LIKE_EXACT.strategy_id]
    shuffled_row = by_strategy[POINTER_LIKE_SHUFFLED.strategy_id]
    oblivious_row = by_strategy[ADDRESS_OBLIVIOUS_CONTROL.strategy_id]

    supported_here = [
        "R20 stayed on the fixed 16-row sample set exported from landed R19 without widening the D0 endpoint.",
        (
            f"Pointer-like exact stayed exact on {pointer_row['exact_case_count']}/{len(sample_rows)} selected rows "
            "under the current mechanism probe runtime."
        ),
        (
            "The negative-control set is now executed rather than merely planned: "
            f"shuffled exact count = {shuffled_row['exact_case_count']}/{len(sample_rows)}, "
            f"address-oblivious exact count = {oblivious_row['exact_case_count']}/{len(sample_rows)}."
        ),
    ]
    unsupported_here = [
        "R20 still does not justify any broader softmax-replacement or widened compiled-endpoint claim.",
        "Linear and accelerated baselines remain imported from landed R19 rather than freshly reprofiled here.",
    ]
    if gate["lane_verdict"] != "mechanism_supported":
        unsupported_here.append("R20 did not close as a mechanism-supported packet on the current bounded evidence.")

    return {
        "status": "r20_runtime_ablation_complete",
        "current_frozen_stage": "h17_refreeze_and_conditional_frontier_recheck",
        "source_runtime_stage": "r19_d0_pointer_like_surface_generalization_gate",
        "selected_case_count": len(sample_rows),
        "admitted_case_count": admitted_case_count,
        "heldout_focus_case_count": heldout_case_count,
        "family_count": len(family_selection_rows),
        "selection_rule": "all admitted rows plus one exact heldout row per family chosen by the lowest pointer-like speedup vs current accelerated",
        "gate": gate,
        "strategy_summary": strategy_summary_rows,
        "next_priority_lane": gate["next_priority_lane"],
        "recommended_next_action": (
            "Advance to R21 to map the boundary of the current exact executor while keeping H19/P13 downstream of the bounded R20 result."
            if gate["next_priority_lane"] == "r21_d0_exact_executor_boundary_break_map"
            else "Refreeze the current mainline and record the R20 regression before any further runtime claims."
        ),
        "supported_here": supported_here,
        "unsupported_here": unsupported_here,
    }


def main() -> None:
    environment = detect_runtime_environment()
    write_probe_read_rows = should_write_probe_read_rows()
    sample_rows = build_sample_set(load_r19_runtime_rows())
    family_selection_rows = build_family_selection_summary(sample_rows)
    control_rows = build_control_matrix(sample_rows)
    measured_runtime_rows, probe_read_rows = execute_mechanism_rows(sample_rows)
    runtime_matrix_rows = build_runtime_matrix_rows(sample_rows, measured_runtime_rows)
    row_mechanism_rows = build_row_mechanism_summary(runtime_matrix_rows, probe_read_rows)
    strategy_summary_rows = build_strategy_summary(runtime_matrix_rows, row_mechanism_rows)
    gate = assess_mechanism_gate(strategy_summary_rows, total_case_count=len(sample_rows))
    summary = build_summary(sample_rows, family_selection_rows, strategy_summary_rows, gate)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "sample_set_rows.json",
        {
            "experiment": "r20_sample_set_rows",
            "environment": environment.as_dict(),
            "rows": sample_rows,
        },
    )
    write_csv(OUT_DIR / "sample_set_rows.csv", sample_rows)
    write_json(
        OUT_DIR / "family_selection_summary.json",
        {
            "experiment": "r20_family_selection_summary",
            "environment": environment.as_dict(),
            "rows": family_selection_rows,
        },
    )
    write_json(
        OUT_DIR / "control_matrix.json",
        {
            "experiment": "r20_control_matrix",
            "environment": environment.as_dict(),
            "rows": control_rows,
        },
    )
    write_csv(OUT_DIR / "control_matrix.csv", control_rows)
    write_json(
        OUT_DIR / "runtime_matrix_rows.json",
        {
            "experiment": "r20_runtime_matrix_rows",
            "environment": environment.as_dict(),
            "rows": runtime_matrix_rows,
        },
    )
    write_csv(OUT_DIR / "runtime_matrix_rows.csv", runtime_matrix_rows)
    probe_read_rows_path = OUT_DIR / "probe_read_rows.json"
    if write_probe_read_rows:
        write_json(
            probe_read_rows_path,
            {
                "experiment": "r20_probe_read_rows",
                "environment": environment.as_dict(),
                "rows": probe_read_rows,
            },
        )
    else:
        remove_if_exists(probe_read_rows_path)
    write_json(
        OUT_DIR / "row_mechanism_summary.json",
        {
            "experiment": "r20_row_mechanism_summary",
            "environment": environment.as_dict(),
            "rows": row_mechanism_rows,
        },
    )
    write_json(
        OUT_DIR / "strategy_summary.json",
        {
            "experiment": "r20_strategy_summary",
            "environment": environment.as_dict(),
            "rows": strategy_summary_rows,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r20_d0_runtime_mechanism_ablation_matrix",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/R19_d0_pointer_like_surface_generalization_gate/summary.json",
                "results/R19_d0_pointer_like_surface_generalization_gate/runtime_rows.json",
                "results/R19_d0_pointer_like_surface_generalization_gate/family_runtime_summary.json",
                "scripts/export_r19_d0_pointer_like_surface_generalization_gate.py",
                "src/model/free_running_executor.py",
            ],
            "summary": summary,
        },
    )
    readme_text = (
        "# R20 D0 Runtime Mechanism Ablation Matrix\n\n"
        "Bounded runtime ablation packet on the fixed R19-derived same-endpoint sample set.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `sample_set_rows.json`\n"
        "- `sample_set_rows.csv`\n"
        "- `family_selection_summary.json`\n"
        "- `control_matrix.json`\n"
        "- `control_matrix.csv`\n"
        "- `runtime_matrix_rows.json`\n"
        "- `runtime_matrix_rows.csv`\n"
        "- `row_mechanism_summary.json`\n"
        "- `strategy_summary.json`\n"
    )
    if write_probe_read_rows:
        readme_text += (
            "\nOptional local-only debug artifact:\n"
            "- `probe_read_rows.json` when `R20_EXPORT_PROBE_READ_ROWS=1`\n"
        )
    (OUT_DIR / "README.md").write_text(readme_text, encoding="utf-8")
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
