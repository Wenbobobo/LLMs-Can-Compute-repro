"""Export the narrow post-H31 control-surface extension gate for R38."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bytecode import (
    BytecodeInterpreter,
    first_divergence_step,
    lower_program,
    normalize_event,
    normalize_final_state,
    run_spec_program,
    subroutine_braid_long_program,
    subroutine_braid_program,
    validate_program_contract,
    verify_program,
)
from bytecode.ir import BytecodeOpcode, BytecodeProgram
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R38_origin_compiler_control_surface_extension_gate"


@dataclass(frozen=True, slots=True)
class CaseSpec:
    case_id: str
    fragment: str
    program: BytecodeProgram
    admission_role: str


CASES: tuple[CaseSpec, ...] = (
    CaseSpec(
        case_id="subroutine_braid_admitted",
        fragment="single_richer_control_call_family",
        program=subroutine_braid_program(6, base_address=80),
        admission_role="admitted",
    ),
    CaseSpec(
        case_id="subroutine_braid_long_boundary",
        fragment="same_family_long_boundary_probe",
        program=subroutine_braid_long_program(12, base_address=160),
        admission_role="boundary_stress",
    ),
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


def contains_loop(program: BytecodeProgram) -> bool:
    for pc, instruction in enumerate(program.instructions):
        if instruction.opcode == BytecodeOpcode.JMP and instruction.arg is not None and instruction.arg <= pc:
            return True
    return False


def contains_branch(program: BytecodeProgram) -> bool:
    return any(instruction.opcode == BytecodeOpcode.JZ_ZERO for instruction in program.instructions)


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


def build_rows() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    source_rows: list[dict[str, object]] = []
    lowering_rows: list[dict[str, object]] = []
    execution_rows: list[dict[str, object]] = []

    for case in CASES:
        verifier_result = verify_program(case.program)
        spec_contract = validate_program_contract(case.program)
        spec_result = run_spec_program(case.program)
        source_result = BytecodeInterpreter().run(case.program)
        lowered_program = lower_program(case.program)
        lowered_result = TraceInterpreter().run(lowered_program)
        max_steps = max(source_result.final_state.steps + 8, 64)
        free_running_result = run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=max_steps)
        free_running_outcome = compare_execution_to_reference(
            lowered_program,
            free_running_result,
            reference=reference_wrapper(lowered_program, lowered_result),
        )
        read_counter = Counter(observation.space for observation in free_running_result.read_observations)

        spec_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in source_result.events
        )
        spec_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            source_result.final_state
        )
        source_to_lowered_trace_match = tuple(source_result.events) == tuple(lowered_result.events)
        source_to_lowered_final_state_match = source_result.final_state == lowered_result.final_state

        source_rows.append(
            {
                "case_id": case.case_id,
                "fragment": case.fragment,
                "program_name": case.program.name,
                "admission_role": case.admission_role,
                "instruction_count": len(case.program.instructions),
                "program_steps": source_result.final_state.steps,
                "contains_branch": contains_branch(case.program),
                "contains_loop": contains_loop(case.program),
                "contains_call": True,
                "opcode_surface": opcode_surface(case.program),
                "source_program": serialize_bytecode_program(case.program),
                "verifier_passed": verifier_result.passed,
                "verifier_error_class": verifier_result.error_class,
                "spec_contract_passed": spec_contract.passed,
                "spec_contract_error_class": spec_contract.error_class,
                "spec_reference_trace_match": spec_trace_match,
                "spec_reference_final_state_match": spec_final_state_match,
                "spec_reference_first_mismatch_step": first_divergence_step(spec_result.events, source_result.events),
                "source_final_state": normalize_state_dict(source_result.final_state),
            }
        )

        lowering_rows.append(
            {
                "case_id": case.case_id,
                "fragment": case.fragment,
                "program_name": case.program.name,
                "admission_role": case.admission_role,
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
                "fragment": case.fragment,
                "program_name": case.program.name,
                "admission_role": case.admission_role,
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

    return source_rows, lowering_rows, execution_rows


def exact_source_rows(rows: list[dict[str, object]], role: str) -> int:
    return sum(
        bool(row["admission_role"] == role)
        and bool(row["verifier_passed"])
        and bool(row["spec_contract_passed"])
        and bool(row["spec_reference_trace_match"])
        and bool(row["spec_reference_final_state_match"])
        for row in rows
    )


def exact_lowering_rows(rows: list[dict[str, object]], role: str) -> int:
    return sum(
        bool(row["admission_role"] == role)
        and bool(row["source_to_lowered_trace_match"])
        and bool(row["source_to_lowered_final_state_match"])
        for row in rows
    )


def exact_execution_rows(rows: list[dict[str, object]], role: str) -> int:
    return sum(
        bool(row["admission_role"] == role)
        and bool(row["free_running_trace_match"])
        and bool(row["free_running_final_state_match"])
        for row in rows
    )


def build_summary(
    source_rows: list[dict[str, object]],
    lowering_rows: list[dict[str, object]],
    execution_rows: list[dict[str, object]],
) -> dict[str, object]:
    opcode_union = {opcode for row in source_rows for opcode in row["opcode_surface"]}  # type: ignore[index]
    allowed_surface = {opcode.value for opcode in ALLOWED_OPCODES}
    narrow_scope_kept = opcode_union == allowed_surface
    admitted_source_ok = exact_source_rows(source_rows, "admitted") == 1
    admitted_lowering_ok = exact_lowering_rows(lowering_rows, "admitted") == 1
    admitted_execution_ok = exact_execution_rows(execution_rows, "admitted") == 1
    lane_passed = narrow_scope_kept and admitted_source_ok and admitted_lowering_ok and admitted_execution_ok

    return {
        "current_paper_phase": "r38_origin_compiler_control_surface_extension_gate_complete",
        "active_runtime_lane": "r38_origin_compiler_control_surface_extension_gate",
        "gate": {
            "lane_verdict": "origin_compiler_control_surface_extension_supported_narrowly"
            if lane_passed
            else "origin_compiler_control_surface_extension_mixed",
            "narrow_scope_kept": narrow_scope_kept,
            "r37_opcode_surface_matches": narrow_scope_kept,
            "admitted_case_count": sum(row["admission_role"] == "admitted" for row in source_rows),
            "boundary_stress_case_count": sum(row["admission_role"] == "boundary_stress" for row in source_rows),
            "verifier_pass_count": sum(bool(row["verifier_passed"]) for row in source_rows),
            "spec_contract_pass_count": sum(bool(row["spec_contract_passed"]) for row in source_rows),
            "admitted_source_reference_exact_count": exact_source_rows(source_rows, "admitted"),
            "admitted_lowering_exact_count": exact_lowering_rows(lowering_rows, "admitted"),
            "admitted_free_running_exact_count": exact_execution_rows(execution_rows, "admitted"),
            "boundary_source_reference_exact_count": exact_source_rows(source_rows, "boundary_stress"),
            "boundary_lowering_exact_count": exact_lowering_rows(lowering_rows, "boundary_stress"),
            "boundary_free_running_exact_count": exact_execution_rows(execution_rows, "boundary_stress"),
            "opcode_surface": sorted(opcode_union),
            "admitted_program_name": next(
                row["program_name"] for row in source_rows if row["admission_role"] == "admitted"
            ),
            "boundary_program_name": next(
                row["program_name"] for row in source_rows if row["admission_role"] == "boundary_stress"
            ),
            "next_priority_lane": "h32_post_r38_compiled_boundary_refreeze",
        },
    }


def main() -> None:
    source_rows, lowering_rows, execution_rows = build_rows()
    failure_rows = [
        {
            "case_id": row["case_id"],
            "admission_role": row["admission_role"],
            "phase": "source"
            if not (
                bool(row.get("verifier_passed"))
                and bool(row.get("spec_contract_passed"))
                and bool(row.get("spec_reference_trace_match"))
                and bool(row.get("spec_reference_final_state_match"))
            )
            else "lowering",
            "failure_reason": row.get("verifier_error_class")
            or row.get("spec_contract_error_class")
            or row.get("spec_reference_first_mismatch_step")
            or row.get("source_to_lowered_first_mismatch_step"),
        }
        for row in source_rows + lowering_rows
        if not (
            bool(row.get("verifier_passed", True))
            and bool(row.get("spec_contract_passed", True))
            and bool(row.get("spec_reference_trace_match", True))
            and bool(row.get("spec_reference_final_state_match", True))
            and bool(row.get("source_to_lowered_trace_match", True))
            and bool(row.get("source_to_lowered_final_state_match", True))
        )
    ]
    failure_rows.extend(
        {
            "case_id": row["case_id"],
            "admission_role": row["admission_role"],
            "phase": "execution",
            "failure_reason": row["free_running_failure_reason"] or row["free_running_first_mismatch_step"],
        }
        for row in execution_rows
        if not (bool(row["free_running_trace_match"]) and bool(row["free_running_final_state_match"]))
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "source_case_rows.json", {"rows": source_rows})
    write_json(OUT_DIR / "lowering_audit_rows.json", {"rows": lowering_rows})
    write_json(OUT_DIR / "execution_rows.json", {"rows": execution_rows})
    write_json(OUT_DIR / "failure_rows.json", {"rows": failure_rows})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": build_summary(source_rows, lowering_rows, execution_rows),
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
