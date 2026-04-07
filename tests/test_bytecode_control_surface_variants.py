from __future__ import annotations

from bytecode import (
    BytecodeCase,
    BytecodeInterpreter,
    lower_program,
    run_harness_case,
    subroutine_braid_long_permuted_helpers_program,
    subroutine_braid_long_program,
    subroutine_braid_permuted_helpers_program,
    subroutine_braid_program,
    validate_program_contract,
    verify_program,
)
from exec_trace import TraceInterpreter


def test_subroutine_braid_permuted_helper_surface_preserves_final_state() -> None:
    cases = (
        (
            subroutine_braid_program(6, base_address=80),
            subroutine_braid_permuted_helpers_program(6, base_address=80),
            256,
        ),
        (
            subroutine_braid_long_program(12, base_address=160),
            subroutine_braid_long_permuted_helpers_program(12, base_address=160),
            768,
        ),
    )

    for baseline, variant, max_steps in cases:
        verifier_result = verify_program(variant)
        contract_result = validate_program_contract(variant)
        baseline_result = BytecodeInterpreter().run(baseline)
        variant_source = BytecodeInterpreter().run(variant)
        variant_lowered = TraceInterpreter().run(lower_program(variant))
        harness_row = run_harness_case(BytecodeCase("control_flow", "exact_trace", max_steps, variant))

        assert verifier_result.passed is True
        assert contract_result.passed is True
        assert variant_source.events == variant_lowered.events
        assert variant_source.final_state == variant_lowered.final_state
        assert variant_source.final_state == baseline_result.final_state
        assert variant_source.events != baseline_result.events
        assert harness_row.trace_match is True
        assert harness_row.final_state_match is True
        assert harness_row.failure_class is None
