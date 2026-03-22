"""Export the narrow same-substrate control-surface dependency audit for R39."""

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
    subroutine_braid_long_permuted_helpers_program,
    subroutine_braid_long_program,
    subroutine_braid_permuted_helpers_program,
    subroutine_braid_program,
    validate_program_contract,
    verify_program,
)
from bytecode.ir import BytecodeOpcode, BytecodeProgram
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R39_origin_compiler_control_surface_dependency_audit"


@dataclass(frozen=True, slots=True)
class CaseSpec:
    case_id: str
    family_role: str
    control_surface_variant: str
    perturbation_name: str
    program: BytecodeProgram


CASES: tuple[CaseSpec, ...] = (
    CaseSpec(
        case_id="subroutine_braid_admitted_baseline",
        family_role="admitted",
        control_surface_variant="baseline",
        perturbation_name="none",
        program=subroutine_braid_program(6, base_address=80),
    ),
    CaseSpec(
        case_id="subroutine_braid_admitted_permuted",
        family_role="admitted",
        control_surface_variant="helper_body_permuted_targets_renumbered",
        perturbation_name="helper_body_permutation_with_target_renumbering",
        program=subroutine_braid_permuted_helpers_program(6, base_address=80),
    ),
    CaseSpec(
        case_id="subroutine_braid_boundary_baseline",
        family_role="boundary_stress",
        control_surface_variant="baseline",
        perturbation_name="none",
        program=subroutine_braid_long_program(12, base_address=160),
    ),
    CaseSpec(
        case_id="subroutine_braid_boundary_permuted",
        family_role="boundary_stress",
        control_surface_variant="helper_body_permuted_targets_renumbered",
        perturbation_name="helper_body_permutation_with_target_renumbering",
        program=subroutine_braid_long_permuted_helpers_program(12, base_address=160),
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
    return any(
        instruction.opcode == BytecodeOpcode.JMP and instruction.arg is not None and instruction.arg <= pc
        for pc, instruction in enumerate(program.instructions)
    )


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


def event_count(events: tuple[Any, ...], opcode: str) -> int:
    return sum(getattr(event.opcode, "value", event.opcode) == opcode for event in events)


def first_event_divergence_step(left: tuple[Any, ...], right: tuple[Any, ...]) -> int | None:
    for produced, expected in zip(left, right):
        if produced != expected:
            return int(produced.step)
    if len(left) != len(right):
        return min(len(left), len(right))
    return None


def exact_source_rows(rows: list[dict[str, object]], variant: str) -> int:
    return sum(
        bool(row["control_surface_variant"] == variant)
        and bool(row["verifier_passed"])
        and bool(row["spec_contract_passed"])
        and bool(row["spec_reference_trace_match"])
        and bool(row["spec_reference_final_state_match"])
        for row in rows
    )


def exact_lowering_rows(rows: list[dict[str, object]], variant: str) -> int:
    return sum(
        bool(row["control_surface_variant"] == variant)
        and bool(row["source_to_lowered_trace_match"])
        and bool(row["source_to_lowered_final_state_match"])
        for row in rows
    )


def exact_execution_rows(rows: list[dict[str, object]], variant: str) -> int:
    return sum(
        bool(row["control_surface_variant"] == variant)
        and bool(row["free_running_trace_match"])
        and bool(row["free_running_final_state_match"])
        for row in rows
    )


def build_rows() -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    source_rows: list[dict[str, object]] = []
    lowering_rows: list[dict[str, object]] = []
    execution_rows: list[dict[str, object]] = []
    comparison_rows: list[dict[str, object]] = []

    source_by_family_variant: dict[tuple[str, str], tuple[Any, Any]] = {}
    lowered_by_family_variant: dict[tuple[str, str], tuple[Any, Any]] = {}
    execution_by_family_variant: dict[tuple[str, str], FreeRunningExecutionResult] = {}

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

        source_by_family_variant[(case.family_role, case.control_surface_variant)] = (case.program, source_result)
        lowered_by_family_variant[(case.family_role, case.control_surface_variant)] = (lowered_program, lowered_result)
        execution_by_family_variant[(case.family_role, case.control_surface_variant)] = free_running_result

        source_rows.append(
            {
                "case_id": case.case_id,
                "family_role": case.family_role,
                "control_surface_variant": case.control_surface_variant,
                "perturbation_name": case.perturbation_name,
                "program_name": case.program.name,
                "instruction_count": len(case.program.instructions),
                "program_steps": source_result.final_state.steps,
                "contains_branch": contains_branch(case.program),
                "contains_loop": contains_loop(case.program),
                "contains_call": True,
                "call_event_count": event_count(source_result.events, "call"),
                "ret_event_count": event_count(source_result.events, "ret"),
                "conditional_branch_event_count": event_count(source_result.events, "jz_zero"),
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
                "family_role": case.family_role,
                "control_surface_variant": case.control_surface_variant,
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
                "control_surface_variant": case.control_surface_variant,
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

    for family_role in ("admitted", "boundary_stress"):
        baseline_program, baseline_source = source_by_family_variant[(family_role, "baseline")]
        perturbed_program, perturbed_source = source_by_family_variant[
            (family_role, "helper_body_permuted_targets_renumbered")
        ]
        baseline_execution = execution_by_family_variant[(family_role, "baseline")]
        perturbed_execution = execution_by_family_variant[(family_role, "helper_body_permuted_targets_renumbered")]
        baseline_read_counter = Counter(observation.space for observation in baseline_execution.read_observations)
        perturbed_read_counter = Counter(observation.space for observation in perturbed_execution.read_observations)

        comparison_rows.append(
            {
                "family_role": family_role,
                "perturbation_name": "helper_body_permutation_with_target_renumbering",
                "baseline_program_name": baseline_program.name,
                "perturbed_program_name": perturbed_program.name,
                "same_final_state_as_baseline": baseline_source.final_state == perturbed_source.final_state,
                "same_trace_as_baseline": tuple(baseline_source.events) == tuple(perturbed_source.events),
                "first_trace_divergence_step": first_event_divergence_step(
                    tuple(perturbed_source.events),
                    tuple(baseline_source.events),
                ),
                "same_instruction_count_as_baseline": len(baseline_program.instructions)
                == len(perturbed_program.instructions),
                "same_program_steps_as_baseline": baseline_source.final_state.steps == perturbed_source.final_state.steps,
                "same_call_event_count_as_baseline": event_count(baseline_source.events, "call")
                == event_count(perturbed_source.events, "call"),
                "same_ret_event_count_as_baseline": event_count(baseline_source.events, "ret")
                == event_count(perturbed_source.events, "ret"),
                "same_conditional_branch_count_as_baseline": event_count(baseline_source.events, "jz_zero")
                == event_count(perturbed_source.events, "jz_zero"),
                "same_read_count_as_baseline": len(baseline_execution.read_observations)
                == len(perturbed_execution.read_observations),
                "same_call_read_count_as_baseline": baseline_read_counter.get("call", 0)
                == perturbed_read_counter.get("call", 0),
                "same_memory_read_count_as_baseline": baseline_read_counter.get("memory", 0)
                == perturbed_read_counter.get("memory", 0),
                "same_stack_read_count_as_baseline": baseline_read_counter.get("stack", 0)
                == perturbed_read_counter.get("stack", 0),
                "baseline_read_count": len(baseline_execution.read_observations),
                "perturbed_read_count": len(perturbed_execution.read_observations),
                "baseline_call_read_count": baseline_read_counter.get("call", 0),
                "perturbed_call_read_count": perturbed_read_counter.get("call", 0),
            }
        )

    return source_rows, lowering_rows, execution_rows, comparison_rows


def build_failure_rows(
    source_rows: list[dict[str, object]],
    lowering_rows: list[dict[str, object]],
    execution_rows: list[dict[str, object]],
    comparison_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for row in source_rows:
        if not (
            bool(row["verifier_passed"])
            and bool(row["spec_contract_passed"])
            and bool(row["spec_reference_trace_match"])
            and bool(row["spec_reference_final_state_match"])
        ):
            rows.append(
                {
                    "row_type": "source",
                    "case_id": row["case_id"],
                    "family_role": row["family_role"],
                    "control_surface_variant": row["control_surface_variant"],
                }
            )

    for row in lowering_rows:
        if not (bool(row["source_to_lowered_trace_match"]) and bool(row["source_to_lowered_final_state_match"])):
            rows.append(
                {
                    "row_type": "lowering",
                    "case_id": row["case_id"],
                    "family_role": row["family_role"],
                    "control_surface_variant": row["control_surface_variant"],
                }
            )

    for row in execution_rows:
        if not (bool(row["free_running_trace_match"]) and bool(row["free_running_final_state_match"])):
            rows.append(
                {
                    "row_type": "execution",
                    "case_id": row["case_id"],
                    "family_role": row["family_role"],
                    "control_surface_variant": row["control_surface_variant"],
                }
            )

    for row in comparison_rows:
        if not (
            bool(row["same_final_state_as_baseline"])
            and not bool(row["same_trace_as_baseline"])
            and bool(row["same_instruction_count_as_baseline"])
            and bool(row["same_program_steps_as_baseline"])
            and bool(row["same_call_event_count_as_baseline"])
            and bool(row["same_ret_event_count_as_baseline"])
            and bool(row["same_conditional_branch_count_as_baseline"])
            and bool(row["same_read_count_as_baseline"])
            and bool(row["same_call_read_count_as_baseline"])
            and bool(row["same_memory_read_count_as_baseline"])
            and bool(row["same_stack_read_count_as_baseline"])
        ):
            rows.append(
                {
                    "row_type": "comparison",
                    "family_role": row["family_role"],
                    "perturbation_name": row["perturbation_name"],
                }
            )

    return rows


def build_summary(
    source_rows: list[dict[str, object]],
    lowering_rows: list[dict[str, object]],
    execution_rows: list[dict[str, object]],
    comparison_rows: list[dict[str, object]],
) -> dict[str, object]:
    opcode_union = {opcode for row in source_rows for opcode in row["opcode_surface"]}  # type: ignore[index]
    allowed_surface = {opcode.value for opcode in ALLOWED_OPCODES}
    same_opcode_surface_kept = opcode_union == allowed_surface
    perturbation_source_exact_count = exact_source_rows(source_rows, "helper_body_permuted_targets_renumbered")
    perturbation_lowering_exact_count = exact_lowering_rows(lowering_rows, "helper_body_permuted_targets_renumbered")
    perturbation_execution_exact_count = exact_execution_rows(execution_rows, "helper_body_permuted_targets_renumbered")
    perturbation_final_state_preserved_count = sum(bool(row["same_final_state_as_baseline"]) for row in comparison_rows)
    perturbation_trace_changed_count = sum(not bool(row["same_trace_as_baseline"]) for row in comparison_rows)
    perturbation_workload_preserved_count = sum(
        bool(row["same_instruction_count_as_baseline"])
        and bool(row["same_program_steps_as_baseline"])
        and bool(row["same_call_event_count_as_baseline"])
        and bool(row["same_ret_event_count_as_baseline"])
        and bool(row["same_conditional_branch_count_as_baseline"])
        and bool(row["same_read_count_as_baseline"])
        and bool(row["same_call_read_count_as_baseline"])
        and bool(row["same_memory_read_count_as_baseline"])
        and bool(row["same_stack_read_count_as_baseline"])
        for row in comparison_rows
    )

    lane_passed = (
        same_opcode_surface_kept
        and perturbation_source_exact_count == 2
        and perturbation_lowering_exact_count == 2
        and perturbation_execution_exact_count == 2
        and perturbation_final_state_preserved_count == 2
        and perturbation_trace_changed_count == 2
        and perturbation_workload_preserved_count == 2
    )
    admitted_perturbation_ok = all(
        row["family_role"] != "admitted"
        or (
            bool(row["same_final_state_as_baseline"])
            and not bool(row["same_trace_as_baseline"])
            and bool(row["same_program_steps_as_baseline"])
        )
        for row in comparison_rows
    ) and sum(
        bool(row["family_role"] == "admitted")
        and bool(row["control_surface_variant"] == "helper_body_permuted_targets_renumbered")
        and bool(row["free_running_trace_match"])
        and bool(row["free_running_final_state_match"])
        for row in execution_rows
    ) == 1
    boundary_perturbation_ok = all(
        row["family_role"] != "boundary_stress"
        or (
            bool(row["same_final_state_as_baseline"])
            and not bool(row["same_trace_as_baseline"])
            and bool(row["same_program_steps_as_baseline"])
        )
        for row in comparison_rows
    ) and sum(
        bool(row["family_role"] == "boundary_stress")
        and bool(row["control_surface_variant"] == "helper_body_permuted_targets_renumbered")
        and bool(row["free_running_trace_match"])
        and bool(row["free_running_final_state_match"])
        for row in execution_rows
    ) == 1

    if lane_passed:
        lane_verdict = "control_surface_dependence_not_detected_on_declared_permutation"
    elif admitted_perturbation_ok and not boundary_perturbation_ok:
        lane_verdict = "declared_permutation_survives_admitted_case_boundary_case_mixed"
    else:
        lane_verdict = "control_surface_dependence_detected_on_declared_permutation"

    return {
        "current_paper_phase": "r39_origin_compiler_control_surface_dependency_audit_complete",
        "active_runtime_lane": "r39_origin_compiler_control_surface_dependency_audit",
        "current_active_routing_stage": "h32_post_r38_compiled_boundary_refreeze",
        "current_control_packet": "h33_post_h32_conditional_next_question_packet",
        "gate": {
            "lane_verdict": lane_verdict,
            "declared_perturbation": "helper_body_permutation_with_target_renumbering",
            "same_opcode_surface_kept": same_opcode_surface_kept,
            "baseline_case_count": sum(row["control_surface_variant"] == "baseline" for row in source_rows),
            "perturbation_case_count": sum(
                row["control_surface_variant"] == "helper_body_permuted_targets_renumbered" for row in source_rows
            ),
            "perturbation_source_reference_exact_count": perturbation_source_exact_count,
            "perturbation_lowering_exact_count": perturbation_lowering_exact_count,
            "perturbation_free_running_exact_count": perturbation_execution_exact_count,
            "perturbation_final_state_preserved_count": perturbation_final_state_preserved_count,
            "perturbation_trace_changed_count": perturbation_trace_changed_count,
            "perturbation_workload_preserved_count": perturbation_workload_preserved_count,
            "admitted_perturbation_program_name": next(
                row["program_name"]
                for row in source_rows
                if row["family_role"] == "admitted"
                and row["control_surface_variant"] == "helper_body_permuted_targets_renumbered"
            ),
            "boundary_perturbation_program_name": next(
                row["program_name"]
                for row in source_rows
                if row["family_role"] == "boundary_stress"
                and row["control_surface_variant"] == "helper_body_permuted_targets_renumbered"
            ),
            "next_priority_lane": "later_explicit_post_r39_decision_packet_required",
        },
    }


def main() -> None:
    source_rows, lowering_rows, execution_rows, comparison_rows = build_rows()
    failure_rows = build_failure_rows(source_rows, lowering_rows, execution_rows, comparison_rows)
    summary = build_summary(source_rows, lowering_rows, execution_rows, comparison_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "source_case_rows.json", {"rows": source_rows})
    write_json(OUT_DIR / "lowering_audit_rows.json", {"rows": lowering_rows})
    write_json(OUT_DIR / "execution_rows.json", {"rows": execution_rows})
    write_json(OUT_DIR / "comparison_rows.json", {"rows": comparison_rows})
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
