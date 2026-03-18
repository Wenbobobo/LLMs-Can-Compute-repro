from __future__ import annotations

from exec_trace import TraceInterpreter

from .datasets import StressReferenceCase
from .interpreter import BytecodeInterpreter
from .lowering import lower_program
from .memory_surfaces import analyze_memory_surfaces, verify_memory_surfaces
from .spec_oracle import (
    first_divergence_step,
    normalize_event,
    normalize_final_state,
    run_spec_program,
    validate_program_contract,
    validate_surface_literals,
)
from .verifier import verify_program


def _failure_reason(
    *,
    comparison_mode: str,
    verifier_disagreement: bool,
    trace_match: bool | None,
    final_state_match: bool | None,
    diagnostic_surface_match: bool | None,
) -> str | None:
    if verifier_disagreement:
        return "current verifier and standalone spec contract disagree."
    if comparison_mode == "medium_exact_trace" and trace_match is False:
        return "bytecode, lowered exec_trace, and standalone spec traces do not agree exactly."
    if comparison_mode == "long_exact_final_state" and final_state_match is False:
        return "bytecode, lowered exec_trace, and standalone spec final states do not agree."
    if diagnostic_surface_match is False:
        return "memory-surface diagnostics diverge between the bytecode and lowered paths."
    return None


def _build_spec_row(case: StressReferenceCase, spec_validation, spec_result) -> dict[str, object]:
    if spec_result is None:
        return {
            "program_name": case.program.name,
            "comparison_mode": case.comparison_mode,
            "contract_passed": spec_validation.passed,
            "contract_first_error_pc": spec_validation.first_error_pc,
            "contract_error_class": spec_validation.error_class,
            "halted": None,
            "step_count": None,
            "final_stack": None,
            "final_frame_memory": None,
            "final_heap_memory": None,
            "final_call_stack": None,
        }
    final_state = spec_result.final_state
    return {
        "program_name": case.program.name,
        "comparison_mode": case.comparison_mode,
        "contract_passed": spec_validation.passed,
        "contract_first_error_pc": spec_validation.first_error_pc,
        "contract_error_class": spec_validation.error_class,
        "halted": final_state.halted,
        "step_count": final_state.steps,
        "final_stack": list(final_state.stack),
        "final_frame_memory": [list(item) for item in final_state.frame_memory],
        "final_heap_memory": [list(item) for item in final_state.heap_memory],
        "final_call_stack": list(final_state.call_stack),
    }


