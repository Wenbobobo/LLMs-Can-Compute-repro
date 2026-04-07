"""Export the post-H44 useful-case surface generalization gate for R46."""

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
    UsefulCaseSurfaceGeneralizationCase,
    first_divergence_step,
    lower_program,
    normalize_event,
    normalize_final_state,
    r46_useful_case_surface_generalization_cases,
    run_spec_program,
    validate_program_contract,
    validate_surface_literals,
    verify_program,
)
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R46_origin_useful_case_surface_generalization_gate"


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


def serialize_bytecode_program(program: BytecodeProgram) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pc, instruction in enumerate(program.instructions):
        rows.append(
            {
                "pc": pc,
                "opcode": instruction.opcode.value,
                "arg": instruction.arg,
                "in_types": [item.value for item in instruction.in_types],
                "out_types": [item.value for item in instruction.out_types],
            }
        )
    return rows


def serialize_trace_program(program: Any) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pc, instruction in enumerate(program.instructions):
        opcode = getattr(getattr(instruction, "opcode", None), "value", getattr(instruction, "opcode", None))
        rows.append({"pc": pc, "opcode": opcode, "arg": instruction.arg})
    return rows


def opcode_surface(program: BytecodeProgram) -> list[str]:
    return sorted({instruction.opcode.value for instruction in program.instructions})


def reference_wrapper(program: Any, result: Any) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def validate_r46_scope(case: UsefulCaseSurfaceGeneralizationCase) -> tuple[bool, str | None]:
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


def build_artifacts() -> tuple[list[dict[str, object]], dict[str, object], dict[str, object]]:
    cases = r46_useful_case_surface_generalization_cases()
    manifest_rows = [
        {
            "case_order": index + 1,
            "kernel_id": case.kernel_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
            "program_name": case.program.name,
        }
        for index, case in enumerate(cases)
    ]

    exactness_rows: list[dict[str, object]] = []
    cost_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for case in cases:
        program = case.program
        verifier_result = verify_program(program)
        spec_contract = validate_program_contract(program)
        surface_literal = validate_surface_literals(program)
        scope_passed, scope_error_class = validate_r46_scope(case)
        spec_result = run_spec_program(program, max_steps=case.max_steps)
        source_result = BytecodeInterpreter().run(program, max_steps=case.max_steps)
        lowered_program = lower_program(program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
        max_steps = max(case.max_steps, source_result.final_state.steps + 8)
        free_running_result = run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=max_steps)
        free_running_outcome = compare_execution_to_reference(
            lowered_program,
            free_running_result,
            reference=reference_wrapper(lowered_program, lowered_result),
        )

        read_counter = Counter(observation.space for observation in free_running_result.read_observations)
        source_spec_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in source_result.events
        )
        source_spec_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            source_result.final_state
        )
        source_to_lowered_trace_match = tuple(source_result.events) == tuple(lowered_result.events)
        source_to_lowered_final_state_match = source_result.final_state == lowered_result.final_state
        memory_read_event_count = sum(int(event.memory_read_address is not None) for event in source_result.events)
        memory_write_event_count = sum(int(event.memory_write is not None) for event in source_result.events)
        branch_event_count = sum(int(bool(event.branch_taken)) for event in source_result.events)

        exactness_row = {
            "kernel_id": case.kernel_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "executed": True,
            "verifier_passed": verifier_result.passed,
            "verifier_error_class": verifier_result.error_class,
            "spec_contract_passed": spec_contract.passed,
            "spec_contract_error_class": spec_contract.error_class,
            "surface_literal_passed": surface_literal.passed,
            "surface_literal_error_class": surface_literal.error_class,
            "scope_passed": scope_passed,
            "scope_error_class": scope_error_class,
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
            "source_final_state": normalize_state_dict(source_result.final_state),
            "lowered_final_state": normalize_state_dict(lowered_result.final_state),
            "free_running_final_state": normalize_state_dict(free_running_result.final_state),
            "source_declared_memory": declared_memory_snapshot(program, source_result.final_state),
            "lowered_declared_memory": declared_memory_snapshot(program, lowered_result.final_state),
            "free_running_declared_memory": declared_memory_snapshot(program, free_running_result.final_state),
            "source_program": serialize_bytecode_program(program),
            "lowered_program": serialize_trace_program(lowered_program),
        }
        stop_class = failure_class(exactness_row)
        exactness_row["stop_class"] = stop_class
        exactness_row["verdict"] = "exact" if stop_class is None else "break"
        exactness_rows.append(exactness_row)

        cost_rows.append(
            {
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
                "opcode_surface": opcode_surface(program),
            }
        )

        if first_failure is None and stop_class is not None:
            first_failure = {
                "kernel_id": case.kernel_id,
                "variant_id": case.variant_id,
                "stop_class": stop_class,
                "first_mismatch_step": free_running_outcome.first_mismatch_step,
                "failure_reason": free_running_outcome.failure_reason,
            }

    kernel_rollup_counter: dict[str, dict[str, int]] = defaultdict(lambda: {"planned": 0, "exact": 0})
    axis_rollup_counter: Counter[str] = Counter()
    for row in exactness_rows:
        kernel_rollup_counter[row["kernel_id"]]["planned"] += 1
        kernel_rollup_counter[row["kernel_id"]]["exact"] += int(row["verdict"] == "exact")
        for tag in row["axis_tags"]:
            axis_rollup_counter[tag] += 1

    kernel_rollup_rows = [
        {
            "kernel_id": kernel_id,
            "planned_variant_count": counts["planned"],
            "exact_variant_count": counts["exact"],
            "kernel_verdict": "all_exact"
            if counts["planned"] == counts["exact"]
            else ("no_exact" if counts["exact"] == 0 else "mixed"),
        }
        for kernel_id, counts in sorted(kernel_rollup_counter.items())
    ]
    axis_rollup_rows = [
        {"axis_tag": axis_tag, "covered_case_count": count}
        for axis_tag, count in sorted(axis_rollup_counter.items())
    ]

    stop_rule = {
        "planned_variant_count": len(cases),
        "executed_variant_count": len(exactness_rows),
        "stop_rule_triggered": first_failure is not None,
        "first_failure": first_failure,
        "reason": "all held-out useful-case surface variants stayed exact"
        if first_failure is None
        else "at least one held-out useful-case surface variant broke exactness",
    }
    surface_report = {
        "exactness_rows": exactness_rows,
        "cost_rows": cost_rows,
        "kernel_rollup_rows": kernel_rollup_rows,
        "axis_rollup_rows": axis_rollup_rows,
    }
    return manifest_rows, surface_report, stop_rule


