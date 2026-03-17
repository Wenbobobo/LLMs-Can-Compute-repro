"""Replay engine for append-only execution traces."""

from __future__ import annotations

from .dsl import ExecutionState, Program, TraceEvent
from .memory import latest_memory_value, reconstruct_memory


class ReplayMismatch(RuntimeError):
    """Raised when a trace event does not match replayed semantics."""


def replay_trace(program: Program, events: tuple[TraceEvent, ...]) -> ExecutionState:
    stack: list[int] = []
    pc = 0
    halted = False
    reconstructed_events: list[TraceEvent] = []

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

        if event.memory_read_address is not None:
            expected_value = latest_memory_value(tuple(reconstructed_events), event.memory_read_address)
            if event.memory_read_value != expected_value:
                raise ReplayMismatch(
                    f"Memory read mismatch at step {event.step}: "
                    f"{event.memory_read_value} != {expected_value}"
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
        reconstructed_events.append(event)

    return ExecutionState(
        pc=pc,
        stack=tuple(stack),
        memory=reconstruct_memory(tuple(reconstructed_events)),
        halted=halted,
        steps=len(events),
    )
