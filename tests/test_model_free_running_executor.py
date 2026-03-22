from __future__ import annotations

import pytest

from exec_trace import (
    TraceInterpreter,
    call_chain_program,
    countdown_program,
    dynamic_memory_program,
    equality_branch_program,
    latest_write_program,
    memory_accumulator_program,
)
from model import (
    FreeRunningTraceExecutor,
    build_countdown_stack_samples,
    compare_execution_to_reference,
    evaluate_free_running_programs,
    fit_scorer,
    run_free_running_exact,
    run_free_running_with_stack_scorer,
)


def test_free_running_exact_linear_matches_reference_programs() -> None:
    programs = (
        call_chain_program(),
        countdown_program(7),
        equality_branch_program(4, 4),
        equality_branch_program(4, 5),
        latest_write_program(),
        memory_accumulator_program(),
        dynamic_memory_program(),
    )
    interpreter = TraceInterpreter()

    for program in programs:
        execution = run_free_running_exact(program, decode_mode="linear")
        reference = interpreter.run(program)

        assert execution.events == reference.events
        assert execution.final_state == reference.final_state


def test_free_running_exact_accelerated_matches_reference_programs() -> None:
    programs = (
        call_chain_program(),
        countdown_program(12),
        equality_branch_program(2, 2),
        equality_branch_program(1, 3),
        latest_write_program(),
        memory_accumulator_program(),
        dynamic_memory_program(),
    )
    interpreter = TraceInterpreter()

    for program in programs:
        execution = run_free_running_exact(program, decode_mode="accelerated")
        reference = interpreter.run(program)

        assert execution.events == reference.events
        assert execution.final_state == reference.final_state


def test_free_running_partitioned_memory_matches_reference_programs() -> None:
    programs = (
        latest_write_program(),
        memory_accumulator_program(),
        dynamic_memory_program(),
    )
    interpreter = TraceInterpreter()
    executor = FreeRunningTraceExecutor(
        stack_strategy="accelerated",
        memory_strategy="partitioned_exact",
    )

    for program in programs:
        execution = executor.run(program)
        reference = interpreter.run(program)

        assert execution.events == reference.events
        assert execution.final_state == reference.final_state


def test_free_running_pointer_like_exact_matches_reference_programs() -> None:
    programs = (
        call_chain_program(),
        countdown_program(12),
        equality_branch_program(2, 2),
        latest_write_program(),
        memory_accumulator_program(),
        dynamic_memory_program(),
    )
    interpreter = TraceInterpreter()
    executor = FreeRunningTraceExecutor(
        stack_strategy="pointer_like_exact",
        memory_strategy="pointer_like_exact",
    )

    for program in programs:
        execution = executor.run(program)
        reference = interpreter.run(program)

        assert execution.events == reference.events
        assert execution.final_state == reference.final_state


def test_free_running_staged_exact_matches_reference_programs() -> None:
    programs = (
        call_chain_program(),
        countdown_program(12),
        equality_branch_program(1, 3),
        latest_write_program(),
        memory_accumulator_program(),
        dynamic_memory_program(),
    )
    interpreter = TraceInterpreter()
    executor = FreeRunningTraceExecutor(
        stack_strategy="staged_exact",
        memory_strategy="staged_exact",
    )

    for program in programs:
        execution = executor.run(program)
        reference = interpreter.run(program)

        assert execution.events == reference.events
        assert execution.final_state == reference.final_state


def test_free_running_rejects_partitioned_stack_strategy() -> None:
    with pytest.raises(ValueError, match="partitioned_exact"):
        FreeRunningTraceExecutor(
            stack_strategy="partitioned_exact",
            memory_strategy="accelerated",
        )


def test_compare_execution_to_reference_reports_exact_match() -> None:
    program = call_chain_program()
    execution = run_free_running_exact(program, decode_mode="accelerated")

    outcome = compare_execution_to_reference(program, execution)

    assert outcome.exact_trace_match is True
    assert outcome.exact_final_state_match is True
    assert outcome.first_mismatch_step is None


def test_free_running_exact_records_call_space_reads() -> None:
    execution = FreeRunningTraceExecutor(
        stack_strategy="pointer_like_exact",
        memory_strategy="pointer_like_exact",
    ).run(call_chain_program())

    call_reads = [observation for observation in execution.read_observations if observation.space == "call"]

    assert len(call_reads) == 2
    assert [observation.chosen_value for observation in call_reads] == [7, 3]


def test_free_running_evaluation_reports_long_countdown_bucket() -> None:
    programs = [countdown_program(start) for start in range(0, 21)]

    evaluation = evaluate_free_running_programs(
        programs,
        lambda program: run_free_running_exact(program, decode_mode="accelerated"),
    )

    assert evaluation.exact_trace_accuracy == 1.0
    assert evaluation.exact_final_state_accuracy == 1.0
    assert any(name == "steps>=49" for name, _ in evaluation.by_length_bucket)


def test_trainable_stack_executor_rolls_out_heldout_countdowns() -> None:
    fit = fit_scorer(build_countdown_stack_samples(range(0, 7)))
    programs = [countdown_program(start) for start in range(0, 21)]

    evaluation = evaluate_free_running_programs(
        programs,
        lambda program: run_free_running_with_stack_scorer(program, fit.scorer),
    )

    assert evaluation.exact_trace_accuracy == 1.0
    assert evaluation.exact_final_state_accuracy == 1.0


def test_trainable_stack_executor_transfers_to_branch_and_dynamic_memory() -> None:
    fit = fit_scorer(build_countdown_stack_samples(range(0, 7)))
    programs = [
        equality_branch_program(0, 0),
        equality_branch_program(0, 1),
        equality_branch_program(5, 5),
        dynamic_memory_program(),
    ]

    evaluation = evaluate_free_running_programs(
        programs,
        lambda program: run_free_running_with_stack_scorer(program, fit.scorer),
    )

    assert evaluation.exact_trace_accuracy == 1.0
    assert evaluation.exact_final_state_accuracy == 1.0
