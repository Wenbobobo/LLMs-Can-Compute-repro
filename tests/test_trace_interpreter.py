from __future__ import annotations

import pytest

from exec_trace import (
    Instruction,
    Opcode,
    Program,
    TraceInterpreter,
    alternating_memory_loop_program,
    countdown_program,
    dynamic_memory_program,
    equality_branch_program,
    flagged_indirect_accumulator_program,
    hotspot_memory_rewrite_program,
    latest_memory_value,
    latest_write_program,
    loop_indirect_memory_program,
    memory_accumulator_program,
    replay_trace,
    reconstruct_memory,
    selector_checkpoint_bank_program,
    stack_fanout_sum_program,
    stack_memory_ping_pong_program,
)
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
    assert replayed.memory == ()


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


def test_memory_latest_write_and_replay_match() -> None:
    interpreter = TraceInterpreter()
    program = latest_write_program()

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (9,)
    assert replayed.memory == ((0, 9),)
    assert latest_memory_value(result.events, 0) == 9
    assert reconstruct_memory(result.events) == ((0, 9),)


def test_memory_accumulator_program() -> None:
    interpreter = TraceInterpreter()
    program = memory_accumulator_program()

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (12,)
    assert replayed.memory == ((0, 7), (1, 5), (2, 12))
    load_events = [event for event in result.events if event.memory_read_address is not None]
    assert [event.memory_read_value for event in load_events] == [7, 5, 12]


def test_dynamic_memory_program() -> None:
    interpreter = TraceInterpreter()
    program = dynamic_memory_program()

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (22,)
    assert replayed.memory == ((2, 11),)
    load_events = [event for event in result.events if event.memory_read_address is not None]
    assert [event.memory_read_address for event in load_events] == [2, 2]
    assert [event.memory_read_value for event in load_events] == [11, 11]


def test_loop_indirect_memory_program() -> None:
    interpreter = TraceInterpreter()
    program = loop_indirect_memory_program(4)

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (10,)
    assert reconstruct_memory(result.events) == ((4, 0), (5, 10))


def test_stack_memory_ping_pong_program() -> None:
    interpreter = TraceInterpreter()
    program = stack_memory_ping_pong_program()

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (13, 28)
    assert reconstruct_memory(result.events) == ((0, 14), (1, 9), (2, 13))


def test_alternating_memory_loop_program() -> None:
    interpreter = TraceInterpreter()
    program = alternating_memory_loop_program(4)

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (10,)
    assert reconstruct_memory(result.events) == ((0, 0), (1, 0), (2, 6), (3, 4))


def test_flagged_indirect_accumulator_program() -> None:
    interpreter = TraceInterpreter()
    program = flagged_indirect_accumulator_program(4, base_address=32)

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (10,)
    assert reconstruct_memory(result.events) == (
        (32, 0),
        (33, 0),
        (34, 36),
        (35, 37),
        (36, 6),
        (37, 4),
    )


def test_selector_checkpoint_bank_program() -> None:
    interpreter = TraceInterpreter()
    program = selector_checkpoint_bank_program(4, base_address=40)

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (10,)
    assert reconstruct_memory(result.events) == (
        (40, 0),
        (41, 1),
        (42, 46),
        (43, 46),
        (44, 47),
        (45, 48),
        (46, 5),
        (47, 3),
        (48, 2),
    )


def test_hotspot_memory_rewrite_program() -> None:
    interpreter = TraceInterpreter()
    program = hotspot_memory_rewrite_program(4, base_address=24)

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (19,)
    assert reconstruct_memory(result.events) == ((24, 0), (25, 1), (26, 8), (27, 5), (28, 6))


def test_stack_fanout_sum_program() -> None:
    interpreter = TraceInterpreter()
    program = stack_fanout_sum_program(5, base_value=2)

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (10,)
    assert result.final_state.steps == 10


def test_call_ret_program_replay_matches_interpreter() -> None:
    interpreter = TraceInterpreter()
    program = Program(
        instructions=(
            Instruction(Opcode.PUSH_CONST, 1),
            Instruction(Opcode.PUSH_CONST, 2),
            Instruction(Opcode.CALL, 4),
            Instruction(Opcode.HALT),
            Instruction(Opcode.ADD),
            Instruction(Opcode.PUSH_CONST, 3),
            Instruction(Opcode.CALL, 8),
            Instruction(Opcode.RET),
            Instruction(Opcode.ADD),
            Instruction(Opcode.RET),
        ),
        name="trace_call_chain_smoke",
    )

    result = interpreter.run(program)
    replayed = replay_trace(program, result.events)

    assert replayed == result.final_state
    assert replayed.stack == (6,)
    assert replayed.call_stack == ()


def test_ret_without_pending_frame_raises() -> None:
    interpreter = TraceInterpreter()
    program = Program(
        instructions=(
            Instruction(Opcode.RET),
            Instruction(Opcode.HALT),
        ),
        name="trace_invalid_empty_return",
    )

    with pytest.raises(RuntimeError, match="pending return address"):
        interpreter.run(program)


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
        memory_read_address=original.memory_read_address,
        memory_read_value=original.memory_read_value,
        memory_write=original.memory_write,
        next_pc=original.next_pc,
        stack_depth_before=original.stack_depth_before,
        stack_depth_after=original.stack_depth_after,
        halted=original.halted,
    )

    with pytest.raises(ReplayMismatch):
        replay_trace(program, tuple(tampered))


def test_replay_detects_tampered_memory_read() -> None:
    interpreter = TraceInterpreter()
    program = latest_write_program()
    result = interpreter.run(program)

    tampered = list(result.events)
    load_event = tampered[4]
    tampered[4] = TraceEvent(
        step=load_event.step,
        pc=load_event.pc,
        opcode=load_event.opcode,
        arg=load_event.arg,
        popped=load_event.popped,
        pushed=load_event.pushed,
        branch_taken=load_event.branch_taken,
        memory_read_address=load_event.memory_read_address,
        memory_read_value=123,
        memory_write=load_event.memory_write,
        next_pc=load_event.next_pc,
        stack_depth_before=load_event.stack_depth_before,
        stack_depth_after=load_event.stack_depth_after,
        halted=load_event.halted,
    )

    with pytest.raises(ReplayMismatch):
        replay_trace(program, tuple(tampered))
