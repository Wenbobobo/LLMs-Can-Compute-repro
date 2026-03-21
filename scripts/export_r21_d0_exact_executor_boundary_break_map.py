"""Export the bounded exact-executor boundary map for R21."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
import json
import math
from pathlib import Path
from statistics import median
import time
from typing import Any, Iterable

from bytecode import (
    checkpoint_replay_long_program,
    helper_checkpoint_braid_program,
    lower_program,
    subroutine_braid_program,
)
from bytecode.ir import BytecodeInstruction, BytecodeOpcode, BytecodeProgram
from exec_trace import TraceInterpreter
from model import compare_execution_to_reference
from model.exact_hardmax import extract_memory_operations
from model.free_running_executor import FreeRunningExecutionResult, FreeRunningTraceExecutor
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
R19_OUT_DIR = ROOT / "results" / "R19_d0_pointer_like_surface_generalization_gate"
OUT_DIR = ROOT / "results" / "R21_d0_exact_executor_boundary_break_map"
FAILURE_LIMIT_PER_BRANCH = 2
UNIQUE_ADDRESS_TARGETS = (6, 8, 12, 16)
HORIZON_MULTIPLIERS = (1.0, 1.5, 2.0)
CHECKPOINT_DEPTHS = ("baseline", "plus_one")
HOT_ADDRESS_SKEWS = ("baseline", "flattened")
SEED_IDS = (0, 1)
CONTROL_FLOW_OPCODES = {
    BytecodeOpcode.JMP,
    BytecodeOpcode.JZ_ZERO,
    BytecodeOpcode.CALL,
}
TARGET_FAMILY_BY_UNIQUE = {
    6: "subroutine_braid",
    8: "helper_checkpoint_braid",
    12: "checkpoint_replay_long",
    16: "checkpoint_replay_long",
}


@dataclass(frozen=True, slots=True)
class TemplateConfig:
    unique_address_target: int
    family: str
    comparison_mode: str
    base_program_name: str
    base_start: int
    base_max_steps: int
    base_unique_address_count: int
    base_memory_operation_count: int


@dataclass(frozen=True, slots=True)
class BranchSpec:
    branch_id: str
    candidate_id: str
    unique_address_target: int
    horizon_multiplier: float
    checkpoint_depth: str
    hot_address_skew: str
    seed_id: int
    family: str
    comparison_mode: str
    base_program_name: str
    seed_variant: str
    base_start: int
    scaled_start: int
    base_max_steps: int
    max_steps: int
    base_unique_address_count: int
    padding_unique_count: int
    flatten_rounds: int
    padding_base_address: int
    expected_padding_instruction_count: int
    target_wrapper_call_depth: int


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


def rate_or_none(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def median_or_none(values: Iterable[float | None]) -> float | None:
    filtered = [value for value in values if value is not None]
    return median(filtered) if filtered else None


def multiplier_label(multiplier: float) -> str:
    return f"{multiplier:.1f}".replace(".", "p")


def format_axis_tags(
    *,
    unique_address_target: int,
    checkpoint_depth: str,
    hot_address_skew: str,
    hottest_address_share: float | None,
) -> str:
    tags: list[str] = []
    if unique_address_target >= 12:
        tags.append("high_unique_address_target")
    if checkpoint_depth == "plus_one":
        tags.append("plus_one_checkpoint_depth")
    if hot_address_skew == "flattened":
        tags.append("flattened_hot_address_target")
    if hottest_address_share is not None and hottest_address_share < 0.30:
        tags.append("low_hottest_address_share_observed")
    return ",".join(tags)


def load_r19_admitted_runtime_rows() -> dict[str, dict[str, Any]]:
    payload = read_json(R19_OUT_DIR / "runtime_rows.json")
    admitted_rows = [row for row in payload["rows"] if row["cohort"] == "admitted"]
    if len(admitted_rows) != 8:
        raise RuntimeError(
            f"R21 expected 8 admitted runtime rows from R19, found {len(admitted_rows)}."
        )
    by_family = {str(row["family"]): row for row in admitted_rows}
    missing_families = sorted(set(TARGET_FAMILY_BY_UNIQUE.values()) - set(by_family))
    if missing_families:
        raise RuntimeError(f"R21 missing R19 admitted anchors for families: {missing_families}.")
    return by_family


def build_template_registry(
    admitted_rows_by_family: dict[str, dict[str, Any]],
) -> list[TemplateConfig]:
    registry: list[TemplateConfig] = []
    for unique_target in UNIQUE_ADDRESS_TARGETS:
        family = TARGET_FAMILY_BY_UNIQUE[unique_target]
        admitted_row = admitted_rows_by_family[family]
        registry.append(
            TemplateConfig(
                unique_address_target=unique_target,
                family=family,
                comparison_mode=str(admitted_row["comparison_mode"]),
                base_program_name=str(admitted_row["program_name"]),
                base_start=int(admitted_row["scaled_start"]),
                base_max_steps=int(admitted_row["max_steps"]),
                base_unique_address_count=int(admitted_row["unique_address_count"]),
                base_memory_operation_count=int(admitted_row["memory_operation_count"]),
            )
        )
    return registry


def seed_variant_for_family(family: str, seed_id: int) -> str:
    if family == "subroutine_braid":
        return "r19_admitted_address_anchor" if seed_id == 0 else "r19_heldout_address_anchor"
    if family == "helper_checkpoint_braid":
        return "r19_admitted_seed_anchor" if seed_id == 0 else "r19_heldout_seed_anchor"
    if family == "checkpoint_replay_long":
        return "r19_admitted_address_anchor" if seed_id == 0 else "r19_heldout_address_anchor"
    raise ValueError(f"Unsupported R21 family for seed variant lookup: {family}")


def build_branch_specs(template_registry: list[TemplateConfig]) -> list[BranchSpec]:
    branch_specs: list[BranchSpec] = []
    branch_counter = 0
    for template in template_registry:
        padding_unique_count = template.unique_address_target - template.base_unique_address_count
        if padding_unique_count < 0:
            raise RuntimeError(
                f"R21 target {template.unique_address_target} is below the base unique count "
                f"{template.base_unique_address_count} for {template.family}."
            )
        for horizon_multiplier in HORIZON_MULTIPLIERS:
            scaled_start = max(1, int(round(template.base_start * horizon_multiplier)))
            for checkpoint_depth in CHECKPOINT_DEPTHS:
                for hot_address_skew in HOT_ADDRESS_SKEWS:
                    branch_id = (
                        f"u{template.unique_address_target}_"
                        f"h{multiplier_label(horizon_multiplier)}_"
                        f"c{checkpoint_depth}_"
                        f"k{hot_address_skew}"
                    )
                    flatten_rounds = 0
                    if hot_address_skew == "flattened":
                        if padding_unique_count == 0:
                            raise RuntimeError(
                                f"R21 cannot flatten the hottest-address share for {branch_id} "
                                "without available padding addresses."
                            )
                        flatten_rounds = max(
                            1,
                            math.ceil(
                                (template.base_memory_operation_count * horizon_multiplier)
                                / padding_unique_count
                            ),
                        )
                    expected_padding_instruction_count = 2 * padding_unique_count * (
                        1 + flatten_rounds
                    )
                    wrapper_overhead = expected_padding_instruction_count + (
                        2 if checkpoint_depth == "plus_one" else 0
                    )
                    max_steps = (
                        math.ceil(template.base_max_steps * horizon_multiplier)
                        + wrapper_overhead
                        + 32
                    )
                    for seed_id in SEED_IDS:
                        padding_base_address = 20_000 + branch_counter * 32 + seed_id * 8
                        candidate_id = f"{branch_id}_seed{seed_id}"
                        branch_specs.append(
                            BranchSpec(
                                branch_id=branch_id,
                                candidate_id=candidate_id,
                                unique_address_target=template.unique_address_target,
                                horizon_multiplier=horizon_multiplier,
                                checkpoint_depth=checkpoint_depth,
                                hot_address_skew=hot_address_skew,
                                seed_id=seed_id,
                                family=template.family,
                                comparison_mode=template.comparison_mode,
                                base_program_name=template.base_program_name,
                                seed_variant=seed_variant_for_family(template.family, seed_id),
                                base_start=template.base_start,
                                scaled_start=scaled_start,
                                base_max_steps=template.base_max_steps,
                                max_steps=max_steps,
                                base_unique_address_count=template.base_unique_address_count,
                                padding_unique_count=padding_unique_count,
                                flatten_rounds=flatten_rounds,
                                padding_base_address=padding_base_address,
                                expected_padding_instruction_count=expected_padding_instruction_count,
                                target_wrapper_call_depth=1 if checkpoint_depth == "plus_one" else 0,
                            )
                        )
                    branch_counter += 1
    return branch_specs


def branch_spec_to_row(spec: BranchSpec) -> dict[str, object]:
    return {
        "branch_id": spec.branch_id,
        "candidate_id": spec.candidate_id,
        "unique_address_target": spec.unique_address_target,
        "horizon_multiplier": spec.horizon_multiplier,
        "checkpoint_depth": spec.checkpoint_depth,
        "hot_address_skew": spec.hot_address_skew,
        "seed_id": spec.seed_id,
        "family": spec.family,
        "comparison_mode": spec.comparison_mode,
        "base_program_name": spec.base_program_name,
        "seed_variant": spec.seed_variant,
        "base_start": spec.base_start,
        "scaled_start": spec.scaled_start,
        "base_max_steps": spec.base_max_steps,
        "max_steps": spec.max_steps,
        "base_unique_address_count": spec.base_unique_address_count,
        "padding_unique_count": spec.padding_unique_count,
        "flatten_rounds": spec.flatten_rounds,
        "padding_base_address": spec.padding_base_address,
        "expected_padding_instruction_count": spec.expected_padding_instruction_count,
        "target_wrapper_call_depth": spec.target_wrapper_call_depth,
    }


def materialize_base_program(spec: BranchSpec) -> BytecodeProgram:
    start = int(spec.scaled_start)
    if spec.family == "subroutine_braid":
        base_address = 96 if spec.seed_id == 0 else 112
        return subroutine_braid_program(start, base_address=base_address)
    if spec.family == "helper_checkpoint_braid":
        return helper_checkpoint_braid_program(start, base_address=280, selector_seed=spec.seed_id)
    if spec.family == "checkpoint_replay_long":
        base_address = 128 if spec.seed_id == 0 else 144
        return checkpoint_replay_long_program(start, base_address=base_address)
    raise ValueError(f"Unsupported R21 family: {spec.family}")


def rebase_instructions(
    instructions: tuple[BytecodeInstruction, ...],
    *,
    offset: int,
) -> tuple[BytecodeInstruction, ...]:
    rebased: list[BytecodeInstruction] = []
    for instruction in instructions:
        arg = instruction.arg
        if instruction.opcode in CONTROL_FLOW_OPCODES and arg is not None:
            arg += offset
        rebased.append(
            BytecodeInstruction(
                instruction.opcode,
                arg,
                in_types=instruction.in_types,
                out_types=instruction.out_types,
            )
        )
    return tuple(rebased)


def build_padding_instructions(
    *,
    padding_base_address: int,
    padding_unique_count: int,
    flatten_rounds: int,
    seed_id: int,
) -> tuple[BytecodeInstruction, ...]:
    instructions: list[BytecodeInstruction] = []
    if padding_unique_count == 0:
        return tuple(instructions)

    for index in range(padding_unique_count):
        address = padding_base_address + index
        instructions.append(BytecodeInstruction(BytecodeOpcode.CONST_I32, seed_id + index + 1))
        instructions.append(BytecodeInstruction(BytecodeOpcode.STORE_STATIC, address))

    for round_index in range(flatten_rounds):
        for index in range(padding_unique_count):
            address = padding_base_address + index
            instructions.append(
                BytecodeInstruction(
                    BytecodeOpcode.CONST_I32,
                    (round_index + 1) * (index + 2) + seed_id,
                )
            )
            instructions.append(BytecodeInstruction(BytecodeOpcode.STORE_STATIC, address))

    return tuple(instructions)


def build_wrapped_program(spec: BranchSpec, base_program: BytecodeProgram) -> BytecodeProgram:
    padding_instructions = build_padding_instructions(
        padding_base_address=spec.padding_base_address,
        padding_unique_count=spec.padding_unique_count,
        flatten_rounds=spec.flatten_rounds,
        seed_id=spec.seed_id,
    )
    if spec.checkpoint_depth == "baseline":
        wrapped_instructions = padding_instructions + rebase_instructions(
            base_program.instructions,
            offset=len(padding_instructions),
        )
    elif spec.checkpoint_depth == "plus_one":
        base_offset = 1
        subroutine_start = base_offset + len(base_program.instructions)
        wrapped_instructions = (
            BytecodeInstruction(BytecodeOpcode.CALL, subroutine_start),
        ) + rebase_instructions(base_program.instructions, offset=base_offset) + padding_instructions + (
            BytecodeInstruction(BytecodeOpcode.RET),
        )
    else:  # pragma: no cover
        raise RuntimeError(f"Unsupported checkpoint depth: {spec.checkpoint_depth}")

    return BytecodeProgram(
        instructions=wrapped_instructions,
        name=(
            f"{base_program.name}_r21_u{spec.unique_address_target}_"
            f"h{multiplier_label(spec.horizon_multiplier)}_"
            f"c{spec.checkpoint_depth}_k{spec.hot_address_skew}_seed{spec.seed_id}"
        ),
        memory_layout=base_program.memory_layout,
    )


def build_address_profile(events) -> dict[str, object]:
    operations = extract_memory_operations(events)
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
        else None
    )
    memory_operation_count = len(operations)
    hottest_address_share = (
        None
        if hottest_address_row is None or memory_operation_count == 0
        else int(hottest_address_row["total_ops"]) / memory_operation_count
    )
    return {
        "reference_step_count": max((event.step for event in events), default=-1) + 1,
        "memory_operation_count": memory_operation_count,
        "memory_load_count": load_count,
        "memory_store_count": store_count,
        "unique_address_count": len(address_rows),
        "hottest_address": None if hottest_address_row is None else hottest_address_row["address"],
        "hottest_address_loads": None if hottest_address_row is None else hottest_address_row["loads"],
        "hottest_address_stores": None if hottest_address_row is None else hottest_address_row["stores"],
        "hottest_address_share": hottest_address_share,
        "address_rows": address_rows,
    }


def failure_class_for_row(*, failure_reason: str | None, exact: bool) -> str | None:
    if exact:
        return None
    if failure_reason is None:
        return "exactness_mismatch"
    if "Maximum step budget exceeded" in failure_reason:
        return "step_budget_exhausted"
    return "exactness_mismatch"


def measure_branch_spec(spec: BranchSpec) -> tuple[dict[str, object], dict[str, object]]:
    base_program = materialize_base_program(spec)
    wrapped_program = build_wrapped_program(spec, base_program)
    lowered_program = lower_program(wrapped_program)
    reference = TraceInterpreter().run(lowered_program, max_steps=spec.max_steps)
    reference_profile = build_address_profile(reference.events)
    observed_unique_address_count = int(reference_profile["unique_address_count"])
    if observed_unique_address_count != spec.unique_address_target:
        raise RuntimeError(
            f"R21 expected observed unique_address_count {spec.unique_address_target} for "
            f"{spec.candidate_id}, found {observed_unique_address_count}."
        )

    executor = FreeRunningTraceExecutor(
        stack_strategy="pointer_like_exact",
        memory_strategy="pointer_like_exact",
        validate_exact_reads=False,
    )
    runtime_seconds = 0.0
    execution = None
    failure_reason: str | None = None
    exact_trace_match = False
    exact_final_state_match = False
    first_mismatch_step = None

    try:
        start_time = time.perf_counter()
        execution = executor.run(lowered_program, max_steps=spec.max_steps)
        runtime_seconds = time.perf_counter() - start_time
        outcome = compare_execution_to_reference(
            lowered_program,
            execution,
            reference=FreeRunningExecutionResult(
                program=lowered_program,
                events=reference.events,
                final_state=reference.final_state,
                read_observations=(),
                stack_strategy="linear",
                memory_strategy="linear",
            ),
        )
        exact_trace_match = bool(outcome.exact_trace_match)
        exact_final_state_match = bool(outcome.exact_final_state_match)
        first_mismatch_step = outcome.first_mismatch_step
        if not exact_trace_match or not exact_final_state_match:
            failure_reason = "trace_or_state_mismatch"
    except Exception as exc:  # pragma: no cover
        runtime_seconds = time.perf_counter() - start_time
        failure_reason = f"{type(exc).__name__}: {exc}"

    exact = failure_reason is None and exact_trace_match and exact_final_state_match
    read_observations = () if execution is None else execution.read_observations
    read_observation_count = len(read_observations)
    memory_read_count = sum(observation.space == "memory" for observation in read_observations)
    stack_read_count = sum(observation.space == "stack" for observation in read_observations)
    failure_class = failure_class_for_row(failure_reason=failure_reason, exact=exact)
    failure_axis_tags = format_axis_tags(
        unique_address_target=spec.unique_address_target,
        checkpoint_depth=spec.checkpoint_depth,
        hot_address_skew=spec.hot_address_skew,
        hottest_address_share=reference_profile["hottest_address_share"],
    )

    row = {
        **branch_spec_to_row(spec),
        "source_runtime_stage": "r20_d0_runtime_mechanism_ablation_matrix",
        "base_runtime_stage": "r19_d0_pointer_like_surface_generalization_gate",
        "program_name": lowered_program.name,
        "base_variant_program_name": base_program.name,
        "runtime_seconds": runtime_seconds,
        "ns_per_step": (
            None
            if reference_profile["reference_step_count"] in {None, 0}
            else (runtime_seconds / int(reference_profile["reference_step_count"])) * 1e9
        ),
        "exact_trace_match": exact_trace_match,
        "exact_final_state_match": exact_final_state_match,
        "first_mismatch_step": first_mismatch_step,
        "failure_reason": failure_reason,
        "failure_class": failure_class,
        "exact": exact,
        "read_observation_count": read_observation_count,
        "memory_read_count": memory_read_count,
        "stack_read_count": stack_read_count,
        "reference_step_count": reference_profile["reference_step_count"],
        "memory_operation_count": reference_profile["memory_operation_count"],
        "memory_load_count": reference_profile["memory_load_count"],
        "memory_store_count": reference_profile["memory_store_count"],
        "unique_address_count": observed_unique_address_count,
        "hottest_address": reference_profile["hottest_address"],
        "hottest_address_share": reference_profile["hottest_address_share"],
        "failure_axis_tags": failure_axis_tags,
    }
    profile = {
        **branch_spec_to_row(spec),
        "program_name": lowered_program.name,
        **reference_profile,
    }
    return row, profile


def execute_boundary_scan(
    branch_specs: list[BranchSpec],
) -> tuple[list[dict[str, object]], list[dict[str, object]], int]:
    rows: list[dict[str, object]] = []
    profiles: list[dict[str, object]] = []
    failures_by_branch: dict[str, int] = defaultdict(int)
    skipped_count = 0
    for spec in branch_specs:
        if failures_by_branch[spec.branch_id] >= FAILURE_LIMIT_PER_BRANCH:
            skipped_count += 1
            continue
        row, profile = measure_branch_spec(spec)
        rows.append(row)
        profiles.append(profile)
        if not bool(row["exact"]):
            failures_by_branch[spec.branch_id] += 1
    return rows, profiles, skipped_count


def build_branch_summary(
    branch_specs: list[BranchSpec],
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows_by_branch: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        rows_by_branch[str(row["branch_id"])].append(row)

    summary_rows: list[dict[str, object]] = []
    branch_templates = {spec.branch_id: spec for spec in branch_specs}
    for branch_id in sorted({spec.branch_id for spec in branch_specs}):
        branch_rows = sorted(rows_by_branch.get(branch_id, []), key=lambda row: int(row["seed_id"]))
        exact_rows = [row for row in branch_rows if bool(row["exact"])]
        failure_rows = [row for row in branch_rows if not bool(row["exact"])]
        first_fail = failure_rows[0] if failure_rows else None
        template = branch_templates[branch_id]
        if not failure_rows:
            branch_verdict = "all_exact"
        elif not exact_rows:
            branch_verdict = "all_failed"
        else:
            branch_verdict = "mixed"
        summary_rows.append(
            {
                "branch_id": branch_id,
                "unique_address_target": template.unique_address_target,
                "horizon_multiplier": template.horizon_multiplier,
                "checkpoint_depth": template.checkpoint_depth,
                "hot_address_skew": template.hot_address_skew,
                "planned_candidate_count": sum(spec.branch_id == branch_id for spec in branch_specs),
                "executed_candidate_count": len(branch_rows),
                "exact_candidate_count": len(exact_rows),
                "failure_candidate_count": len(failure_rows),
                "first_fail_candidate_id": None if first_fail is None else first_fail["candidate_id"],
                "first_fail_program_name": None if first_fail is None else first_fail["program_name"],
                "first_fail_step": None if first_fail is None else first_fail["first_mismatch_step"],
                "first_fail_reason": None if first_fail is None else first_fail["failure_reason"],
                "median_hottest_address_share": median_or_none(
                    row["hottest_address_share"] for row in branch_rows
                ),
                "branch_verdict": branch_verdict,
            }
        )
    return summary_rows


def build_first_fail_digest(branch_summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    digest_rows: list[dict[str, object]] = []
    for row in branch_summary_rows:
        if row["first_fail_candidate_id"] is None:
            continue
        digest_rows.append(
            {
                "branch_id": row["branch_id"],
                "unique_address_target": row["unique_address_target"],
                "horizon_multiplier": row["horizon_multiplier"],
                "checkpoint_depth": row["checkpoint_depth"],
                "hot_address_skew": row["hot_address_skew"],
                "first_fail_candidate_id": row["first_fail_candidate_id"],
                "first_fail_program_name": row["first_fail_program_name"],
                "first_fail_step": row["first_fail_step"],
                "first_fail_reason": row["first_fail_reason"],
            }
        )
    return digest_rows


def assess_boundary_gate(
    branch_specs: list[BranchSpec],
    rows: list[dict[str, object]],
    branch_summary_rows: list[dict[str, object]],
    *,
    skipped_count: int,
) -> dict[str, object]:
    exact_candidate_count = sum(bool(row["exact"]) for row in rows)
    failure_candidate_count = sum(not bool(row["exact"]) for row in rows)
    if failure_candidate_count == 0:
        lane_verdict = "no_boundary_break_detected"
        reason = "Every executed bounded R21 candidate stayed exact on the current D0 endpoint."
    elif exact_candidate_count == 0:
        lane_verdict = "boundary_break_detected"
        reason = "Every executed bounded R21 candidate failed, so the current exact executor breaks across the scanned packet."
    else:
        lane_verdict = "mixed_boundary_detected"
        reason = "The bounded R21 grid preserved many exact rows but now includes explicit failing candidates."

    return {
        "lane_verdict": lane_verdict,
        "reason": reason,
        "planned_branch_count": len({spec.branch_id for spec in branch_specs}),
        "planned_candidate_count": len(branch_specs),
        "executed_candidate_count": len(rows),
        "skipped_candidate_count": skipped_count,
        "exact_candidate_count": exact_candidate_count,
        "failure_candidate_count": failure_candidate_count,
        "failure_branch_count": sum(int(row["failure_candidate_count"]) > 0 for row in branch_summary_rows),
        "next_priority_lane": "h19_refreeze_and_next_scope_decision",
    }


def build_summary(
    branch_specs: list[BranchSpec],
    rows: list[dict[str, object]],
    branch_summary_rows: list[dict[str, object]],
    gate: dict[str, object],
) -> dict[str, object]:
    return {
        "status": "r21_boundary_map_complete",
        "current_frozen_stage": "h17_refreeze_and_conditional_frontier_recheck",
        "source_runtime_stage": "r20_d0_runtime_mechanism_ablation_matrix",
        "gate": gate,
        "planned_unique_address_targets": list(UNIQUE_ADDRESS_TARGETS),
        "planned_horizon_multipliers": list(HORIZON_MULTIPLIERS),
        "planned_checkpoint_depths": list(CHECKPOINT_DEPTHS),
        "planned_hot_address_skews": list(HOT_ADDRESS_SKEWS),
        "executed_family_count": len({str(row["family"]) for row in rows}),
        "recommended_next_action": (
            "Advance to H19 to refreeze R19-R21 into one machine-readable same-endpoint state."
        ),
        "supported_here": [
            "R21 stayed on the current D0 endpoint and kept the exact-executor scan exporter-local.",
            "Both positive and negative rows are preserved when failures occur.",
        ],
        "unsupported_here": [
            "R21 does not authorize a wider endpoint, frontend surface, or repair loop.",
            "R21 remains a bounded boundary map rather than a general runtime replacement claim.",
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    admitted_rows = load_r19_admitted_runtime_rows()
    templates = build_template_registry(admitted_rows)
    branch_specs = build_branch_specs(templates)
    manifest_rows = [branch_spec_to_row(spec) for spec in branch_specs]
    rows, profiles, skipped_count = execute_boundary_scan(branch_specs)
    branch_summary_rows = build_branch_summary(branch_specs, rows)
    failure_rows = [row for row in rows if not bool(row["exact"])]
    first_fail_digest_rows = build_first_fail_digest(branch_summary_rows)
    gate = assess_boundary_gate(
        branch_specs,
        rows,
        branch_summary_rows,
        skipped_count=skipped_count,
    )
    summary = build_summary(branch_specs, rows, branch_summary_rows, gate)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "branch_manifest.json",
        {"experiment": "r21_branch_manifest", "environment": environment.as_dict(), "rows": manifest_rows},
    )
    write_csv(OUT_DIR / "branch_manifest.csv", manifest_rows)
    write_json(
        OUT_DIR / "boundary_rows.json",
        {"experiment": "r21_boundary_rows", "environment": environment.as_dict(), "rows": rows},
    )
    write_csv(OUT_DIR / "boundary_rows.csv", rows)
    write_json(
        OUT_DIR / "address_profiles.json",
        {"experiment": "r21_address_profiles", "environment": environment.as_dict(), "rows": profiles},
    )
    write_json(
        OUT_DIR / "positive_rows.json",
        {
            "experiment": "r21_positive_rows",
            "environment": environment.as_dict(),
            "rows": [row for row in rows if bool(row["exact"])],
        },
    )
    write_json(
        OUT_DIR / "failure_rows.json",
        {"experiment": "r21_failure_rows", "environment": environment.as_dict(), "rows": failure_rows},
    )
    write_json(
        OUT_DIR / "branch_summary.json",
        {"experiment": "r21_branch_summary", "environment": environment.as_dict(), "rows": branch_summary_rows},
    )
    write_json(
        OUT_DIR / "first_fail_digest.json",
        {
            "experiment": "r21_first_fail_digest",
            "environment": environment.as_dict(),
            "rows": first_fail_digest_rows,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r21_d0_exact_executor_boundary_break_map",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/R19_d0_pointer_like_surface_generalization_gate/runtime_rows.json",
                "results/R20_d0_runtime_mechanism_ablation_matrix/summary.json",
                "docs/plans/2026-03-21-h18-unattended-mainline-master-plan.md",
                "tmp/active_wave_plan.md",
                "src/model/free_running_executor.py",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# R21 D0 Exact Executor Boundary Break Map\n\n"
        "Bounded exact-executor boundary scan on the current D0 endpoint.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `branch_manifest.json`\n"
        "- `branch_manifest.csv`\n"
        "- `boundary_rows.json`\n"
        "- `boundary_rows.csv`\n"
        "- `address_profiles.json`\n"
        "- `positive_rows.json`\n"
        "- `failure_rows.json`\n"
        "- `branch_summary.json`\n"
        "- `first_fail_digest.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
