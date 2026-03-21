"""Export the extended same-endpoint boundary-localization gate for R22."""

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
    helper_checkpoint_braid_long_program,
    helper_checkpoint_braid_program,
    lower_program,
    subroutine_braid_long_program,
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
R21_OUT_DIR = ROOT / "results" / "R21_d0_exact_executor_boundary_break_map"
OUT_DIR = ROOT / "results" / "R22_d0_true_boundary_localization_gate"

FAILURE_LIMIT_PER_BRANCH = 2
MAX_REFERENCE_STEP_LIMIT = 40_000
SEED_IDS = (0, 1)
FIRST_FAIL_RECHECK_REPEATS = 2
HOT_ADDRESS_SKEWS = ("baseline", "flattened")
EXTENDED_HORIZON_MULTIPLIERS = (2.5, 3.0)
EXTENDED_CHECKPOINT_DEPTHS = ("plus_one", "plus_two")
CHECKPOINT_DEPTH_TO_CALL_DEPTH = {"baseline": 0, "plus_one": 1, "plus_two": 2}
CHECKPOINT_DEPTH_ORDER = ("baseline", "plus_one", "plus_two")
HOT_ADDRESS_SKEW_ORDER = ("baseline", "flattened")
CONTROL_FLOW_OPCODES = {
    BytecodeOpcode.JMP,
    BytecodeOpcode.JZ_ZERO,
    BytecodeOpcode.CALL,
}
TARGET_FAMILIES = (
    "subroutine_braid",
    "helper_checkpoint_braid",
    "subroutine_braid_long",
    "helper_checkpoint_braid_long",
    "checkpoint_replay_long",
)
ANCHOR_BRANCH_PLANS = (
    ("continuity_anchor", "subroutine_braid", 6, 2.0, "plus_one", "flattened"),
    ("continuity_anchor", "helper_checkpoint_braid", 8, 2.0, "plus_one", "flattened"),
    ("continuity_anchor", "checkpoint_replay_long", 16, 2.0, "plus_one", "flattened"),
)
EXTENDED_UNIQUE_TARGETS_BY_FAMILY = {
    "subroutine_braid_long": (12, 20),
    "helper_checkpoint_braid_long": (12, 20),
    "checkpoint_replay_long": (24, 32),
}


@dataclass(frozen=True, slots=True)
class TemplateConfig:
    family: str
    comparison_mode: str
    base_program_name: str
    base_start: int
    base_max_steps: int
    base_reference_step_count: int
    base_unique_address_count: int
    base_memory_operation_count: int


@dataclass(frozen=True, slots=True)
class BranchPlan:
    lane_class: str
    family: str
    unique_address_target: int
    horizon_multiplier: float
    checkpoint_depth: str
    hot_address_skew: str


@dataclass(frozen=True, slots=True)
class BranchSpec:
    branch_id: str
    candidate_id: str
    lane_class: str
    family: str
    comparison_mode: str
    base_program_name: str
    seed_variant: str
    unique_address_target: int
    horizon_multiplier: float
    checkpoint_depth: str
    hot_address_skew: str
    seed_id: int
    base_start: int
    scaled_start: int
    base_max_steps: int
    max_steps: int
    base_reference_step_count: int
    expected_reference_step_count: int
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


def median_or_none(values: Iterable[float | None]) -> float | None:
    filtered = [value for value in values if value is not None]
    return median(filtered) if filtered else None


def multiplier_label(multiplier: float) -> str:
    return f"{multiplier:.1f}".replace(".", "p")


def format_axis_tags(
    *,
    family: str,
    unique_address_target: int,
    checkpoint_depth: str,
    hot_address_skew: str,
    hottest_address_share: float | None,
) -> str:
    tags: list[str] = []
    if family.endswith("_long"):
        tags.append("long_family")
    if unique_address_target >= 20:
        tags.append("high_unique_address_target")
    if checkpoint_depth == "plus_two":
        tags.append("plus_two_checkpoint_depth")
    elif checkpoint_depth == "plus_one":
        tags.append("plus_one_checkpoint_depth")
    if hot_address_skew == "flattened":
        tags.append("flattened_hot_address_target")
    if hottest_address_share is not None and hottest_address_share < 0.20:
        tags.append("low_hottest_address_share_observed")
    return ",".join(tags)