def assess_gate(surface_report: dict[str, object], stop_rule: dict[str, object]) -> dict[str, object]:
    exactness_rows = surface_report["exactness_rows"]
    kernel_rollup_rows = surface_report["kernel_rollup_rows"]
    planned_variant_count = len(exactness_rows)
    exact_variant_count = sum(row["verdict"] == "exact" for row in exactness_rows)
    exact_kernel_count = sum(row["kernel_verdict"] == "all_exact" for row in kernel_rollup_rows)

    if exact_variant_count == planned_variant_count:
        lane_verdict = "surface_generalizes_narrowly"
    elif exact_variant_count == 0:
        lane_verdict = "fixed_suite_only"
    else:
        lane_verdict = "mixed_inside_surface"

    return {
        "lane_verdict": lane_verdict,
        "route_posture": "exact_first_useful_case_surface_generalization",
        "planned_variant_count": planned_variant_count,
        "executed_variant_count": planned_variant_count,
        "exact_variant_count": exact_variant_count,
        "failed_variant_count": planned_variant_count - exact_variant_count,
        "planned_kernel_count": len(kernel_rollup_rows),
        "exact_kernel_count": exact_kernel_count,
        "stop_rule_triggered": bool(stop_rule["stop_rule_triggered"]),
        "article_level_surface_generalization_survived_narrowly": lane_verdict == "surface_generalizes_narrowly",
        "claim_ceiling": "bounded_useful_cases_only",
        "later_explicit_followup_packet_required": True,
        "next_required_lane": "h45_post_r46_surface_decision_packet",
    }


def main() -> None:
    manifest_rows, surface_report, stop_rule = build_artifacts()
    gate = assess_gate(surface_report, stop_rule)

    write_json(OUT_DIR / "case_manifest.json", {"rows": manifest_rows})
    write_json(OUT_DIR / "surface_report.json", surface_report)
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": {
                "current_paper_phase": "h44_post_h43_route_reauthorization_packet_active",
                "current_active_docs_only_stage": "h44_post_h43_route_reauthorization_packet",
                "active_runtime_lane": "r46_origin_useful_case_surface_generalization_gate",
                "activation_packet": "h44_post_h43_route_reauthorization_packet",
                "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
                "current_completed_exact_runtime_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
                "current_completed_useful_case_gate": "r44_origin_restricted_wasm_useful_case_execution_gate",
                "current_completed_post_h44_exact_runtime_gate": "r46_origin_useful_case_surface_generalization_gate",
                "coequal_model_comparator_gate": "r45_origin_dual_mode_model_mainline_gate",
                "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
                "next_required_packet": "h45_post_r46_surface_decision_packet",
                "gate": gate,
            },
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