def run_stress_reference_case(case: StressReferenceCase) -> dict[str, object]:
    program = case.program
    verifier_result = verify_program(program)
    spec_validation = validate_program_contract(program)
    row: dict[str, object] = {
        "program_name": program.name,
        "suite": case.suite,
        "comparison_mode": case.comparison_mode,
        "verifier_passed": verifier_result.passed,
        "verifier_first_error_pc": verifier_result.first_error_pc,
        "verifier_error_class": verifier_result.error_class,
        "spec_contract_passed": spec_validation.passed,
        "spec_contract_first_error_pc": spec_validation.first_error_pc,
        "spec_contract_error_class": spec_validation.error_class,
        "trace_match_current_lowered": None,
        "trace_match_current_spec": None,
        "trace_match_lowered_spec": None,
        "all_final_state_match": None,
        "first_divergence_step": None,
        "diagnostic_surface_match": None,
        "mismatch_class": None,
        "failure_reason": None,
        "bytecode_step_count": None,
        "lowered_step_count": None,
        "spec_step_count": None,
        "bytecode_halted": None,
        "lowered_halted": None,
        "spec_halted": None,
    }

    if case.comparison_mode == "verifier_negative":
        matched_rejection = (
            verifier_result.passed is False
            and spec_validation.passed is False
            and verifier_result.error_class == spec_validation.error_class
            and verifier_result.first_error_pc == spec_validation.first_error_pc
        )
        row["mismatch_class"] = None if matched_rejection else "verifier_disagreement"
        row["failure_reason"] = None if matched_rejection else "verifier and standalone contract reject differently."
        row["external_reference"] = _build_spec_row(case, spec_validation, None)
        return row

    if case.comparison_mode == "memory_surface_negative":
        surface_result = verify_memory_surfaces(program)
        surface_contract = validate_surface_literals(program)
        matched_rejection = (
            surface_result.passed is False
            and surface_contract.passed is False
            and surface_result.error_class == surface_contract.error_class
            and surface_result.first_error_pc == surface_contract.first_error_pc
        )
        row["surface_verifier_passed"] = surface_result.passed
        row["surface_verifier_first_error_pc"] = surface_result.first_error_pc
        row["surface_verifier_error_class"] = surface_result.error_class
        row["surface_contract_passed"] = surface_contract.passed
        row["surface_contract_first_error_pc"] = surface_contract.first_error_pc
        row["surface_contract_error_class"] = surface_contract.error_class
        row["mismatch_class"] = None if matched_rejection else "diagnostic_surface_disagreement"
        row["failure_reason"] = (
            None if matched_rejection else "current and standalone surface contracts reject differently."
        )
        row["external_reference"] = {
            "program_name": program.name,
            "comparison_mode": case.comparison_mode,
            "contract_passed": surface_contract.passed,
            "contract_first_error_pc": surface_contract.first_error_pc,
            "contract_error_class": surface_contract.error_class,
            "halted": None,
            "step_count": None,
            "final_stack": None,
            "final_frame_memory": None,
            "final_heap_memory": None,
            "final_call_stack": None,
        }
        return row

    verifier_disagreement = (
        verifier_result.passed != spec_validation.passed
        or verifier_result.error_class != spec_validation.error_class
        or verifier_result.first_error_pc != spec_validation.first_error_pc
    )
    if verifier_disagreement or not verifier_result.passed or not spec_validation.passed:
        row["mismatch_class"] = "verifier_disagreement"
        row["failure_reason"] = "current verifier and standalone spec contract disagree before execution."
        row["external_reference"] = _build_spec_row(case, spec_validation, None)
        return row

    bytecode_result = BytecodeInterpreter().run(program, max_steps=case.max_steps)
    lowered_result = TraceInterpreter().run(lower_program(program), max_steps=case.max_steps)
    spec_result = run_spec_program(program, max_steps=case.max_steps)

    trace_match_current_lowered = tuple(normalize_event(event) for event in bytecode_result.events) == tuple(
        normalize_event(event) for event in lowered_result.events
    )
    trace_match_current_spec = tuple(normalize_event(event) for event in bytecode_result.events) == tuple(
        normalize_event(event) for event in spec_result.events
    )
    trace_match_lowered_spec = tuple(normalize_event(event) for event in lowered_result.events) == tuple(
        normalize_event(event) for event in spec_result.events
    )
    final_state_match = (
        normalize_final_state(bytecode_result.final_state)
        == normalize_final_state(lowered_result.final_state)
        == normalize_final_state(spec_result.final_state)
    )
    divergence_step = first_divergence_step(bytecode_result.events, spec_result.events)
    if divergence_step is None:
        divergence_step = first_divergence_step(lowered_result.events, spec_result.events)

    diagnostic_surface_match: bool | None = None
    if case.diagnostic_surface:
        reference_surface = analyze_memory_surfaces(program, bytecode_result)
        lowered_surface = analyze_memory_surfaces(program, lowered_result)
        diagnostic_surface_match = reference_surface == lowered_surface

    mismatch_class: str | None = None
    if case.comparison_mode == "medium_exact_trace" and not (
        trace_match_current_lowered and trace_match_current_spec and trace_match_lowered_spec
    ):
        mismatch_class = "trace_disagreement"
    elif case.comparison_mode == "long_exact_final_state" and not final_state_match:
        mismatch_class = "final_state_disagreement"
    elif diagnostic_surface_match is False:
        mismatch_class = "diagnostic_surface_disagreement"

    row.update(
        {
            "trace_match_current_lowered": trace_match_current_lowered,
            "trace_match_current_spec": trace_match_current_spec,
            "trace_match_lowered_spec": trace_match_lowered_spec,
            "all_final_state_match": final_state_match,
            "first_divergence_step": divergence_step,
            "diagnostic_surface_match": diagnostic_surface_match,
            "mismatch_class": mismatch_class,
            "failure_reason": _failure_reason(
                comparison_mode=case.comparison_mode,
                verifier_disagreement=verifier_disagreement,
                trace_match=trace_match_current_lowered and trace_match_current_spec and trace_match_lowered_spec,
                final_state_match=final_state_match,
                diagnostic_surface_match=diagnostic_surface_match,
            ),
            "bytecode_step_count": bytecode_result.final_state.steps,
            "lowered_step_count": lowered_result.final_state.steps,
            "spec_step_count": spec_result.final_state.steps,
            "bytecode_halted": bytecode_result.final_state.halted,
            "lowered_halted": lowered_result.final_state.halted,
            "spec_halted": spec_result.final_state.halted,
            "external_reference": _build_spec_row(case, spec_validation, spec_result),
        }
    )
    return row


def run_stress_reference_harness(cases: tuple[StressReferenceCase, ...]) -> tuple[dict[str, object], ...]:
    return tuple(run_stress_reference_case(case) for case in cases)