def load_r19_admitted_runtime_rows() -> dict[str, dict[str, Any]]:
    payload = read_json(R19_OUT_DIR / "runtime_rows.json")
    admitted_rows = [row for row in payload["rows"] if row["cohort"] == "admitted"]
    by_family = {str(row["family"]): row for row in admitted_rows}
    missing_families = sorted(set(TARGET_FAMILIES) - set(by_family))
    if missing_families:
        raise RuntimeError(f"R22 missing admitted R19 anchors for families: {missing_families}.")
    return {family: by_family[family] for family in TARGET_FAMILIES}


def build_template_registry(
    admitted_rows_by_family: dict[str, dict[str, Any]],
) -> dict[str, TemplateConfig]:
    registry: dict[str, TemplateConfig] = {}
    for family, row in admitted_rows_by_family.items():
        registry[family] = TemplateConfig(
            family=family,
            comparison_mode=str(row["comparison_mode"]),
            base_program_name=str(row["program_name"]),
            base_start=int(row["scaled_start"]),
            base_max_steps=int(row["max_steps"]),
            base_reference_step_count=int(row["reference_step_count"]),
            base_unique_address_count=int(row["unique_address_count"]),
            base_memory_operation_count=int(row["memory_operation_count"]),
        )
    return registry


def build_branch_plans() -> list[BranchPlan]:
    plans = [BranchPlan(*plan) for plan in ANCHOR_BRANCH_PLANS]
    for family in ("subroutine_braid_long", "helper_checkpoint_braid_long", "checkpoint_replay_long"):
        for unique_address_target in EXTENDED_UNIQUE_TARGETS_BY_FAMILY[family]:
            for horizon_multiplier in EXTENDED_HORIZON_MULTIPLIERS:
                for checkpoint_depth in EXTENDED_CHECKPOINT_DEPTHS:
                    for hot_address_skew in HOT_ADDRESS_SKEWS:
                        plans.append(
                            BranchPlan(
                                lane_class="extended_probe",
                                family=family,
                                unique_address_target=unique_address_target,
                                horizon_multiplier=horizon_multiplier,
                                checkpoint_depth=checkpoint_depth,
                                hot_address_skew=hot_address_skew,
                            )
                        )
    return plans


def seed_variant_for_family(family: str, seed_id: int) -> str:
    if family.startswith("helper_checkpoint_braid"):
        return "r19_admitted_seed_anchor" if seed_id == 0 else "r19_heldout_seed_anchor"
    if family in {
        "subroutine_braid",
        "subroutine_braid_long",
        "checkpoint_replay_long",
    }:
        return "r19_admitted_address_anchor" if seed_id == 0 else "r19_heldout_address_anchor"
    raise ValueError(f"Unsupported R22 family for seed variant lookup: {family}")


