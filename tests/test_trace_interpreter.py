from __future__ import annotations

import pytest

from exec_trace import TraceInterpreter, countdown_program, equality_branch_program, replay_trace
from exec_trace.dsl import TraceEvent
from exec_trace.replay import ReplayMismatch


def test_countdown_replay_matches_interpreter() -> None:
    interpreter = TraceInterpreter()
    program = countdown_program(4)

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.halted is True
    assert replayed.stack == (0,)


def test_branch_program_true_and_false_paths() -> None:
    interpreter = TraceInterpreter()

    true_program = equality_branch_program(7, 7)
    false_program = equality_branch_program(7, 9)

    true_result = interpreter.run(true_program)
    false_result = interpreter.run(false_program)

    assert true_result.final_state.stack == (1,)
    assert false_result.final_state.stack == (0,)


def test_trace_emission_is_deterministic() -> None:
    interpreter = TraceInterpreter()
    program = countdown_program(3)

    first = interpreter.run(program)
    second = interpreter.run(program)

    assert first.events == second.events
    assert first.final_state == second.final_state


def test_replay_detects_tampering() -> None:
    interpreter = TraceInterpreter()
    program = countdown_program(2)
    result = interpreter.run(program)

    tampered = list(result.events)
    original = tampered[1]
    tampered[1] = TraceEvent(
        step=original.step,
        pc=original.pc,
        opcode=original.opcode,
        arg=original.arg,
        popped=original.popped,
        pushed=(),
        branch_taken=original.branch_taken,
        next_pc=original.next_pc,
        stack_depth_before=original.stack_depth_before,
        stack_depth_after=original.stack_depth_after,
        halted=original.halted,
    )

    with pytest.raises(ReplayMismatch):
        replay_trace(program, tuple(tampered))
