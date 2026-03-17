"""Replay engine for append-only execution traces."""

from __future__ import annotations

from .dsl import ExecutionState, Program, TraceEvent


class ReplayMismatch(RuntimeError):
    """Raised when a trace event does not match replayed semantics."""


def replay_trace(program: Program, events: tuple[TraceEvent, ...]) -> ExecutionState:
    stack: list[int] = []
    pc = 0
    halted = False

    for expected_step, event in enumerate(events):
        if halted:
            raise ReplayMismatch("Trace contains events after halt.")
        if event.step != expected_step:
            raise ReplayMismatch(f"Unexpected step number: {event.step} != {expected_step}")
        if event.pc != pc:
            raise ReplayMismatch(f"Unexpected PC: {event.pc} != {pc}")
        if not (0 <= pc < len(program)):
            raise ReplayMismatch(f"PC out of range during replay: {pc}")

        instruction = program.instructions[pc]
        if event.opcode != instruction.opcode or event.arg != instruction.arg:
            raise ReplayMismatch(
                f"Instruction mismatch at pc={pc}: {event.opcode}/{event.arg} != "
                f"{instruction.opcode}/{instruction.arg}"
            )

        if len(stack) != event.stack_depth_before:
            raise ReplayMismatch(
                f"Stack depth mismatch before event at step {event.step}: "
                f"{len(stack)} != {event.stack_depth_before}"
            )

        if event.popped:
            actual = tuple(stack[-len(event.popped) :])
            if actual != event.popped:
                raise ReplayMismatch(f"Popped values mismatch at step {event.step}: {actual} != {event.popped}")
            del stack[-len(event.popped) :]

        stack.extend(event.pushed)

        if len(stack) != event.stack_depth_after:
            raise ReplayMismatch(
                f"Stack depth mismatch after event at step {event.step}: "
                f"{len(stack)} != {event.stack_depth_after}"
            )

        pc = event.next_pc
        halted = event.halted

    return ExecutionState(pc=pc, stack=tuple(stack), halted=halted, steps=len(events))