def build_branch_specs(
    template_registry: dict[str, TemplateConfig],
    branch_plans: list[BranchPlan],
) -> list[BranchSpec]:
    branch_specs: list[BranchSpec] = []
    for branch_index, plan in enumerate(branch_plans):
        template = template_registry[plan.family]
        padding_unique_count = plan.unique_address_target - template.base_unique_address_count
        if padding_unique_count < 0:
            raise RuntimeError(
                f"R22 target {plan.unique_address_target} is below the base unique count "
                f"{template.base_unique_address_count} for {plan.family}."
            )
        flatten_rounds = 0
        if plan.hot_address_skew == "flattened":
            if padding_unique_count == 0:
                raise RuntimeError(
                    f"R22 cannot flatten the hottest-address share for {plan.family} "
                    f"without available padding addresses."
                )
            flatten_rounds = max(
                1,
                math.ceil(
                    (template.base_memory_operation_count * plan.horizon_multiplier)
                    / padding_unique_count
                ),
            )
        expected_padding_instruction_count = 2 * padding_unique_count * (1 + flatten_rounds)
        call_depth = CHECKPOINT_DEPTH_TO_CALL_DEPTH[plan.checkpoint_depth]
        scaled_start = max(1, int(round(template.base_start * plan.horizon_multiplier)))
        branch_id = (
            f"{plan.lane_class}_{plan.family}_u{plan.unique_address_target}_"
            f"h{multiplier_label(plan.horizon_multiplier)}_"
            f"c{plan.checkpoint_depth}_k{plan.hot_address_skew}"
        )
        expected_reference_step_count = (
            math.ceil(template.base_reference_step_count * plan.horizon_multiplier)
            + expected_padding_instruction_count
            + call_depth
        )
        max_steps = (
            math.ceil(template.base_max_steps * plan.horizon_multiplier)
            + expected_padding_instruction_count
            + call_depth
            + 64
        )
        for seed_id in SEED_IDS:
            branch_specs.append(
                BranchSpec(
                    branch_id=branch_id,
                    candidate_id=f"{branch_id}_seed{seed_id}",
                    lane_class=plan.lane_class,
                    family=plan.family,
                    comparison_mode=template.comparison_mode,
                    base_program_name=template.base_program_name,
                    seed_variant=seed_variant_for_family(plan.family, seed_id),
                    unique_address_target=plan.unique_address_target,
                    horizon_multiplier=plan.horizon_multiplier,
                    checkpoint_depth=plan.checkpoint_depth,
                    hot_address_skew=plan.hot_address_skew,
                    seed_id=seed_id,
                    base_start=template.base_start,
                    scaled_start=scaled_start,
                    base_max_steps=template.base_max_steps,
                    max_steps=max_steps,
                    base_reference_step_count=template.base_reference_step_count,
                    expected_reference_step_count=expected_reference_step_count,
                    base_unique_address_count=template.base_unique_address_count,
                    padding_unique_count=padding_unique_count,
                    flatten_rounds=flatten_rounds,
                    padding_base_address=40_000 + branch_index * 64 + seed_id * 16,
                    expected_padding_instruction_count=expected_padding_instruction_count,
                    target_wrapper_call_depth=call_depth,
                )
            )
    return branch_specs


