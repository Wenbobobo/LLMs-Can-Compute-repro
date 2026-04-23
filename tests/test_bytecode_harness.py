from __future__ import annotations

from bytecode import (
    alternating_memory_loop_bytecode_program,
    arithmetic_smoke_program,
    branch_then_call_false_program,
    branch_then_call_true_program,
    call_add_halt_program,
    call_chain_smoke_program,
    checkpoint_replay_long_program,
    countdown_helper_call_program,
    countdown_loop_program,
    dynamic_latest_write_program,
    eq_branch_false_program,
    eq_branch_true_program,
    indirect_counter_bank_program,
    lower_program,
    loop_with_subroutine_update_program,
    run_harness_case,
    selector_checkpoint_bank_bytecode_program,
    stack_memory_braid_program,
    static_memory_roundtrip_program,
    subroutine_braid_program,
    verifier_negative_programs,
    verify_program,
)
from bytecode.datasets import BytecodeCase
from bytecode.interpreter import BytecodeInterpreter
from exec_trace import TraceInterpreter


def test_verifier_accepts_valid_programs() -> None:
    for program in (
        arithmetic_smoke_program(),
        eq_branch_true_program(),
        eq_branch_false_program(),
        call_add_halt_program(),
        branch_then_call_true_program(),
        branch_then_call_false_program(),
        call_chain_smoke_program(),
        static_memory_roundtrip_program(),
        dynamic_latest_write_program(),
        countdown_loop_program(4),
        countdown_helper_call_program(4, counter_address=48),
        loop_with_subroutine_update_program(6, counter_address=64, accumulator_address=65),
        alternating_memory_loop_bytecode_program(4, base_address=16),
        selector_checkpoint_bank_bytecode_program(4, base_address=32),
        indirect_counter_bank_program(8, counter_address=32, accumulator_address=33),
        subroutine_braid_program(4, base_address=80),
        stack_memory_braid_program(6, base_address=64),
        checkpoint_replay_long_program(6, base_address=96),
    ):
        result = verify_program(program)
        assert result.passed is True
        assert result.error_class is None


def test_verifier_rejects_invalid_programs() -> None:
    results = [verify_program(program) for program in verifier_negative_programs()]

    assert all(result.passed is False for result in results)
    assert {result.error_class for result in results} == {
        "branch_target",
        "call_target",
        "empty_return",
        "recursive_call",
        "type_mismatch",
        "unterminated_frame",
    }


def test_lowered_program_matches_reference_interpreter() -> None:
    program = loop_with_subroutine_update_program(6, counter_address=64, accumulator_address=65)
    bytecode_result = BytecodeInterpreter().run(program)
    lowered_result = TraceInterpreter().run(lower_program(program))

    assert bytecode_result.events == lowered_result.events
    assert bytecode_result.final_state == lowered_result.final_state


def test_harness_case_reports_exact_match_for_valid_program() -> None:
    case = BytecodeCase("smoke", "short_exact_trace", 32, arithmetic_smoke_program())
    row = run_harness_case(case)

    assert row.trace_match is True
    assert row.final_state_match is True
    assert row.failure_class is None


def test_harness_case_reports_exact_match_for_selector_checkpoint_bank() -> None:
    case = BytecodeCase(
        "loops",
        "medium_exact_trace",
        512,
        selector_checkpoint_bank_bytecode_program(6, base_address=32),
    )
    row = run_harness_case(case)

    assert row.trace_match is True
    assert row.final_state_match is True
    assert row.failure_class is None


def test_harness_case_reports_exact_match_for_subroutine_braid() -> None:
    case = BytecodeCase(
        "control_flow",
        "medium_exact_trace",
        256,
        subroutine_braid_program(6, base_address=80),
    )
    row = run_harness_case(case)

    assert row.trace_match is True
    assert row.final_state_match is True
    assert row.failure_class is None


def test_harness_case_reports_verify_error_for_invalid_program() -> None:
    invalid = verifier_negative_programs()[0]
    case = BytecodeCase("invalid", "short_exact_trace", 32, invalid)
    row = run_harness_case(case)

    assert row.failure_class == "verify_error"
    assert row.trace_match is False
