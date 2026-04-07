"""Export the restricted stack-bytecode lowering contract gate for R58."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from bytecode import (
    BytecodeInterpreter,
    BytecodeMemoryRegion,
    BytecodeOpcode,
    BytecodeProgram,
    lower_program,
    normalize_event,
    normalize_final_state,
    r58_restricted_compiled_boundary_cases,
    run_spec_program,
    validate_program_contract,
    validate_surface_literals,
    verify_program,
)
from exec_trace import TraceInterpreter
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R58_origin_restricted_stack_bytecode_lowering_contract_gate"


ALLOWED_OPCODES: frozenset[BytecodeOpcode] = frozenset(
    {
        BytecodeOpcode.CONST_I32,
        BytecodeOpcode.CONST_ADDR,
        BytecodeOpcode.DUP,
        BytecodeOpcode.POP,
        BytecodeOpcode.ADD_I32,
        BytecodeOpcode.SUB_I32,
        BytecodeOpcode.EQ_I32,
        BytecodeOpcode.LOAD_STATIC,
        BytecodeOpcode.STORE_STATIC,
        BytecodeOpcode.LOAD_INDIRECT,
        BytecodeOpcode.STORE_INDIRECT,
        BytecodeOpcode.JMP,
        BytecodeOpcode.JZ_ZERO,
        BytecodeOpcode.CALL,
        BytecodeOpcode.RET,
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


def normalized_first_mismatch_step(events_a: tuple[object, ...], events_b: tuple[object, ...]) -> int | None:
    normalized_a = tuple(normalize_event(event) for event in events_a)
    normalized_b = tuple(normalize_event(event) for event in events_b)
    for index, (event_a, event_b) in enumerate(zip(normalized_a, normalized_b)):
        if event_a != event_b:
            return index
    if len(normalized_a) != len(normalized_b):
        return min(len(normalized_a), len(normalized_b))
    return None


def validate_compiled_scope(program: BytecodeProgram) -> tuple[bool, str | None]:
    opcodes = {instruction.opcode for instruction in program.instructions}
    if not opcodes.issubset(ALLOWED_OPCODES):
        return False, "opcode_out_of_scope"
    if any(cell.region == BytecodeMemoryRegion.HEAP for cell in program.memory_layout):
        return False, "heap_region_not_admitted"
    return True, None


def failure_class(row: dict[str, object]) -> str | None:
    if not row["compiled_scope_passed"]:
        return "compiled_scope_break"
    if not row["verifier_passed"]:
        return "verifier_break"
    if not row["spec_contract_passed"]:
        return "spec_contract_break"
    if not row["surface_literal_passed"]:
        return "surface_literal_break"
    if not row["normalized_spec_trace_match"] or not row["normalized_spec_final_state_match"]:
        return "normalized_spec_break"
    if not row["source_to_lowered_trace_match"] or not row["source_to_lowered_final_state_match"]:
        return "lowering_break"
    return None


def assess_gate(exactness_rows: list[dict[str, object]], stop_rule: dict[str, object]) -> dict[str, object]:
    planned_count = len(exactness_rows)
    exact_rows = [row for row in exactness_rows if row["verdict"] == "exact"]
    exact_categories = sorted({str(row["category"]) for row in exact_rows})
    return {
        "lane_verdict": "restricted_stack_bytecode_lowering_supported_narrowly"
        if len(exact_rows) == planned_count
        else "restricted_stack_bytecode_lowering_break",
        "restricted_surface": "typed_stack_bytecode_subset_only",
        "planned_case_count": planned_count,
        "executed_case_count": planned_count,
        "exact_case_count": len(exact_rows),
        "failed_case_count": planned_count - len(exact_rows),
        "planned_category_count": len({str(row["category"]) for row in exactness_rows}),
        "exact_category_count": len(exact_categories),
        "exact_category_ids": exact_categories,
        "claim_ceiling": "bounded_useful_cases_only",
        "stop_rule_triggered": bool(stop_rule["stop_rule_triggered"]),
        "next_required_packet": "r59_origin_compiled_trace_vm_execution_gate",
    }


def build_artifacts() -> tuple[list[dict[str, object]], dict[str, object], dict[str, object], dict[str, object]]:
    cases = r58_restricted_compiled_boundary_cases()
    manifest_rows = [
        {
            "case_order": index + 1,
            "case_id": case.case_id,
            "category": case.category,
            "description": case.description,
            "notes": case.notes,
            "max_steps": case.max_steps,
            "program_name": case.program.name,
        }
        for index, case in enumerate(cases)
    ]

    exactness_rows: list[dict[str, object]] = []
    cost_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for case in cases:
        compiled_scope_passed, compiled_scope_error = validate_compiled_scope(case.program)
        verifier_result = verify_program(case.program)
        spec_contract = validate_program_contract(case.program)
        surface_literal = validate_surface_literals(case.program)
        source_result = BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
        spec_result = run_spec_program(case.program, max_steps=case.max_steps)
        lowered_program = lower_program(case.program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)

        normalized_spec_trace_match = tuple(normalize_event(event) for event in source_result.events) == tuple(
            normalize_event(event) for event in spec_result.events
        )
        normalized_spec_final_state_match = normalize_final_state(source_result.final_state) == normalize_final_state(
            spec_result.final_state
        )
        source_to_lowered_trace_match = tuple(source_result.events) == tuple(lowered_result.events)
        source_to_lowered_final_state_match = source_result.final_state == lowered_result.final_state

        exactness_row = {
            "case_id": case.case_id,
            "category": case.category,
            "description": case.description,
            "notes": case.notes,
            "program_name": case.program.name,
            "executed": True,
            "compiled_scope_passed": compiled_scope_passed,
            "compiled_scope_error_class": compiled_scope_error,
            "verifier_passed": verifier_result.passed,
            "verifier_error_class": verifier_result.error_class,
            "spec_contract_passed": spec_contract.passed,
            "spec_contract_error_class": spec_contract.error_class,
            "surface_literal_passed": surface_literal.passed,
            "surface_literal_error_class": surface_literal.error_class,
            "normalized_spec_trace_match": normalized_spec_trace_match,
            "normalized_spec_final_state_match": normalized_spec_final_state_match,
            "normalized_spec_first_mismatch_step": normalized_first_mismatch_step(source_result.events, spec_result.events),
            "source_to_lowered_trace_match": source_to_lowered_trace_match,
            "source_to_lowered_final_state_match": source_to_lowered_final_state_match,
            "source_to_lowered_first_mismatch_step": normalized_first_mismatch_step(source_result.events, lowered_result.events),
            "source_final_state": normalize_state_dict(source_result.final_state),
            "lowered_final_state": normalize_state_dict(lowered_result.final_state),
            "bytecode_program": serialize_bytecode_program(case.program),
            "lowered_program": serialize_trace_program(lowered_program),
        }
        stop_class = failure_class(exactness_row)
        exactness_row["stop_class"] = stop_class
        exactness_row["verdict"] = "exact" if stop_class is None else "break"
        exactness_rows.append(exactness_row)

        cost_rows.append(
            {
                "case_id": case.case_id,
                "category": case.category,
                "source_instruction_count": len(case.program.instructions),
                "lowered_instruction_count": len(lowered_program.instructions),
                "source_step_count": source_result.final_state.steps,
                "declared_memory_cell_count": len(case.program.memory_layout),
                "opcode_surface": opcode_surface(case.program),
            }
        )

        if first_failure is None and stop_class is not None:
            first_failure = {
                "case_id": case.case_id,
                "category": case.category,
                "stop_class": stop_class,
                "first_mismatch_step": exactness_row["source_to_lowered_first_mismatch_step"],
            }

    category_rollup_rows: list[dict[str, object]] = []
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in exactness_rows:
        grouped[str(row["category"])].append(row)
    for category in sorted(grouped):
        rows = grouped[category]
        category_rollup_rows.append(
            {
                "category": category,
                "planned_case_count": len(rows),
                "exact_case_count": sum(row["verdict"] == "exact" for row in rows),
            }
        )

    stop_rule = {
        "stop_rule_triggered": first_failure is not None,
        "first_failure": first_failure,
        "stop_policy": "stop at first scope, verifier, contract, spec, or lowering exactness break",
    }
    report = {
        "runtime_environment": environment_payload(),
        "exactness_rows": exactness_rows,
        "cost_rows": cost_rows,
        "category_rollup_rows": category_rollup_rows,
    }
    summary = {
        "summary": {
            "current_active_docs_only_stage": "h53_post_h52_compiled_boundary_reentry_packet",
            "current_post_h52_planning_bundle": "f29_post_h52_restricted_compiled_boundary_bundle",
            "active_runtime_lane": "r58_origin_restricted_stack_bytecode_lowering_contract_gate",
            "activation_bundle": "f29_post_h52_restricted_compiled_boundary_bundle",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "preserved_prior_docs_only_closeout": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            "gate": assess_gate(exactness_rows, stop_rule),
        },
        "runtime_environment": environment_payload(),
    }
    return manifest_rows, report, stop_rule, summary


def main() -> None:
    manifest_rows, report, stop_rule, summary = build_artifacts()
    write_json(OUT_DIR / "case_manifest.json", {"rows": manifest_rows})
    write_json(OUT_DIR / "lowering_report.json", report)
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