def branch_spec_to_row(spec: BranchSpec) -> dict[str, object]:
    return {
        "branch_id": spec.branch_id,
        "candidate_id": spec.candidate_id,
        "lane_class": spec.lane_class,
        "family": spec.family,
        "comparison_mode": spec.comparison_mode,
        "base_program_name": spec.base_program_name,
        "seed_variant": spec.seed_variant,
        "unique_address_target": spec.unique_address_target,
        "horizon_multiplier": spec.horizon_multiplier,
        "checkpoint_depth": spec.checkpoint_depth,
        "hot_address_skew": spec.hot_address_skew,
        "seed_id": spec.seed_id,
        "base_start": spec.base_start,
        "scaled_start": spec.scaled_start,
        "base_max_steps": spec.base_max_steps,
        "max_steps": spec.max_steps,
        "base_reference_step_count": spec.base_reference_step_count,
        "expected_reference_step_count": spec.expected_reference_step_count,
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
    if spec.family == "subroutine_braid_long":
        base_address = 176 if spec.seed_id == 0 else 208
        return subroutine_braid_long_program(start, base_address=base_address)
    if spec.family == "helper_checkpoint_braid":
        return helper_checkpoint_braid_program(start, base_address=280, selector_seed=spec.seed_id)
    if spec.family == "helper_checkpoint_braid_long":
        return helper_checkpoint_braid_long_program(
            start,
            base_address=312,
            selector_seed=spec.seed_id,
        )
    if spec.family == "checkpoint_replay_long":
        base_address = 128 if spec.seed_id == 0 else 144
        return checkpoint_replay_long_program(start, base_address=base_address)
    raise ValueError(f"Unsupported R22 family: {spec.family}")


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


def build_nested_checkpoint_subroutine(
    body_instructions: tuple[BytecodeInstruction, ...],
    *,
    call_depth: int,
) -> tuple[BytecodeInstruction, ...]:
    if call_depth <= 0:
        raise ValueError("R22 nested checkpoint subroutine requires positive call depth.")
    subroutine = body_instructions + (BytecodeInstruction(BytecodeOpcode.RET),)
    for _ in range(call_depth - 1):
        subroutine = (
            BytecodeInstruction(BytecodeOpcode.CALL, 2),
            BytecodeInstruction(BytecodeOpcode.RET),
        ) + rebase_instructions(subroutine, offset=2)
    return subroutine


def build_wrapped_program(spec: BranchSpec, base_program: BytecodeProgram) -> BytecodeProgram:
    padding_instructions = build_padding_instructions(
        padding_base_address=spec.padding_base_address,
        padding_unique_count=spec.padding_unique_count,
        flatten_rounds=spec.flatten_rounds,
        seed_id=spec.seed_id,
    )
    base_instructions = rebase_instructions(base_program.instructions, offset=len(padding_instructions))
    body_instructions = padding_instructions + base_instructions
    if spec.target_wrapper_call_depth == 0:
        wrapped_instructions = body_instructions
    else:
        subroutine = build_nested_checkpoint_subroutine(
            body_instructions,
            call_depth=spec.target_wrapper_call_depth,
        )
        wrapped_instructions = (
            BytecodeInstruction(BytecodeOpcode.CALL, 2),
            BytecodeInstruction(BytecodeOpcode.HALT),
        ) + rebase_instructions(subroutine, offset=2)

    return BytecodeProgram(
        instructions=wrapped_instructions,
        name=(
            f"{base_program.name}_r22_u{spec.unique_address_target}_"
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
            f"R22 expected observed unique_address_count {spec.unique_address_target} for "
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
        family=spec.family,
        unique_address_target=spec.unique_address_target,
        checkpoint_depth=spec.checkpoint_depth,
        hot_address_skew=spec.hot_address_skew,
        hottest_address_share=reference_profile["hottest_address_share"],
    )

    row = {
        **branch_spec_to_row(spec),
        "source_runtime_stage": "r21_d0_exact_executor_boundary_break_map",
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
) -> tuple[list[dict[str, object]], list[dict[str, object]], int, list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    profiles: list[dict[str, object]] = []
    skipped_rows: list[dict[str, object]] = []
    failures_by_branch: dict[str, int] = defaultdict(int)
    pruned_count = 0
    for spec in branch_specs:
        if spec.expected_reference_step_count > MAX_REFERENCE_STEP_LIMIT:
            skipped_rows.append(
                {
                    **branch_spec_to_row(spec),
                    "skip_class": "resource_limit",
                    "skip_reason": "expected_reference_step_limit_exceeded",
                }
            )
            continue
        if failures_by_branch[spec.branch_id] >= FAILURE_LIMIT_PER_BRANCH:
            pruned_count += 1
            continue
        row, profile = measure_branch_spec(spec)
        rows.append(row)
        profiles.append(profile)
        if not bool(row["exact"]):
            failures_by_branch[spec.branch_id] += 1
    return rows, profiles, pruned_count, skipped_rows


def build_branch_summary(
    branch_specs: list[BranchSpec],
    rows: list[dict[str, object]],
    skipped_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows_by_branch: dict[str, list[dict[str, object]]] = defaultdict(list)
    skips_by_branch: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        rows_by_branch[str(row["branch_id"])].append(row)
    for row in skipped_rows:
        skips_by_branch[str(row["branch_id"])].append(row)

    summary_rows: list[dict[str, object]] = []
    branch_templates = {spec.branch_id: spec for spec in branch_specs}
    for branch_id in sorted({spec.branch_id for spec in branch_specs}):
        branch_rows = sorted(rows_by_branch.get(branch_id, []), key=lambda row: int(row["seed_id"]))
        branch_skips = sorted(skips_by_branch.get(branch_id, []), key=lambda row: int(row["seed_id"]))
        exact_rows = [row for row in branch_rows if bool(row["exact"])]
        failure_rows = [row for row in branch_rows if not bool(row["exact"])]
        first_fail = failure_rows[0] if failure_rows else None
        template = branch_templates[branch_id]
        if branch_skips and not branch_rows:
            branch_verdict = "resource_limited"
        elif not failure_rows:
            branch_verdict = "all_exact"
        elif not exact_rows:
            branch_verdict = "all_failed"
        else:
            branch_verdict = "mixed"
        summary_rows.append(
            {
                "branch_id": branch_id,
                "lane_class": template.lane_class,
                "family": template.family,
                "unique_address_target": template.unique_address_target,
                "horizon_multiplier": template.horizon_multiplier,
                "checkpoint_depth": template.checkpoint_depth,
                "hot_address_skew": template.hot_address_skew,
                "target_wrapper_call_depth": template.target_wrapper_call_depth,
                "planned_candidate_count": sum(spec.branch_id == branch_id for spec in branch_specs),
                "executed_candidate_count": len(branch_rows),
                "resource_skipped_candidate_count": len(branch_skips),
                "exact_candidate_count": len(exact_rows),
                "failure_candidate_count": len(failure_rows),
                "first_fail_candidate_id": None if first_fail is None else first_fail["candidate_id"],
                "first_fail_program_name": None if first_fail is None else first_fail["program_name"],
                "first_fail_step": None if first_fail is None else first_fail["first_mismatch_step"],
                "first_fail_reason": None if first_fail is None else first_fail["failure_reason"],
                "first_fail_failure_class": None if first_fail is None else first_fail["failure_class"],
                "median_hottest_address_share": median_or_none(
                    row["hottest_address_share"] for row in branch_rows
                ),
                "branch_verdict": branch_verdict,
            }
        )
    return summary_rows


def build_first_fail_digest(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        if bool(row["exact"]):
            continue
        return [
            {
                "branch_id": row["branch_id"],
                "candidate_id": row["candidate_id"],
                "lane_class": row["lane_class"],
                "family": row["family"],
                "unique_address_target": row["unique_address_target"],
                "horizon_multiplier": row["horizon_multiplier"],
                "checkpoint_depth": row["checkpoint_depth"],
                "hot_address_skew": row["hot_address_skew"],
                "target_wrapper_call_depth": row["target_wrapper_call_depth"],
                "program_name": row["program_name"],
                "first_mismatch_step": row["first_mismatch_step"],
                "failure_reason": row["failure_reason"],
                "failure_class": row["failure_class"],
            }
        ]
    return []


def _is_exact_branch(row: dict[str, object]) -> bool:
    return (
        int(row["executed_candidate_count"]) > 0
        and int(row["failure_candidate_count"]) == 0
        and int(row["resource_skipped_candidate_count"]) == 0
    )


def build_localized_boundary(
    first_fail_digest_rows: list[dict[str, object]],
    branch_summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    if not first_fail_digest_rows:
        return []

    first_fail = first_fail_digest_rows[0]
    summary_by_key = {
        (
            str(row["family"]),
            int(row["unique_address_target"]),
            float(row["horizon_multiplier"]),
            str(row["checkpoint_depth"]),
            str(row["hot_address_skew"]),
        ): row
        for row in branch_summary_rows
    }
    family = str(first_fail["family"])
    unique_address_target = int(first_fail["unique_address_target"])
    horizon_multiplier = float(first_fail["horizon_multiplier"])
    checkpoint_depth = str(first_fail["checkpoint_depth"])
    hot_address_skew = str(first_fail["hot_address_skew"])

    family_targets = sorted(
        {
            int(row["unique_address_target"])
            for row in branch_summary_rows
            if str(row["family"]) == family
        }
    )
    family_horizons = sorted(
        {
            float(row["horizon_multiplier"])
            for row in branch_summary_rows
            if str(row["family"]) == family
        }
    )

    def previous_value(values: tuple[str, ...] | list[int] | list[float], current):
        current_index = list(values).index(current)
        if current_index == 0:
            return None
        return list(values)[current_index - 1]

    neighbors: list[dict[str, object]] = []
    candidate_keys = [
        (
            "unique_address_target",
            (
                family,
                previous_value(family_targets, unique_address_target),
                horizon_multiplier,
                checkpoint_depth,
                hot_address_skew,
            ),
        ),
        (
            "horizon_multiplier",
            (
                family,
                unique_address_target,
                previous_value(family_horizons, horizon_multiplier),
                checkpoint_depth,
                hot_address_skew,
            ),
        ),
        (
            "checkpoint_depth",
            (
                family,
                unique_address_target,
                horizon_multiplier,
                previous_value(CHECKPOINT_DEPTH_ORDER, checkpoint_depth),
                hot_address_skew,
            ),
        ),
        (
            "hot_address_skew",
            (
                family,
                unique_address_target,
                horizon_multiplier,
                checkpoint_depth,
                previous_value(HOT_ADDRESS_SKEW_ORDER, hot_address_skew),
            ),
        ),
    ]
    for axis_name, key in candidate_keys:
        if None in key:
            continue
        neighbor_row = summary_by_key.get(key)
        if neighbor_row is None or not _is_exact_branch(neighbor_row):
            continue
        neighbors.append(
            {
                "axis_name": axis_name,
                "branch_id": neighbor_row["branch_id"],
                "candidate_basis": list(key),
                "exact_candidate_count": neighbor_row["exact_candidate_count"],
                "planned_candidate_count": neighbor_row["planned_candidate_count"],
            }
        )

    return [
        {
            **first_fail,
            "supporting_exact_neighbor_count": len(neighbors),
            "supporting_exact_neighbors": neighbors,
        }
    ]


def build_failure_rechecks(
    spec_lookup: dict[str, BranchSpec],
    first_fail_digest_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    if not first_fail_digest_rows:
        return []
    first_fail = first_fail_digest_rows[0]
    spec = spec_lookup[str(first_fail["candidate_id"])]
    rows: list[dict[str, object]] = []
    for recheck_index in range(FIRST_FAIL_RECHECK_REPEATS):
        row, _profile = measure_branch_spec(spec)
        reproduced = (
            not bool(row["exact"])
            and row["first_mismatch_step"] == first_fail["first_mismatch_step"]
            and row["failure_class"] == first_fail["failure_class"]
            and row["failure_reason"] == first_fail["failure_reason"]
        )
        rows.append(
            {
                "candidate_id": spec.candidate_id,
                "recheck_index": recheck_index,
                "exact": row["exact"],
                "first_mismatch_step": row["first_mismatch_step"],
                "failure_reason": row["failure_reason"],
                "failure_class": row["failure_class"],
                "runtime_seconds": row["runtime_seconds"],
                "reproduced": reproduced,
            }
        )
    return rows


def assess_boundary_gate(
    branch_specs: list[BranchSpec],
    rows: list[dict[str, object]],
    branch_summary_rows: list[dict[str, object]],
    *,
    pruned_count: int,
    skipped_rows: list[dict[str, object]],
    first_fail_digest_rows: list[dict[str, object]],
    localized_boundary_rows: list[dict[str, object]],
    failure_rechecks: list[dict[str, object]],
) -> dict[str, object]:
    if first_fail_digest_rows and failure_rechecks and not all(
        bool(row["reproduced"]) for row in failure_rechecks
    ):
        raise RuntimeError("R22 found a failing candidate but could not reproduce it during recheck.")

    exact_candidate_count = sum(bool(row["exact"]) for row in rows)
    failure_candidate_count = sum(not bool(row["exact"]) for row in rows)
    continuity_anchor_rows = [row for row in rows if row["lane_class"] == "continuity_anchor"]
    extended_probe_rows = [row for row in rows if row["lane_class"] == "extended_probe"]
    first_fail = first_fail_digest_rows[0] if first_fail_digest_rows else None
    localized_boundary = localized_boundary_rows[0] if localized_boundary_rows else None

    if first_fail is not None:
        lane_verdict = "first_boundary_failure_localized"
        reason = (
            "R22 found a reproducible first failing candidate inside the extended same-endpoint grid."
        )
    elif skipped_rows:
        lane_verdict = "resource_limited_without_failure"
        reason = "R22 did not find a failure before hitting the planned bounded step cap."
    else:
        lane_verdict = "no_failure_in_extended_grid"
        reason = (
            "Every executed R22 candidate stayed exact inside the harder same-endpoint boundary grid."
        )

    return {
        "lane_verdict": lane_verdict,
        "reason": reason,
        "planned_branch_count": len({spec.branch_id for spec in branch_specs}),
        "planned_candidate_count": len(branch_specs),
        "executed_candidate_count": len(rows),
        "resource_skipped_candidate_count": len(skipped_rows),
        "pruned_candidate_count": pruned_count,
        "exact_candidate_count": exact_candidate_count,
        "failure_candidate_count": failure_candidate_count,
        "failure_branch_count": sum(
            int(row["failure_candidate_count"]) > 0 for row in branch_summary_rows
        ),
        "continuity_anchor_candidate_count": len(continuity_anchor_rows),
        "continuity_anchor_exact_count": sum(bool(row["exact"]) for row in continuity_anchor_rows),
        "extended_probe_candidate_count": len(extended_probe_rows),
        "extended_probe_exact_count": sum(bool(row["exact"]) for row in extended_probe_rows),
        "first_fail_candidate_id": None if first_fail is None else first_fail["candidate_id"],
        "first_fail_program_name": None if first_fail is None else first_fail["program_name"],
        "first_fail_reproduced": all(bool(row["reproduced"]) for row in failure_rechecks)
        if failure_rechecks
        else None,
        "first_fail_supporting_exact_neighbor_count": None
        if localized_boundary is None
        else localized_boundary["supporting_exact_neighbor_count"],
        "next_priority_lane": "r23_d0_same_endpoint_systems_overturn_gate",
    }


def build_summary(
    branch_specs: list[BranchSpec],
    gate: dict[str, object],
) -> dict[str, object]:
    return {
        "status": "r22_boundary_localization_complete",
        "current_frozen_stage": "h19_refreeze_and_next_scope_decision",
        "source_runtime_stage": "r21_d0_exact_executor_boundary_break_map",
        "gate": gate,
        "planned_lane_classes": ["continuity_anchor", "extended_probe"],
        "planned_families": sorted({spec.family for spec in branch_specs}),
        "planned_unique_address_targets": sorted({spec.unique_address_target for spec in branch_specs}),
        "planned_horizon_multipliers": sorted({spec.horizon_multiplier for spec in branch_specs}),
        "planned_checkpoint_depths": sorted(
            {spec.checkpoint_depth for spec in branch_specs},
            key=CHECKPOINT_DEPTH_ORDER.index,
        ),
        "planned_hot_address_skews": sorted(
            {spec.hot_address_skew for spec in branch_specs},
            key=HOT_ADDRESS_SKEW_ORDER.index,
        ),
        "executed_family_count": len({spec.family for spec in branch_specs}),
        "recommended_next_action": (
            "Advance to R23 on the same D0 endpoint, then refreeze R22 and R23 together in H21."
        ),
        "supported_here": [
            "R22 stayed on the current tiny typed-bytecode D0 endpoint.",
            "R22 preserved a continuity-anchor set and a harder extended-probe set in one machine-readable export.",
            "R22 preserves positive rows, failure rows, and first-fail diagnostics without opening a repair lane.",
        ],
        "unsupported_here": [
            "R22 does not authorize wider frontend, wider language scope, or a broader softmax-replacement claim.",
            "R22 does not itself repair failures or widen beyond the same-endpoint executor story.",
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    admitted_rows = load_r19_admitted_runtime_rows()
    template_registry = build_template_registry(admitted_rows)
    branch_plans = build_branch_plans()
    branch_specs = build_branch_specs(template_registry, branch_plans)
    spec_lookup = {spec.candidate_id: spec for spec in branch_specs}
    manifest_rows = [branch_spec_to_row(spec) for spec in branch_specs]
    rows, profiles, pruned_count, skipped_rows = execute_boundary_scan(branch_specs)
    branch_summary_rows = build_branch_summary(branch_specs, rows, skipped_rows)
    failure_rows = [row for row in rows if not bool(row["exact"])]
    first_fail_digest_rows = build_first_fail_digest(rows)
    localized_boundary_rows = build_localized_boundary(first_fail_digest_rows, branch_summary_rows)
    failure_rechecks = build_failure_rechecks(spec_lookup, first_fail_digest_rows)
    gate = assess_boundary_gate(
        branch_specs,
        rows,
        branch_summary_rows,
        pruned_count=pruned_count,
        skipped_rows=skipped_rows,
        first_fail_digest_rows=first_fail_digest_rows,
        localized_boundary_rows=localized_boundary_rows,
        failure_rechecks=failure_rechecks,
    )
    summary = build_summary(branch_specs, gate)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "branch_manifest.json",
        {"experiment": "r22_branch_manifest", "environment": environment.as_dict(), "rows": manifest_rows},
    )
    write_csv(OUT_DIR / "branch_manifest.csv", manifest_rows)
    write_json(
        OUT_DIR / "boundary_rows.json",
        {"experiment": "r22_boundary_rows", "environment": environment.as_dict(), "rows": rows},
    )
    write_csv(OUT_DIR / "boundary_rows.csv", rows)
    write_json(
        OUT_DIR / "address_profiles.json",
        {"experiment": "r22_address_profiles", "environment": environment.as_dict(), "rows": profiles},
    )
    write_json(
        OUT_DIR / "positive_rows.json",
        {
            "experiment": "r22_positive_rows",
            "environment": environment.as_dict(),
            "rows": [row for row in rows if bool(row["exact"])],
        },
    )
    write_json(
        OUT_DIR / "failure_rows.json",
        {"experiment": "r22_failure_rows", "environment": environment.as_dict(), "rows": failure_rows},
    )
    write_json(
        OUT_DIR / "skipped_rows.json",
        {"experiment": "r22_skipped_rows", "environment": environment.as_dict(), "rows": skipped_rows},
    )
    write_json(
        OUT_DIR / "branch_summary.json",
        {"experiment": "r22_branch_summary", "environment": environment.as_dict(), "rows": branch_summary_rows},
    )
    write_json(
        OUT_DIR / "first_fail_digest.json",
        {
            "experiment": "r22_first_fail_digest",
            "environment": environment.as_dict(),
            "rows": first_fail_digest_rows,
        },
    )
    write_json(
        OUT_DIR / "localized_boundary.json",
        {
            "experiment": "r22_localized_boundary",
            "environment": environment.as_dict(),
            "rows": localized_boundary_rows,
        },
    )
    write_json(
        OUT_DIR / "failure_rechecks.json",
        {
            "experiment": "r22_failure_rechecks",
            "environment": environment.as_dict(),
            "rows": failure_rechecks,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r22_d0_true_boundary_localization_gate",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/R19_d0_pointer_like_surface_generalization_gate/runtime_rows.json",
                "results/R20_d0_runtime_mechanism_ablation_matrix/summary.json",
                "results/R21_d0_exact_executor_boundary_break_map/summary.json",
                "docs/plans/2026-03-21-post-h19-mainline-reentry-design.md",
                "tmp/active_wave_plan.md",
                "src/model/free_running_executor.py",
                "src/bytecode/datasets.py",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# R22 D0 True Boundary Localization Gate\n\n"
        "Harder same-endpoint executor-boundary localization scan on the current D0 endpoint.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `branch_manifest.json`\n"
        "- `branch_manifest.csv`\n"
        "- `boundary_rows.json`\n"
        "- `boundary_rows.csv`\n"
        "- `address_profiles.json`\n"
        "- `positive_rows.json`\n"
        "- `failure_rows.json`\n"
        "- `skipped_rows.json`\n"
        "- `branch_summary.json`\n"
        "- `first_fail_digest.json`\n"
        "- `localized_boundary.json`\n"
        "- `failure_rechecks.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
