"""Export the restricted frontend translation gate for R47."""

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
    compile_restricted_frontend_program,
    first_divergence_step,
    lower_program,
    normalize_event,
    normalize_final_state,
    r47_restricted_frontend_translation_cases,
    run_spec_program,
    serialize_restricted_frontend_program,
    validate_program_contract,
    validate_restricted_frontend_program,
    validate_surface_literals,
    verify_program,
)
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R47_origin_restricted_frontend_translation_gate"


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


def validate_compiled_scope(program: BytecodeProgram) -> tuple[bool, str | None]:
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
    if not row["frontend_scope_passed"]:
        return "frontend_scope_break"
    if not row["compiled_scope_passed"]:
        return "compiled_scope_break"
    if not row["verifier_passed"]:
        return "verifier_break"
    if not row["spec_contract_passed"]:
        return "spec_contract_break"
    if not row["surface_literal_passed"]:
        return "surface_literal_break"
    if not row["translation_identity_match"]:
        return "translation_identity_break"
    if not row["compiled_to_canonical_trace_match"] or not row["compiled_to_canonical_final_state_match"]:
        return "canonical_alignment_break"
    if not row["compiled_spec_trace_match"] or not row["compiled_spec_final_state_match"]:
        return "spec_break"
    if not row["compiled_to_lowered_trace_match"] or not row["compiled_to_lowered_final_state_match"]:
        return "lowering_break"
    if not row["free_running_trace_match"] or not row["free_running_final_state_match"]:
        return "free_running_break"
    return None


def assess_gate(exactness_rows: list[dict[str, object]], stop_rule: dict[str, object]) -> dict[str, object]:
    planned_count = len(exactness_rows)
    executed_rows = [row for row in exactness_rows if row["executed"]]
    exact_rows = [row for row in executed_rows if row["verdict"] == "exact"]
    exact_kernel_ids = sorted({str(row["kernel_id"]) for row in exact_rows})
    return {
        "lane_verdict": "restricted_frontend_supported_narrowly" if len(exact_rows) == planned_count else "restricted_frontend_break",
        "restricted_frontend_surface": "structured_i32_static_memory_only",
        "planned_variant_count": planned_count,
        "executed_variant_count": len(executed_rows),
        "exact_variant_count": len(exact_rows),
        "failed_variant_count": len(executed_rows) - len(exact_rows),
        "planned_kernel_count": len({str(row["kernel_id"]) for row in exactness_rows}),
        "exact_kernel_count": len(exact_kernel_ids),
        "exact_kernel_ids": exact_kernel_ids,
        "translation_identity_exact_count": sum(bool(row["translation_identity_match"]) for row in exact_rows),
        "claim_ceiling": "bounded_useful_cases_only",
        "stop_rule_triggered": bool(stop_rule["stop_rule_triggered"]),
        "later_explicit_followup_packet_required": True,
        "next_required_lane": "h46_post_r47_frontend_bridge_decision_packet",
        "blocked_future_model_candidate": "r48_origin_dual_mode_useful_case_model_gate",
    }


