"""Helpers for latest-write reconstruction over append-only trace events."""

from __future__ import annotations

from .dsl import TraceEvent


def latest_memory_value(
    events: tuple[TraceEvent, ...],
    address: int,
    *,
    upto_step: int | None = None,
    default: int = 0,
) -> int:
    """Return the latest visible value for an address under last-write-wins semantics."""

    for event in reversed(events):
        if upto_step is not None and event.step > upto_step:
            continue
        if event.memory_write is None:
            continue
        write_address, write_value = event.memory_write
        if write_address == address:
            return write_value
    return default


def reconstruct_memory(events: tuple[TraceEvent, ...]) -> tuple[tuple[int, int], ...]:
    """Reconstruct final memory solely from append-only trace events."""

    memory: dict[int, int] = {}
    for event in events:
        if event.memory_write is None:
            continue
        address, value = event.memory_write
        memory[address] = value
    return tuple(sorted(memory.items()))
