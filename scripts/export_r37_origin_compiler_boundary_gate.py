"""Export the narrow Origin-core compiled-boundary gate for R37."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bytecode import (
    BytecodeInterpreter,
    accumulator_loop_program,
    arithmetic_smoke_program,
    eq_branch_false_program,
    eq_branch_true_program,
    first_divergence_step,
    loop_with_subroutine_update_program,
    lower_program,
    normalize_event,
    normalize_final_state,
    run_spec_program,
    validate_program_contract,
    verify_program,
)
from bytecode.ir import BytecodeOpcode, BytecodeProgram
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R37_origin_compiler_boundary_gate"


@dataclass(frozen=True, slots=True)
class CaseSpec:
    case_id: str
    fragment: str
    program: BytecodeProgram
    includes_call: bool = False


CASES: tuple[CaseSpec, ...] = (
    CaseSpec(
        case_id="arithmetic_smoke",
        fragment="straight_line_arithmetic",
        program=arithmetic_smoke_program(),
    ),
    CaseSpec(
        case_id="eq_branch_true",
        fragment="single_branch_true_path",
        program=eq_branch_true_program(),
    ),
    CaseSpec(
        case_id="eq_branch_false",
        fragment="single_branch_false_path",
        program=eq_branch_false_program(),
    ),
    CaseSpec(
        case_id="accumulator_loop_static",
        fragment="bounded_loop_with_static_locals",
        program=accumulator_loop_program(6),
    ),
    CaseSpec(
        case_id="loop_with_subroutine_update",
        fragment="bounded_loop_with_one_helper_call",
        program=loop_with_subroutine_update_program(6, counter_address=64, accumulator_address=65),
        includes_call=True,
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
        max_steps = max(source_result.final_state.steps + 4, 32)
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
                "instruction_count": len(case.program.instructions),
                "program_steps": source_result.final_state.steps,
                "contains_branch": contains_branch(case.program),
                "contains_loop": contains_loop(case.program),
                "contains_call": case.includes_call,
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


def build_summary(
    source_rows: list[dict[str, object]],
    lowering_rows: list[dict[str, object]],
    execution_rows: list[dict[str, object]],
) -> dict[str, object]:
    opcode_union = {opcode for row in source_rows for opcode in row["opcode_surface"]}  # type: ignore[index]
    narrow_scope_kept = opcode_union <= {opcode.value for opcode in ALLOWED_OPCODES}
    source_reference_ok = all(
        bool(row["verifier_passed"])
        and bool(row["spec_contract_passed"])
        and bool(row["spec_reference_trace_match"])
        and bool(row["spec_reference_final_state_match"])
        for row in source_rows
    )
    lowering_ok = all(
        bool(row["source_to_lowered_trace_match"]) and bool(row["source_to_lowered_final_state_match"])
        for row in lowering_rows
    )
    execution_ok = all(
        bool(row["free_running_trace_match"]) and bool(row["free_running_final_state_match"])
        for row in execution_rows
    )
    lane_passed = narrow_scope_kept and source_reference_ok and lowering_ok and execution_ok

    return {
        "current_paper_phase": "r37_origin_compiler_boundary_gate_complete",
        "active_runtime_lane": "r37_origin_compiler_boundary_gate",
        "gate": {
            "lane_verdict": "origin_tiny_compiled_boundary_supported_narrowly"
            if lane_passed
            else "origin_tiny_compiled_boundary_mixed",
            "narrow_scope_kept": narrow_scope_kept,
            "admitted_source_case_count": len(source_rows),
            "verifier_pass_count": sum(bool(row["verifier_passed"]) for row in source_rows),
            "spec_contract_pass_count": sum(bool(row["spec_contract_passed"]) for row in source_rows),
            "source_reference_exact_count": sum(
                bool(row["spec_reference_trace_match"]) and bool(row["spec_reference_final_state_match"])
                for row in source_rows
            ),
            "lowering_exact_count": sum(
                bool(row["source_to_lowered_trace_match"]) and bool(row["source_to_lowered_final_state_match"])
                for row in lowering_rows
            ),
            "free_running_exact_count": sum(
                bool(row["free_running_trace_match"]) and bool(row["free_running_final_state_match"])
                for row in execution_rows
            ),
            "call_case_count": sum(bool(row["contains_call"]) for row in source_rows),
            "loop_case_count": sum(bool(row["contains_loop"]) for row in source_rows),
            "branch_case_count": sum(bool(row["contains_branch"]) for row in source_rows),
            "opcode_surface": sorted(opcode_union),
            "next_priority_lane": "h30_post_r36_r37_scope_decision_packet",
        },
    }


def main() -> None:
    source_rows, lowering_rows, execution_rows = build_rows()
    failure_rows = [
        {
            "case_id": row["case_id"],
            "phase": "source"
            if not (
                bool(row.get("verifier_passed"))
                and bool(row.get("spec_contract_passed"))
                and bool(row.get("spec_reference_trace_match"))
                and bool(row.get("spec_reference_final_state_match"))
            )
            else "lowering",
        }
        for row in source_rows
        if not (
            bool(row["verifier_passed"])
            and bool(row["spec_contract_passed"])
            and bool(row["spec_reference_trace_match"])
            and bool(row["spec_reference_final_state_match"])
        )
    ]
    failure_rows.extend(
        {
            "case_id": row["case_id"],
            "phase": "lowering",
        }
        for row in lowering_rows
        if not (bool(row["source_to_lowered_trace_match"]) and bool(row["source_to_lowered_final_state_match"]))
    )
    failure_rows.extend(
        {
            "case_id": row["case_id"],
            "phase": "free_running",
            "failure_reason": row["free_running_failure_reason"],
            "first_mismatch_step": row["free_running_first_mismatch_step"],
        }
        for row in execution_rows
        if not (bool(row["free_running_trace_match"]) and bool(row["free_running_final_state_match"]))
    )
    summary = build_summary(source_rows, lowering_rows, execution_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "source_case_rows.json", {"rows": source_rows})
    write_json(OUT_DIR / "lowering_audit_rows.json", {"rows": lowering_rows})
    write_json(OUT_DIR / "execution_rows.json", {"rows": execution_rows})
    write_json(OUT_DIR / "failure_rows.json", {"rows": failure_rows})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
