"""Export the bounded scalar locals-and-flags gate for R40."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bytecode import (
    BytecodeCase,
    BytecodeInterpreter,
    bounded_scalar_family_cases,
    bounded_scalar_family_negative_programs,
    first_divergence_step,
    lower_program,
    normalize_event,
    normalize_final_state,
    run_memory_surface_case,
    run_spec_program,
    validate_program_contract,
    verify_memory_surfaces,
    verify_program,
)
from bytecode.ir import BytecodeOpcode, BytecodeProgram
from bytecode.types import BytecodeMemoryRegion, BytecodeType
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R40_origin_bounded_scalar_locals_and_flags_gate"


@dataclass(frozen=True, slots=True)
class CaseSpec:
    case_id: str
    family_role: str
    fragment: str
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram


CASES: tuple[CaseSpec, ...] = tuple(
    CaseSpec(
        case_id="bounded_scalar_admitted",
        family_role="admitted",
        fragment="explicit_flag_slot_loop",
        comparison_mode=case.comparison_mode,
        max_steps=case.max_steps,
        program=case.program,
    )
    if index == 0
    else CaseSpec(
        case_id="bounded_scalar_boundary",
        family_role="boundary_stress",
        fragment="same_family_longer_multi_local_loop",
        comparison_mode=case.comparison_mode,
        max_steps=case.max_steps,
        program=case.program,
    )
    for index, case in enumerate(bounded_scalar_family_cases())
)


ALLOWED_OPCODES: frozenset[BytecodeOpcode] = frozenset(
    {
        BytecodeOpcode.CONST_I32,
        BytecodeOpcode.ADD_I32,
        BytecodeOpcode.SUB_I32,
        BytecodeOpcode.EQ_I32,
        BytecodeOpcode.LOAD_STATIC,
        BytecodeOpcode.STORE_STATIC,
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


def validate_bounded_scalar_family_scope(program: BytecodeProgram) -> tuple[bool, str]:
    opcodes = {instruction.opcode for instruction in program.instructions}
    if BytecodeOpcode.CONST_ADDR in opcodes:
        return False, "const_addr_not_admitted"
    if BytecodeOpcode.LOAD_INDIRECT in opcodes or BytecodeOpcode.STORE_INDIRECT in opcodes:
        return False, "indirect_memory_not_admitted"
    if not program.memory_layout:
        return False, "memory_layout_required"
    if any(cell.region != BytecodeMemoryRegion.FRAME for cell in program.memory_layout):
        return False, "non_frame_cell_present"
    if any(cell.cell_type not in {BytecodeType.I32, BytecodeType.FLAG} for cell in program.memory_layout):
        return False, "non_scalar_or_non_flag_cell_present"
    if any(cell.allowed_targets for cell in program.memory_layout):
        return False, "allowed_targets_not_admitted"
    if any(cell.alias_group is not None for cell in program.memory_layout):
        return False, "alias_group_not_admitted"
    if not any(cell.cell_type == BytecodeType.FLAG for cell in program.memory_layout):
        return False, "flag_slot_required"
    return True, "ok"


def exact_source_rows(rows: list[dict[str, object]], role: str) -> int:
    return sum(
        bool(row["family_role"] == role)
        and bool(row["verifier_passed"])
        and bool(row["spec_contract_passed"])
        and bool(row["spec_reference_trace_match"])
        and bool(row["spec_reference_final_state_match"])
        and bool(row["family_scope_passed"])
        and bool(row["memory_surface_verifier_passed"])
        and bool(row["memory_surface_match"])
        for row in rows
    )


def exact_lowering_rows(rows: list[dict[str, object]], role: str) -> int:
    return sum(
        bool(row["family_role"] == role)
        and bool(row["source_to_lowered_trace_match"])
        and bool(row["source_to_lowered_final_state_match"])
        for row in rows
    )


def exact_execution_rows(rows: list[dict[str, object]], role: str) -> int:
    return sum(
        bool(row["family_role"] == role)
        and bool(row["free_running_trace_match"])
        and bool(row["free_running_final_state_match"])
        for row in rows
    )


def build_rows() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    source_rows: list[dict[str, object]] = []
    lowering_rows: list[dict[str, object]] = []
    execution_rows: list[dict[str, object]] = []
    negative_rows: list[dict[str, object]] = []

    for case in CASES:
        verifier_result = verify_program(case.program)
        spec_contract = validate_program_contract(case.program)
        spec_result = run_spec_program(case.program)
        source_result = BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
        lowered_program = lower_program(case.program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
        max_steps = max(source_result.final_state.steps + 8, case.max_steps)
        free_running_result = run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=max_steps)
        free_running_outcome = compare_execution_to_reference(
            lowered_program,
            free_running_result,
            reference=reference_wrapper(lowered_program, lowered_result),
        )
        read_counter = Counter(observation.space for observation in free_running_result.read_observations)
        memory_row = run_memory_surface_case(
            BytecodeCase(
                suite="bounded_scalar_family",
                comparison_mode=case.comparison_mode,
                max_steps=case.max_steps,
                program=case.program,
            )
        )

        spec_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in source_result.events
        )
        spec_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            source_result.final_state
        )
        source_to_lowered_trace_match = tuple(source_result.events) == tuple(lowered_result.events)
        source_to_lowered_final_state_match = source_result.final_state == lowered_result.final_state
        family_scope_passed, family_scope_error = validate_bounded_scalar_family_scope(case.program)
        flag_cell_count = sum(cell.cell_type == BytecodeType.FLAG for cell in case.program.memory_layout)

        source_rows.append(
            {
                "case_id": case.case_id,
                "family_role": case.family_role,
                "fragment": case.fragment,
                "comparison_mode": case.comparison_mode,
                "program_name": case.program.name,
                "instruction_count": len(case.program.instructions),
                "program_steps": source_result.final_state.steps,
                "opcode_surface": opcode_surface(case.program),
                "flag_cell_count": flag_cell_count,
                "frame_cell_count": sum(cell.region == BytecodeMemoryRegion.FRAME for cell in case.program.memory_layout),
                "heap_cell_count": sum(cell.region == BytecodeMemoryRegion.HEAP for cell in case.program.memory_layout),
                "family_scope_passed": family_scope_passed,
                "family_scope_error": None if family_scope_passed else family_scope_error,
                "verifier_passed": verifier_result.passed,
                "verifier_error_class": verifier_result.error_class,
                "spec_contract_passed": spec_contract.passed,
                "spec_contract_error_class": spec_contract.error_class,
                "spec_reference_trace_match": spec_trace_match,
                "spec_reference_final_state_match": spec_final_state_match,
                "spec_reference_first_mismatch_step": first_divergence_step(spec_result.events, source_result.events),
                "memory_surface_verifier_passed": memory_row.memory_surface_verifier_passed,
                "memory_surface_error_class": memory_row.memory_surface_error_class,
                "memory_surface_match": memory_row.memory_surface_match,
                "touched_frame_addresses": list(memory_row.touched_frame_addresses),
                "touched_heap_addresses": list(memory_row.touched_heap_addresses),
                "boundary_snapshot_count": memory_row.boundary_snapshot_count,
                "source_program": serialize_bytecode_program(case.program),
                "source_final_state": normalize_state_dict(source_result.final_state),
            }
        )

        lowering_rows.append(
            {
                "case_id": case.case_id,
                "family_role": case.family_role,
                "program_name": case.program.name,
                "lowered_instruction_count": len(lowered_program.instructions),
                "lowered_program": serialize_trace_program(lowered_program),
                "source_to_lowered_trace_match": source_to_lowered_trace_match,
                "source_to_lowered_final_state_match": source_to_lowered_final_state_match,
                "source_to_lowered_first_mismatch_step": first_divergence_step(source_result.events, lowered_result.events),
                "lowered_final_state": normalize_state_dict(lowered_result.final_state),
            }
        )

        execution_rows.append(
            {
                "case_id": case.case_id,
                "family_role": case.family_role,
                "program_name": case.program.name,
                "max_steps": max_steps,
                "free_running_trace_match": free_running_outcome.exact_trace_match,
                "free_running_final_state_match": free_running_outcome.exact_final_state_match,
                "free_running_first_mismatch_step": free_running_outcome.first_mismatch_step,
                "free_running_failure_reason": free_running_outcome.failure_reason,
                "free_running_read_count": len(free_running_result.read_observations),
                "free_running_stack_read_count": read_counter.get("stack", 0),
                "free_running_memory_read_count": read_counter.get("memory", 0),
                "free_running_call_read_count": read_counter.get("call", 0),
                "free_running_stack_strategy": free_running_result.stack_strategy,
                "free_running_memory_strategy": free_running_result.memory_strategy,
                "free_running_final_state": normalize_state_dict(free_running_result.final_state),
            }
        )

    negative_programs = bounded_scalar_family_negative_programs()
    negative_cases = (
        ("invalid_flag_branch", "non_flag_branch_operand", negative_programs[0]),
        ("invalid_flag_layout", "layout_type_mismatch", negative_programs[1]),
        ("invalid_heap_escape", "family_scope_escape", negative_programs[2]),
    )
    for case_id, fragment, program in negative_cases:
        verifier_result = verify_program(program)
        spec_contract = validate_program_contract(program)
        memory_verification = verify_memory_surfaces(program)
        family_scope_passed, family_scope_error = validate_bounded_scalar_family_scope(program)
        rejected = (
            not verifier_result.passed
            or not spec_contract.passed
            or not memory_verification.passed
            or not family_scope_passed
        )
        negative_rows.append(
            {
                "case_id": case_id,
                "fragment": fragment,
                "program_name": program.name,
                "opcode_surface": opcode_surface(program),
                "verifier_passed": verifier_result.passed,
                "verifier_error_class": verifier_result.error_class,
                "spec_contract_passed": spec_contract.passed,
                "spec_contract_error_class": spec_contract.error_class,
                "memory_surface_verifier_passed": memory_verification.passed,
                "memory_surface_error_class": memory_verification.error_class,
                "family_scope_passed": family_scope_passed,
                "family_scope_error": None if family_scope_passed else family_scope_error,
                "rejected_by_r40": rejected,
                "source_program": serialize_bytecode_program(program),
            }
        )

    return source_rows, lowering_rows, execution_rows, negative_rows


def build_summary(
    source_rows: list[dict[str, object]],
    lowering_rows: list[dict[str, object]],
    execution_rows: list[dict[str, object]],
    negative_rows: list[dict[str, object]],
) -> dict[str, object]:
    opcode_union = {opcode for row in source_rows for opcode in row["opcode_surface"]}  # type: ignore[index]
    allowed_surface = {opcode.value for opcode in ALLOWED_OPCODES}
    same_opcode_surface_kept = opcode_union <= allowed_surface
    positive_count = len(source_rows)
    negative_count = len(negative_rows)
    admitted_source_exact_count = exact_source_rows(source_rows, "admitted")
    boundary_source_exact_count = exact_source_rows(source_rows, "boundary_stress")
    admitted_lowering_exact_count = exact_lowering_rows(lowering_rows, "admitted")
    boundary_lowering_exact_count = exact_lowering_rows(lowering_rows, "boundary_stress")
    admitted_execution_exact_count = exact_execution_rows(execution_rows, "admitted")
    boundary_execution_exact_count = exact_execution_rows(execution_rows, "boundary_stress")
    lane_passed = (
        same_opcode_surface_kept
        and admitted_source_exact_count == 1
        and boundary_source_exact_count == 1
        and admitted_lowering_exact_count == 1
        and boundary_lowering_exact_count == 1
        and admitted_execution_exact_count == 1
        and boundary_execution_exact_count == 1
        and sum(bool(row["memory_surface_verifier_passed"]) for row in source_rows) == positive_count
        and sum(bool(row["family_scope_passed"]) for row in source_rows) == positive_count
        and sum(bool(row["rejected_by_r40"]) for row in negative_rows) == negative_count
    )
    return {
        "current_paper_phase": "r40_origin_bounded_scalar_locals_and_flags_gate_complete",
        "active_runtime_lane": "r40_origin_bounded_scalar_locals_and_flags_gate",
        "gate": {
            "lane_verdict": "origin_bounded_scalar_locals_and_flags_supported_narrowly"
            if lane_passed
            else "origin_bounded_scalar_locals_and_flags_mixed",
            "same_opcode_surface_kept": same_opcode_surface_kept,
            "admitted_case_count": sum(row["family_role"] == "admitted" for row in source_rows),
            "boundary_stress_case_count": sum(row["family_role"] == "boundary_stress" for row in source_rows),
            "admitted_source_reference_exact_count": admitted_source_exact_count,
            "admitted_lowering_exact_count": admitted_lowering_exact_count,
            "admitted_free_running_exact_count": admitted_execution_exact_count,
            "boundary_source_reference_exact_count": boundary_source_exact_count,
            "boundary_lowering_exact_count": boundary_lowering_exact_count,
            "boundary_free_running_exact_count": boundary_execution_exact_count,
            "flag_slot_case_count": sum(int(row["flag_cell_count"]) > 0 for row in source_rows),
            "memory_surface_verifier_pass_count": sum(bool(row["memory_surface_verifier_passed"]) for row in source_rows),
            "family_scope_pass_count": sum(bool(row["family_scope_passed"]) for row in source_rows),
            "negative_control_count": negative_count,
            "negative_control_rejection_count": sum(bool(row["rejected_by_r40"]) for row in negative_rows),
            "family_scope_rejection_count": sum(not bool(row["family_scope_passed"]) for row in negative_rows),
            "memory_surface_negative_count": sum(not bool(row["memory_surface_verifier_passed"]) for row in negative_rows),
            "opcode_surface": sorted(opcode_union),
            "admitted_program_name": next(row["program_name"] for row in source_rows if row["family_role"] == "admitted"),
            "boundary_program_name": next(
                row["program_name"] for row in source_rows if row["family_role"] == "boundary_stress"
            ),
            "next_priority_lane": "h36_post_r40_bounded_scalar_family_refreeze",
        },
    }


def main() -> None:
    source_rows, lowering_rows, execution_rows, negative_rows = build_rows()
    summary = build_summary(source_rows, lowering_rows, execution_rows, negative_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "source_case_rows.json", {"rows": source_rows})
    write_json(OUT_DIR / "lowering_rows.json", {"rows": lowering_rows})
    write_json(OUT_DIR / "execution_rows.json", {"rows": execution_rows})
    write_json(OUT_DIR / "negative_control_rows.json", {"rows": negative_rows})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
