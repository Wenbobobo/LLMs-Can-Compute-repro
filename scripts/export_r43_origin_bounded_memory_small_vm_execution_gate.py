"""Export the bounded-memory small-VM execution gate for R43."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from bytecode import (
    BoundedMemoryVMCase,
    BytecodeInterpreter,
    BytecodeMemoryRegion,
    BytecodeOpcode,
    BytecodeProgram,
    first_divergence_step,
    lower_program,
    normalize_event,
    normalize_final_state,
    r43_bounded_memory_vm_cases,
    run_spec_program,
    validate_program_contract,
    validate_surface_literals,
    verify_program,
)
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R43_origin_bounded_memory_small_vm_execution_gate"


ALLOWED_OPCODES: frozenset[BytecodeOpcode] = frozenset(
    {
        BytecodeOpcode.CONST_I32,
        BytecodeOpcode.CONST_ADDR,
        BytecodeOpcode.ADD_I32,
        BytecodeOpcode.SUB_I32,
        BytecodeOpcode.EQ_I32,
        BytecodeOpcode.DUP,
        BytecodeOpcode.POP,
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
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def length_bucket(program_steps: int) -> str:
    if program_steps <= 128:
        return "steps<=128"
    if program_steps <= 256:
        return "129<=steps<=256"
    return "steps>256"


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


def validate_r43_scope(case: BoundedMemoryVMCase) -> tuple[bool, str | None]:
    program = case.program
    opcodes = {instruction.opcode for instruction in program.instructions}
    if not opcodes.issubset(ALLOWED_OPCODES):
        return False, "opcode_out_of_scope"
    if any(cell.region == BytecodeMemoryRegion.HEAP for cell in program.memory_layout):
        return False, "heap_region_not_admitted"

    call_sites = [
        (pc, instruction.arg)
        for pc, instruction in enumerate(program.instructions)
        if instruction.opcode == BytecodeOpcode.CALL
    ]
    if case.family_id != "single_call_return_accumulator" and call_sites:
        return False, "call_surface_not_admitted_for_core_family"
    if case.family_id == "single_call_return_accumulator":
        if len(call_sites) != 1:
            return False, "single_call_return_surface_required"
        call_pc, call_target = call_sites[0]
        if call_target is None or call_target <= call_pc:
            return False, "recursive_or_backward_call_not_admitted"
        if BytecodeOpcode.RET not in opcodes:
            return False, "ret_required_for_single_call_return_surface"
    return True, None


def static_program_row(case: BoundedMemoryVMCase) -> dict[str, object]:
    program = case.program
    opcodes = {instruction.opcode for instruction in program.instructions}
    return {
        "family_id": case.family_id,
        "task_id": case.family_id,
        "family_role": case.family_role,
        "gated_on_previous_exact": case.gated_on_previous_exact,
        "description": case.description,
        "program_name": program.name,
        "comparison_mode": case.comparison_mode,
        "max_steps": case.max_steps,
        "instruction_count": len(program.instructions),
        "opcode_surface": opcode_surface(program),
        "contains_branch": any(op in opcodes for op in {BytecodeOpcode.JMP, BytecodeOpcode.JZ_ZERO}),
        "contains_call": BytecodeOpcode.CALL in opcodes,
        "contains_indirect_memory": any(op in opcodes for op in {BytecodeOpcode.LOAD_INDIRECT, BytecodeOpcode.STORE_INDIRECT}),
        "frame_cell_count": sum(cell.region == BytecodeMemoryRegion.FRAME for cell in program.memory_layout),
        "heap_cell_count": sum(cell.region == BytecodeMemoryRegion.HEAP for cell in program.memory_layout),
        "layout_cell_count": len(program.memory_layout),
        "surface_literal_passed": None,
        "surface_literal_error_class": None,
        "scope_passed": None,
        "scope_error_class": None,
        "program_steps": None,
        "length_bucket": None,
        "free_running_read_count": None,
        "free_running_stack_read_count": None,
        "free_running_memory_read_count": None,
        "free_running_call_read_count": None,
        "executed": False,
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


def assess_gate(exactness_rows: list[dict[str, object]], stop_rule: dict[str, object]) -> dict[str, object]:
    executed_rows = [row for row in exactness_rows if row["executed"]]
    planned_count = len(exactness_rows)
    executed_count = len(executed_rows)
    exact_count = sum(row["verdict"] == "exact" for row in executed_rows)
    exact_core_count = sum(row["verdict"] == "exact" and row["family_role"] == "core" for row in executed_rows)
    optional_rows = [row for row in exactness_rows if row["family_role"] == "gated_optional"]
    optional_executed = any(row["executed"] for row in optional_rows)
    optional_exact = any(row["executed"] and row["verdict"] == "exact" for row in optional_rows)

    if exact_count == planned_count and executed_count == planned_count:
        lane_verdict = "keep_semantic_boundary_route"
    elif exact_core_count == 4 and stop_rule["first_failure"] is not None:
        lane_verdict = "mixed_nonunique"
    else:
        lane_verdict = "bounded_memory_vm_break"

    return {
        "lane_verdict": lane_verdict,
        "planned_family_count": planned_count,
        "executed_family_count": executed_count,
        "exact_family_count": exact_count,
        "exact_core_family_count": exact_core_count,
        "optional_call_family_executed": optional_executed,
        "optional_call_family_exact": optional_exact,
        "stop_rule_triggered": bool(stop_rule["stop_rule_triggered"]),
        "later_explicit_packet_required": True,
        "conditional_next_runtime_candidate": "r45_origin_dual_mode_model_mainline_gate"
        if lane_verdict == "keep_semantic_boundary_route"
        else "none",
        "later_explicit_followup_packet": "h42_post_r43_route_selection_packet",
    }


def build_artifacts() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    cases = r43_bounded_memory_vm_cases()
    manifest_rows = [
        {
            "family_order": index + 1,
            "family_id": case.family_id,
            "task_id": case.family_id,
            "family_role": case.family_role,
            "gated_on_previous_exact": case.gated_on_previous_exact,
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
            "program_name": case.program.name,
            "description": case.description,
        }
        for index, case in enumerate(cases)
    ]
    program_rows = [static_program_row(case) for case in cases]
    exactness_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None
    core_exact_count = 0

    for index, case in enumerate(cases):
        if first_failure is not None:
            exactness_rows.append(
                {
                    "family_id": case.family_id,
                    "task_id": case.family_id,
                    "family_role": case.family_role,
                    "executed": False,
                    "gated_on_previous_exact": case.gated_on_previous_exact,
                    "verdict": "not_executed_after_prior_failure",
                    "stop_class": None,
                    "source_spec_trace_match": None,
                    "source_spec_final_state_match": None,
                    "source_to_lowered_trace_match": None,
                    "source_to_lowered_final_state_match": None,
                    "free_running_trace_match": None,
                    "free_running_final_state_match": None,
                    "first_mismatch_step": None,
                    "failure_reason": None,
                    "source_final_state": None,
                    "lowered_final_state": None,
                    "free_running_final_state": None,
                }
            )
            continue
        if case.gated_on_previous_exact and core_exact_count < 4:
            exactness_rows.append(
                {
                    "family_id": case.family_id,
                    "task_id": case.family_id,
                    "family_role": case.family_role,
                    "executed": False,
                    "gated_on_previous_exact": case.gated_on_previous_exact,
                    "verdict": "not_executed_core_gate_unsatisfied",
                    "stop_class": "core_gate_unsatisfied",
                    "source_spec_trace_match": None,
                    "source_spec_final_state_match": None,
                    "source_to_lowered_trace_match": None,
                    "source_to_lowered_final_state_match": None,
                    "free_running_trace_match": None,
                    "free_running_final_state_match": None,
                    "first_mismatch_step": None,
                    "failure_reason": "core families did not all stay exact before the optional call/return family.",
                    "source_final_state": None,
                    "lowered_final_state": None,
                    "free_running_final_state": None,
                }
            )
            continue

        program = case.program
        verifier_result = verify_program(program)
        spec_contract = validate_program_contract(program)
        surface_literal = validate_surface_literals(program)
        scope_passed, scope_error_class = validate_r43_scope(case)
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

        program_rows[index].update(
            {
                "surface_literal_passed": surface_literal.passed,
                "surface_literal_error_class": surface_literal.error_class,
                "scope_passed": scope_passed,
                "scope_error_class": scope_error_class,
                "program_steps": source_result.final_state.steps,
                "length_bucket": length_bucket(source_result.final_state.steps),
                "free_running_read_count": len(free_running_result.read_observations),
                "free_running_stack_read_count": read_counter.get("stack", 0),
                "free_running_memory_read_count": read_counter.get("memory", 0),
                "free_running_call_read_count": read_counter.get("call", 0),
                "executed": True,
            }
        )

        exactness_row = {
            "family_id": case.family_id,
            "task_id": case.family_id,
            "family_role": case.family_role,
            "executed": True,
            "gated_on_previous_exact": case.gated_on_previous_exact,
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
            "source_program": serialize_bytecode_program(program),
            "lowered_program": serialize_trace_program(lowered_program),
        }
        stop_class = failure_class(exactness_row)
        exactness_row["stop_class"] = stop_class
        exactness_row["verdict"] = "exact" if stop_class is None else "break"
        exactness_rows.append(exactness_row)

        if stop_class is None:
            if case.family_role == "core":
                core_exact_count += 1
        else:
            first_failure = {
                "family_id": case.family_id,
                "task_id": case.family_id,
                "family_role": case.family_role,
                "stop_class": stop_class,
                "first_mismatch_step": free_running_outcome.first_mismatch_step,
                "failure_reason": free_running_outcome.failure_reason,
            }

    stop_rule = {
        "planned_family_count": len(cases),
        "executed_family_count": sum(int(row["executed"]) for row in exactness_rows),
        "stop_rule_triggered": first_failure is not None,
        "first_failure": first_failure,
        "reason": "all executed families stayed exact on source/spec, source/lowered, trace, and final state"
        if first_failure is None
        else "stopped at the first bounded-memory small-VM execution failure",
    }
    return manifest_rows, program_rows, exactness_rows, stop_rule


def main() -> None:
    manifest_rows, program_rows, exactness_rows, stop_rule = build_artifacts()
    gate = assess_gate(exactness_rows, stop_rule)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "execution_manifest.json", {"rows": manifest_rows})
    write_json(OUT_DIR / "program_table.json", {"rows": program_rows})
    write_json(OUT_DIR / "exactness_rows.json", {"rows": exactness_rows})
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": {
                "current_paper_phase": "r43_origin_bounded_memory_small_vm_execution_gate_complete",
                "active_runtime_lane": "r43_origin_bounded_memory_small_vm_execution_gate",
                "activation_packet": "h41_post_r42_aggressive_long_arc_decision_packet",
                "preserved_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
                "current_completed_retrieval_contract_gate": "r42_origin_append_only_memory_retrieval_contract_gate",
                "current_model_mainline_bundle": "f20_post_r42_dual_mode_model_mainline_bundle",
                "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
                "gate": gate,
            },
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