def build_artifacts() -> tuple[list[dict[str, object]], dict[str, object], dict[str, object]]:
    cases = r47_restricted_frontend_translation_cases()
    manifest_rows = [
        {
            "case_order": index + 1,
            "kernel_id": case.kernel_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
            "frontend_program_name": case.frontend_program.name,
            "canonical_program_name": case.canonical_program.name,
        }
        for index, case in enumerate(cases)
    ]

    exactness_rows: list[dict[str, object]] = []
    cost_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for case in cases:
        frontend_scope_passed, frontend_scope_error = validate_restricted_frontend_program(case.frontend_program)
        compiled_program = compile_restricted_frontend_program(case.frontend_program)
        compiled_scope_passed, compiled_scope_error = validate_compiled_scope(compiled_program)
        verifier_result = verify_program(compiled_program)
        spec_contract = validate_program_contract(compiled_program)
        surface_literal = validate_surface_literals(compiled_program)
        spec_result = run_spec_program(compiled_program, max_steps=case.max_steps)
        compiled_result = BytecodeInterpreter().run(compiled_program, max_steps=case.max_steps)
        canonical_result = BytecodeInterpreter().run(case.canonical_program, max_steps=case.max_steps)
        lowered_program = lower_program(compiled_program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
        max_steps = max(case.max_steps, compiled_result.final_state.steps + 8)
        free_running_result = run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=max_steps)
        free_running_outcome = compare_execution_to_reference(
            lowered_program,
            free_running_result,
            reference=reference_wrapper(lowered_program, lowered_result),
        )

        read_counter = Counter(observation.space for observation in free_running_result.read_observations)
        compiled_spec_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in compiled_result.events
        )
        compiled_spec_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            compiled_result.final_state
        )
        compiled_to_canonical_trace_match = tuple(normalize_event(event) for event in compiled_result.events) == tuple(
            normalize_event(event) for event in canonical_result.events
        )
        compiled_to_canonical_final_state_match = normalize_final_state(
            compiled_result.final_state
        ) == normalize_final_state(canonical_result.final_state)
        compiled_to_lowered_trace_match = tuple(compiled_result.events) == tuple(lowered_result.events)
        compiled_to_lowered_final_state_match = compiled_result.final_state == lowered_result.final_state
        translation_identity_match = (
            compiled_program.instructions == case.canonical_program.instructions
            and compiled_program.memory_layout == case.canonical_program.memory_layout
        )
        memory_read_event_count = sum(int(event.memory_read_address is not None) for event in compiled_result.events)
        memory_write_event_count = sum(int(event.memory_write is not None) for event in compiled_result.events)
        branch_event_count = sum(int(bool(event.branch_taken)) for event in compiled_result.events)

        exactness_row = {
            "kernel_id": case.kernel_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "executed": True,
            "frontend_scope_passed": frontend_scope_passed,
            "frontend_scope_error_class": frontend_scope_error,
            "compiled_scope_passed": compiled_scope_passed,
            "compiled_scope_error_class": compiled_scope_error,
            "verifier_passed": verifier_result.passed,
            "verifier_error_class": verifier_result.error_class,
            "spec_contract_passed": spec_contract.passed,
            "spec_contract_error_class": spec_contract.error_class,
            "surface_literal_passed": surface_literal.passed,
            "surface_literal_error_class": surface_literal.error_class,
            "translation_identity_match": translation_identity_match,
            "compiled_to_canonical_trace_match": compiled_to_canonical_trace_match,
            "compiled_to_canonical_final_state_match": compiled_to_canonical_final_state_match,
            "compiled_to_canonical_first_mismatch_step": first_divergence_step(
                canonical_result.events,
                compiled_result.events,
            ),
            "compiled_spec_trace_match": compiled_spec_trace_match,
            "compiled_spec_final_state_match": compiled_spec_final_state_match,
            "compiled_spec_first_mismatch_step": first_divergence_step(spec_result.events, compiled_result.events),
            "compiled_to_lowered_trace_match": compiled_to_lowered_trace_match,
            "compiled_to_lowered_final_state_match": compiled_to_lowered_final_state_match,
            "compiled_to_lowered_first_mismatch_step": first_divergence_step(compiled_result.events, lowered_result.events),
            "free_running_trace_match": free_running_outcome.exact_trace_match,
            "free_running_final_state_match": free_running_outcome.exact_final_state_match,
            "first_mismatch_step": free_running_outcome.first_mismatch_step,
            "failure_reason": free_running_outcome.failure_reason,
            "compiled_final_state": normalize_state_dict(compiled_result.final_state),
            "canonical_final_state": normalize_state_dict(canonical_result.final_state),
            "lowered_final_state": normalize_state_dict(lowered_result.final_state),
            "free_running_final_state": normalize_state_dict(free_running_result.final_state),
            "compiled_declared_memory": declared_memory_snapshot(compiled_program, compiled_result.final_state),
            "canonical_declared_memory": declared_memory_snapshot(case.canonical_program, canonical_result.final_state),
            "free_running_declared_memory": declared_memory_snapshot(compiled_program, free_running_result.final_state),
            "frontend_program": serialize_restricted_frontend_program(case.frontend_program),
            "compiled_program": serialize_bytecode_program(compiled_program),
            "canonical_program": serialize_bytecode_program(case.canonical_program),
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
                "instruction_count": len(compiled_program.instructions),
                "program_steps": compiled_result.final_state.steps,
                "memory_read_event_count": memory_read_event_count,
                "memory_write_event_count": memory_write_event_count,
                "branch_event_count": branch_event_count,
                "free_running_read_count": len(free_running_result.read_observations),
                "free_running_stack_read_count": read_counter.get("stack", 0),
                "free_running_memory_read_count": read_counter.get("memory", 0),
                "free_running_call_read_count": read_counter.get("call", 0),
                "declared_memory_cell_count": len(compiled_program.memory_layout),
                "opcode_surface": opcode_surface(compiled_program),
            }
        )

        if first_failure is None and stop_class is not None:
            first_failure = {
                "kernel_id": case.kernel_id,
                "variant_id": case.variant_id,
                "stop_class": stop_class,
                "first_mismatch_step": exactness_row["first_mismatch_step"],
                "failure_reason": exactness_row["failure_reason"],
            }

    kernel_rollup_rows: list[dict[str, object]] = []
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in exactness_rows:
        grouped[str(row["kernel_id"])].append(row)
    for kernel_id in sorted(grouped):
        rows = grouped[kernel_id]
        kernel_rollup_rows.append(
            {
                "kernel_id": kernel_id,
                "planned_variant_count": len(rows),
                "exact_variant_count": sum(row["verdict"] == "exact" for row in rows),
                "translation_identity_exact_count": sum(bool(row["translation_identity_match"]) for row in rows),
            }
        )

    stop_rule = {
        "stop_rule_triggered": first_failure is not None,
        "first_failure": first_failure,
        "stop_policy": "stop at first excluded feature, translation mismatch, or exact free-running break",
    }
    report = {
        "environment": environment_payload(),
        "exactness_rows": exactness_rows,
        "cost_rows": cost_rows,
        "kernel_rollup_rows": kernel_rollup_rows,
    }
    summary = {
        "environment": environment_payload(),
        "summary": {
            "current_active_docs_only_stage": "h45_post_r46_surface_decision_packet",
            "active_runtime_lane": "r47_origin_restricted_frontend_translation_gate",
            "activation_packet": "h45_post_r46_surface_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
            "preserved_prior_post_h44_exact_gate": "r46_origin_useful_case_surface_generalization_gate",
            "gate": assess_gate(exactness_rows, stop_rule),
        },
    }
    return manifest_rows, report, stop_rule, summary


def main() -> None:
    manifest_rows, report, stop_rule, summary = build_artifacts()
    write_json(OUT_DIR / "case_manifest.json", {"rows": manifest_rows})
    write_json(OUT_DIR / "translation_report.json", report)
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
