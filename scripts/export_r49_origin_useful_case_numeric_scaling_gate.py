"""Export the post-H47 useful-case numeric scaling gate for R49."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from bytecode import (
    BytecodeInterpreter,
    BytecodeMemoryRegion,
    BytecodeOpcode,
    BytecodeProgram,
    UsefulCaseNumericScalingCase,
    first_divergence_step,
    lower_program,
    normalize_event,
    normalize_final_state,
    r49_useful_case_numeric_scaling_cases,
    run_spec_program,
    validate_program_contract,
    validate_surface_literals,
    verify_program,
)
from exec_trace import TraceInterpreter
from model import (
    FreeRunningExecutionResult,
    check_real_trace_precision,
    compare_execution_to_reference,
    extract_memory_operations,
    run_free_running_exact,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R49_origin_useful_case_numeric_scaling_gate"


ALLOWED_OPCODES: frozenset[BytecodeOpcode] = frozenset(
    {
        BytecodeOpcode.CONST_I32,
        BytecodeOpcode.DUP,
        BytecodeOpcode.POP,
        BytecodeOpcode.ADD_I32,
        BytecodeOpcode.SUB_I32,
        BytecodeOpcode.EQ_I32,
        BytecodeOpcode.LOAD_STATIC,
        BytecodeOpcode.STORE_STATIC,
        BytecodeOpcode.JMP,
        BytecodeOpcode.JZ_ZERO,
        BytecodeOpcode.HALT,
    }
)

PRIMARY_PRECISION_REGIMES: tuple[dict[str, object], ...] = (
    {
        "regime_id": "float32_single_head",
        "fmt": "float32",
        "scheme": "single_head",
        "base": 64,
        "addressability_strategy": "preserved_absolute_base",
        "role": "negative_control",
        "admitted_recovery": False,
    },
    {
        "regime_id": "float32_radix2",
        "fmt": "float32",
        "scheme": "radix2",
        "base": 64,
        "addressability_strategy": "radix2_address_split",
        "role": "admitted_recovery",
        "admitted_recovery": True,
    },
    {
        "regime_id": "float32_block_recentered",
        "fmt": "float32",
        "scheme": "block_recentered",
        "base": 64,
        "addressability_strategy": "block_recentered_window",
        "role": "admitted_recovery",
        "admitted_recovery": True,
    },
)

FLOAT64_REFERENCE_REGIME: dict[str, object] = {
    "regime_id": "float64_reference",
    "fmt": "float64",
    "scheme": "single_head",
    "base": 64,
    "addressability_strategy": "preserved_absolute_base",
    "role": "sampled_reference",
    "admitted_recovery": False,
}


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize_state_dict(state: object) -> dict[str, object]:
    pc, stack, memory, call_stack, halted, steps = normalize_final_state(state)
    return {
        "pc": int(pc),
        "stack": list(stack),
        "memory": [list(item) for item in memory],
        "call_stack": list(call_stack),
        "halted": bool(halted),
        "steps": int(steps),
    }


def reference_wrapper(program: Any, result: Any) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def validate_r49_scope(case: UsefulCaseNumericScalingCase) -> tuple[bool, str | None]:
    program = case.program
    opcodes = {instruction.opcode for instruction in program.instructions}
    if not opcodes.issubset(ALLOWED_OPCODES):
        return False, "opcode_out_of_scope"
    if any(cell.region == BytecodeMemoryRegion.HEAP for cell in program.memory_layout):
        return False, "heap_region_not_admitted"
    return True, None


def declared_memory_snapshot(program: BytecodeProgram, state: object) -> dict[str, int]:
    _, _, memory, _, _, _ = normalize_final_state(state)
    memory_map = {int(address): int(value) for address, value in memory}
    return {
        cell.label: memory_map.get(cell.address, 0)
        for cell in sorted(program.memory_layout, key=lambda item: item.address)
    }


def failure_class(row: dict[str, object]) -> str | None:
    if not row["scope_passed"]:
        return "scope_break"
    if not row["verifier_passed"]:
        return "verifier_break"
    if not row["spec_contract_passed"]:
        return "spec_contract_break"
    if not row["surface_literal_passed"]:
        return "surface_literal_break"
    if not row["source_spec_trace_match"] or not row["source_spec_final_state_match"]:
        return "source_spec_break"
    if not row["source_to_lowered_trace_match"] or not row["source_to_lowered_final_state_match"]:
        return "lowering_break"
    if not row["free_running_trace_match"] or not row["free_running_final_state_match"]:
        return "free_running_break"
    return None


def _memory_surface_span(program: BytecodeProgram) -> tuple[int, int]:
    addresses = [cell.address for cell in program.memory_layout]
    return min(addresses), max(addresses)


def _precision_rows_for_case(
    case: UsefulCaseNumericScalingCase,
    operations,
) -> list[dict[str, object]]:
    native_max_steps = max(operation.step for operation in operations)
    address_values = [operation.address for operation in operations]
    rows: list[dict[str, object]] = []
    regimes = list(PRIMARY_PRECISION_REGIMES)
    if case.precision_reference_sampled:
        regimes.append(FLOAT64_REFERENCE_REGIME)

    for regime in regimes:
        result = check_real_trace_precision(
            operations,
            fmt=str(regime["fmt"]),
            scheme=str(regime["scheme"]),
            base=int(regime["base"]),
            max_steps=case.max_steps,
        )
        failure = result.first_failure
        rows.append(
            {
                "bucket_id": case.bucket_id,
                "kernel_id": case.kernel_id,
                "variant_id": case.variant_id,
                "program_name": case.program.name,
                "max_steps_budget": case.max_steps,
                "native_operation_max_step": native_max_steps,
                "operation_address_min": min(address_values),
                "operation_address_max": max(address_values),
                "regime_id": regime["regime_id"],
                "fmt": regime["fmt"],
                "scheme": regime["scheme"],
                "base": regime["base"],
                "addressability_strategy": regime["addressability_strategy"],
                "role": regime["role"],
                "admitted_recovery": regime["admitted_recovery"],
                "read_count": result.read_count,
                "write_count": result.write_count,
                "passed": result.passed,
                "failure_type": None if failure is None else failure.failure_type,
                "failure_read_step": None if failure is None else failure.read_step,
                "failure_query_address": None if failure is None else failure.query_address,
                "expected_address": None if failure is None else failure.expected_address,
                "expected_step": None if failure is None else failure.expected_step,
                "competing_address": None if failure is None else failure.competing_address,
                "competing_step": None if failure is None else failure.competing_step,
                "expected_scores": None if failure is None else list(failure.expected_scores),
                "competing_scores": None if failure is None else list(failure.competing_scores),
            }
        )
    return rows


def build_artifacts() -> tuple[list[dict[str, object]], dict[str, object], dict[str, object], dict[str, object]]:
    cases = r49_useful_case_numeric_scaling_cases()
    manifest_rows = [
        {
            "case_order": index + 1,
            "bucket_id": case.bucket_id,
            "kernel_id": case.kernel_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
            "program_name": case.program.name,
            "precision_reference_sampled": case.precision_reference_sampled,
        }
        for index, case in enumerate(cases)
    ]

    exactness_rows: list[dict[str, object]] = []
    cost_rows: list[dict[str, object]] = []
    precision_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for case in cases:
        program = case.program
        verifier_result = verify_program(program)
        spec_contract = validate_program_contract(program)
        surface_literal = validate_surface_literals(program)
        scope_passed, scope_error_class = validate_r49_scope(case)
        spec_result = run_spec_program(program, max_steps=case.max_steps)
        source_result = BytecodeInterpreter().run(program, max_steps=case.max_steps)
        lowered_program = lower_program(program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
        free_running_result = run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=case.max_steps)
        free_running_outcome = compare_execution_to_reference(
            lowered_program,
            free_running_result,
            reference=reference_wrapper(lowered_program, lowered_result),
        )

        source_spec_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in source_result.events
        )
        source_spec_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            source_result.final_state
        )
        source_to_lowered_trace_match = tuple(source_result.events) == tuple(lowered_result.events)
        source_to_lowered_final_state_match = source_result.final_state == lowered_result.final_state
        read_counter = Counter(observation.space for observation in free_running_result.read_observations)
        memory_read_event_count = sum(int(event.memory_read_address is not None) for event in source_result.events)
        memory_write_event_count = sum(int(event.memory_write is not None) for event in source_result.events)
        branch_event_count = sum(int(bool(event.branch_taken)) for event in source_result.events)
        memory_surface_min, memory_surface_max = _memory_surface_span(program)

        exactness_row = {
            "bucket_id": case.bucket_id,
            "kernel_id": case.kernel_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "comparison_mode": case.comparison_mode,
            "max_steps_budget": case.max_steps,
            "precision_reference_sampled": case.precision_reference_sampled,
            "executed": True,
            "scope_passed": scope_passed,
            "scope_error_class": scope_error_class,
            "verifier_passed": verifier_result.passed,
            "verifier_error_class": verifier_result.error_class,
            "spec_contract_passed": spec_contract.passed,
            "spec_contract_error_class": spec_contract.error_class,
            "surface_literal_passed": surface_literal.passed,
            "surface_literal_error_class": surface_literal.error_class,
            "source_spec_trace_match": source_spec_trace_match,
            "source_spec_final_state_match": source_spec_final_state_match,
            "source_spec_first_mismatch_step": first_divergence_step(spec_result.events, source_result.events),
            "source_to_lowered_trace_match": source_to_lowered_trace_match,
            "source_to_lowered_final_state_match": source_to_lowered_final_state_match,
            "source_to_lowered_first_mismatch_step": first_divergence_step(source_result.events, lowered_result.events),
            "free_running_trace_match": free_running_outcome.exact_trace_match,
            "free_running_final_state_match": free_running_outcome.exact_final_state_match,
            "first_mismatch_step": free_running_outcome.first_mismatch_step,
            "failure_reason": free_running_outcome.failure_reason,
            "instruction_count": len(program.instructions),
            "program_steps": source_result.final_state.steps,
            "declared_memory_cell_count": len(program.memory_layout),
            "memory_surface_min_address": memory_surface_min,
            "memory_surface_max_address": memory_surface_max,
            "source_final_state": normalize_state_dict(source_result.final_state),
            "lowered_final_state": normalize_state_dict(lowered_result.final_state),
            "free_running_final_state": normalize_state_dict(free_running_result.final_state),
            "source_declared_memory": declared_memory_snapshot(program, source_result.final_state),
            "lowered_declared_memory": declared_memory_snapshot(program, lowered_result.final_state),
            "free_running_declared_memory": declared_memory_snapshot(program, free_running_result.final_state),
        }
        stop_class = failure_class(exactness_row)
        exactness_row["stop_class"] = stop_class
        exactness_row["verdict"] = "exact" if stop_class is None else "break"
        exactness_rows.append(exactness_row)

        cost_rows.append(
            {
                "bucket_id": case.bucket_id,
                "kernel_id": case.kernel_id,
                "variant_id": case.variant_id,
                "instruction_count": len(program.instructions),
                "program_steps": source_result.final_state.steps,
                "memory_read_event_count": memory_read_event_count,
                "memory_write_event_count": memory_write_event_count,
                "branch_event_count": branch_event_count,
                "free_running_read_count": len(free_running_result.read_observations),
                "free_running_stack_read_count": read_counter.get("stack", 0),
                "free_running_memory_read_count": read_counter.get("memory", 0),
                "free_running_call_read_count": read_counter.get("call", 0),
                "declared_memory_cell_count": len(program.memory_layout),
                "memory_surface_min_address": memory_surface_min,
                "memory_surface_max_address": memory_surface_max,
            }
        )

        if stop_class is None:
            operations = extract_memory_operations(lowered_result.events)
            precision_rows.extend(_precision_rows_for_case(case, operations))
        elif first_failure is None:
            first_failure = {
                "bucket_id": case.bucket_id,
                "kernel_id": case.kernel_id,
                "variant_id": case.variant_id,
                "stop_class": stop_class,
                "first_mismatch_step": free_running_outcome.first_mismatch_step,
                "failure_reason": free_running_outcome.failure_reason,
            }

    exactness_bucket_rows: list[dict[str, object]] = []
    grouped_exactness: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in exactness_rows:
        grouped_exactness[str(row["bucket_id"])].append(row)
    for bucket_id in sorted(grouped_exactness):
        rows = grouped_exactness[bucket_id]
        exact_count = sum(row["verdict"] == "exact" for row in rows)
        exactness_bucket_rows.append(
            {
                "bucket_id": bucket_id,
                "planned_case_count": len(rows),
                "exact_case_count": exact_count,
                "failed_case_count": len(rows) - exact_count,
                "kernel_ids": sorted({str(row["kernel_id"]) for row in rows}),
                "all_exact": exact_count == len(rows),
            }
        )

    kernel_rows: list[dict[str, object]] = []
    grouped_kernels: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in exactness_rows:
        grouped_kernels[str(row["kernel_id"])].append(row)
    for kernel_id in sorted(grouped_kernels):
        rows = grouped_kernels[kernel_id]
        exact_count = sum(row["verdict"] == "exact" for row in rows)
        kernel_rows.append(
            {
                "kernel_id": kernel_id,
                "planned_case_count": len(rows),
                "exact_case_count": exact_count,
                "bucket_ids": sorted({str(row["bucket_id"]) for row in rows}),
                "all_exact": exact_count == len(rows),
            }
        )

    case_summary_rows: list[dict[str, object]] = []
    grouped_precision: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in precision_rows:
        grouped_precision[(str(row["bucket_id"]), str(row["variant_id"]))].append(row)
    for (bucket_id, variant_id), rows in sorted(grouped_precision.items()):
        by_regime = {str(row["regime_id"]): row for row in rows}
        single_head_row = by_regime["float32_single_head"]
        radix2_row = by_regime["float32_radix2"]
        block_row = by_regime["float32_block_recentered"]
        float64_row = by_regime.get("float64_reference")
        admitted_exact = [
            regime_id
            for regime_id, row in (
                ("float32_radix2", radix2_row),
                ("float32_block_recentered", block_row),
            )
            if bool(row["passed"])
        ]
        case_summary_rows.append(
            {
                "bucket_id": bucket_id,
                "kernel_id": rows[0]["kernel_id"],
                "variant_id": variant_id,
                "program_name": rows[0]["program_name"],
                "max_steps_budget": rows[0]["max_steps_budget"],
                "float32_single_head_passed": bool(single_head_row["passed"]),
                "float32_single_head_failure_type": single_head_row["failure_type"],
                "float32_radix2_passed": bool(radix2_row["passed"]),
                "float32_block_recentered_passed": bool(block_row["passed"]),
                "float64_reference_sampled": float64_row is not None,
                "float64_reference_passed": None if float64_row is None else bool(float64_row["passed"]),
                "admitted_float32_recovery_regimes": admitted_exact,
                "decomposition_recovers_single_head_failure": (not bool(single_head_row["passed"])) and bool(admitted_exact),
            }
        )

    bucket_summary_rows: list[dict[str, object]] = []
    grouped_case_summary: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in case_summary_rows:
        grouped_case_summary[str(row["bucket_id"])].append(row)
    planned_by_bucket = {str(row["bucket_id"]): int(row["planned_case_count"]) for row in exactness_bucket_rows}
    for bucket_id in sorted(planned_by_bucket):
        rows = grouped_case_summary.get(bucket_id, [])
        planned_case_count = planned_by_bucket[bucket_id]
        single_head_exact_case_count = sum(bool(row["float32_single_head_passed"]) for row in rows)
        single_head_failed_case_count = sum(not bool(row["float32_single_head_passed"]) for row in rows)
        radix2_exact_case_count = sum(bool(row["float32_radix2_passed"]) for row in rows)
        block_exact_case_count = sum(bool(row["float32_block_recentered_passed"]) for row in rows)
        admitted_exact_regimes: list[str] = []
        if radix2_exact_case_count == planned_case_count:
            admitted_exact_regimes.append("float32_radix2")
        if block_exact_case_count == planned_case_count:
            admitted_exact_regimes.append("float32_block_recentered")
        exactness_row = next(row for row in exactness_bucket_rows if str(row["bucket_id"]) == bucket_id)
        if int(exactness_row["exact_case_count"]) != planned_case_count:
            bucket_verdict = "exactness_break"
        elif admitted_exact_regimes:
            bucket_verdict = "admitted_float32_survives"
        else:
            bucket_verdict = "no_admitted_float32_recovery"
        bucket_summary_rows.append(
            {
                "bucket_id": bucket_id,
                "planned_case_count": planned_case_count,
                "precision_screened_case_count": len(rows),
                "exact_case_count": exactness_row["exact_case_count"],
                "single_head_exact_case_count": single_head_exact_case_count,
                "single_head_failed_case_count": single_head_failed_case_count,
                "float32_radix2_exact_case_count": radix2_exact_case_count,
                "float32_block_recentered_exact_case_count": block_exact_case_count,
                "admitted_float32_recovery_exact_regimes": admitted_exact_regimes,
                "sampled_float64_reference_count": sum(bool(row["float64_reference_sampled"]) for row in rows),
                "sampled_float64_reference_exact_count": sum(bool(row["float64_reference_passed"]) for row in rows),
                "decomposition_recovery_case_count": sum(
                    bool(row["decomposition_recovers_single_head_failure"]) for row in rows
                ),
                "bucket_verdict": bucket_verdict,
            }
        )

    sampled_reference_failures = [
        row
        for row in case_summary_rows
        if bool(row["float64_reference_sampled"])
        and bool(row["float64_reference_passed"])
        and not bool(row["admitted_float32_recovery_regimes"])
    ]
    bucket_summary_by_id = {str(row["bucket_id"]): row for row in bucket_summary_rows}
    bucket_a = bucket_summary_by_id["bucket_a_2x"]
    bucket_b = bucket_summary_by_id["bucket_b_4x"]
    kill_triggers: list[str] = []
    if not bucket_a["admitted_float32_recovery_exact_regimes"]:
        kill_triggers.append("no_admitted_float32_recovery_on_bucket_a")
    if sampled_reference_failures:
        kill_triggers.append("sampled_float64_only_survival")
    if not bucket_b["admitted_float32_recovery_exact_regimes"]:
        kill_triggers.append("no_clean_transition_to_f25_after_bucket_b")
    if any(not bool(row["scope_passed"]) for row in exactness_rows):
        kill_triggers.append("scope_lift_or_surface_break_required")

    stop_rule = {
        "planned_case_count": len(cases),
        "exact_case_count": sum(row["verdict"] == "exact" for row in exactness_rows),
        "precision_row_count": len(precision_rows),
        "stop_rule_triggered": bool(first_failure is not None or kill_triggers),
        "first_exactness_failure": first_failure,
        "kill_triggers": kill_triggers,
        "reason": "all buckets stayed exact and at least one admitted float32 recovery regime stayed exact on bucket_a and bucket_b"
        if not (first_failure is not None or kill_triggers)
        else "exactness or bucket-level kill criteria fired before H48 interpretation",
    }

    exactness_report = {
        "exactness_rows": exactness_rows,
        "cost_rows": cost_rows,
        "exactness_bucket_rows": exactness_bucket_rows,
        "kernel_rows": kernel_rows,
    }
    precision_report = {
        "screening_rows": precision_rows,
        "case_summary_rows": case_summary_rows,
        "bucket_summary_rows": bucket_summary_rows,
    }
    return manifest_rows, exactness_report, precision_report, stop_rule


def assess_gate(
    exactness_report: dict[str, object],
    precision_report: dict[str, object],
    stop_rule: dict[str, object],
) -> dict[str, object]:
    exactness_rows = exactness_report["exactness_rows"]
    bucket_rows = precision_report["bucket_summary_rows"]
    bucket_by_id = {str(row["bucket_id"]): row for row in bucket_rows}
    bucket_a = bucket_by_id["bucket_a_2x"]
    bucket_b = bucket_by_id["bucket_b_4x"]
    bucket_c = bucket_by_id["bucket_c_8x"]
    exact_case_count = sum(row["verdict"] == "exact" for row in exactness_rows)
    planned_case_count = len(exactness_rows)
    single_head_failure_case_count = sum(int(row["single_head_failed_case_count"]) for row in bucket_rows)
    decomposition_recovery_case_count = sum(int(row["decomposition_recovery_case_count"]) for row in bucket_rows)

    if exact_case_count != planned_case_count:
        lane_verdict = "numeric_scaling_exactness_break"
    elif not bucket_a["admitted_float32_recovery_exact_regimes"] or not bucket_b["admitted_float32_recovery_exact_regimes"]:
        lane_verdict = "numeric_scaling_practical_falsifier"
    elif bucket_c["admitted_float32_recovery_exact_regimes"]:
        lane_verdict = "numeric_scaling_survives_through_bucket_c"
    else:
        lane_verdict = "numeric_scaling_survives_through_bucket_b_only"

    return {
        "lane_verdict": lane_verdict,
        "route_posture": "exact_first_useful_case_numeric_scaling",
        "planned_case_count": planned_case_count,
        "exact_case_count": exact_case_count,
        "failed_case_count": planned_case_count - exact_case_count,
        "bucket_count": len(bucket_rows),
        "kernel_count": len({str(row["kernel_id"]) for row in exactness_rows}),
        "precision_row_count": len(precision_report["screening_rows"]),
        "sampled_float64_reference_case_count": sum(
            bool(row["float64_reference_sampled"]) for row in precision_report["case_summary_rows"]
        ),
        "single_head_failure_case_count": single_head_failure_case_count,
        "decomposition_recovery_case_count": decomposition_recovery_case_count,
        "bucket_a_admitted_float32_recovery_exact_regimes": list(bucket_a["admitted_float32_recovery_exact_regimes"]),
        "bucket_b_admitted_float32_recovery_exact_regimes": list(bucket_b["admitted_float32_recovery_exact_regimes"]),
        "bucket_c_admitted_float32_recovery_exact_regimes": list(bucket_c["admitted_float32_recovery_exact_regimes"]),
        "practical_falsifier_triggered": bool(stop_rule["stop_rule_triggered"]),
        "claim_ceiling": "bounded_useful_cases_only",
        "next_required_packet": "h48_post_r49_numeric_scaling_decision_packet",
    }


def main() -> None:
    manifest_rows, exactness_report, precision_report, stop_rule = build_artifacts()
    gate = assess_gate(exactness_report, precision_report, stop_rule)

    write_json(OUT_DIR / "case_manifest.json", {"rows": manifest_rows})
    write_json(OUT_DIR / "exactness_report.json", exactness_report)
    write_json(OUT_DIR / "precision_report.json", precision_report)
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": {
                "current_active_docs_only_stage": "h47_post_r48_useful_case_bridge_refreeze",
                "active_runtime_lane": "r49_origin_useful_case_numeric_scaling_gate",
                "activation_packet": "h47_post_r48_useful_case_bridge_refreeze",
                "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
                "current_exact_first_planning_bundle": "f23_post_h47_numeric_scaling_bundle",
                "preserved_prior_post_h44_exact_gate": "r46_origin_useful_case_surface_generalization_gate",
                "preserved_prior_frontend_bridge_gate": "r47_origin_restricted_frontend_translation_gate",
                "preserved_comparator_only_gate": "r48_origin_dual_mode_useful_case_model_gate",
                "gate": gate,
            },
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
