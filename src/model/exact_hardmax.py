"""Exact hard-max causal decode helpers for latest-write state semantics."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal, Sequence

from exec_trace import TraceEvent
from exec_trace.dsl import Opcode
from geometry import HullKVCache, brute_force_hardmax_2d


@dataclass(frozen=True, slots=True)
class LatestWriteDecodeConfig:
    """Configuration for exact latest-write retrieval under bounded causal length."""

    max_steps: int
    addresses: tuple[int, ...]
    default_value: int = 0

    @property
    def epsilon(self) -> Fraction:
        # Keep the time bias strictly below the minimum one-step address mismatch gap.
        return Fraction(1, self.max_steps + 2)


@dataclass(frozen=True, slots=True)
class MemoryOperation:
    step: int
    kind: Literal["store", "load"]
    address: int
    value: int
    space: Literal["memory", "stack", "call"] = "memory"


@dataclass(frozen=True, slots=True)
class DecodeCandidateRow:
    row_index: int
    kind: Literal["default", "store"]
    address: int
    step: int
    value: int
    space: Literal["memory", "stack", "call"]
    label: str


@dataclass(frozen=True, slots=True)
class DecodeObservation:
    step: int
    address: int
    expected_value: int
    linear_value: int
    accelerated_value: int
    linear_maximizer_indices: tuple[int, ...]
    accelerated_maximizer_indices: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class DecodeRun:
    config: LatestWriteDecodeConfig
    operations: tuple[MemoryOperation, ...]
    candidate_rows: tuple[DecodeCandidateRow, ...]
    observations: tuple[DecodeObservation, ...]


def encode_latest_write_key(address: int, step: int, epsilon: Fraction) -> tuple[int, Fraction]:
    """Encode a write so exact address match wins, then newest step breaks ties."""

    return (address, Fraction(-(address**2)) + (epsilon * step))


def encode_latest_write_query(address: int) -> tuple[int, int]:
    return (2 * address, 1)


def extract_memory_operations(events: Sequence[TraceEvent]) -> tuple[MemoryOperation, ...]:
    operations: list[MemoryOperation] = []
    for event in events:
        if event.memory_write is not None:
            address, value = event.memory_write
            operations.append(
                MemoryOperation(step=event.step, kind="store", address=address, value=value, space="memory")
            )
        if event.memory_read_address is not None:
            if event.memory_read_value is None:
                raise ValueError(f"Read event at step {event.step} is missing a memory_read_value.")
            operations.append(
                MemoryOperation(
                    step=event.step,
                    kind="load",
                    address=event.memory_read_address,
                    value=event.memory_read_value,
                    space="memory",
                )
            )
    return tuple(operations)


def extract_stack_slot_operations(events: Sequence[TraceEvent]) -> tuple[MemoryOperation, ...]:
    operations: list[MemoryOperation] = []
    for event in events:
        pop_count = len(event.popped)
        read_base = event.stack_depth_before - pop_count
        for offset, value in enumerate(event.popped):
            operations.append(
                MemoryOperation(
                    step=event.step,
                    kind="load",
                    address=read_base + offset,
                    value=value,
                    space="stack",
                )
            )

        write_base = event.stack_depth_before - pop_count
        for offset, value in enumerate(event.pushed):
            operations.append(
                MemoryOperation(
                    step=event.step,
                    kind="store",
                    address=write_base + offset,
                    value=value,
                    space="stack",
                )
            )
    return tuple(operations)


def extract_call_frame_operations(events: Sequence[TraceEvent]) -> tuple[MemoryOperation, ...]:
    operations: list[MemoryOperation] = []
    call_depth = 0
    for event in events:
        if event.opcode == Opcode.CALL:
            operations.append(
                MemoryOperation(
                    step=event.step,
                    kind="store",
                    address=call_depth,
                    value=event.pc + 1,
                    space="call",
                )
            )
            call_depth += 1
        elif event.opcode == Opcode.RET:
            if call_depth <= 0:
                raise ValueError(f"RET event at step {event.step} has no pending call frame.")
            call_depth -= 1
            operations.append(
                MemoryOperation(
                    step=event.step,
                    kind="load",
                    address=call_depth,
                    value=event.next_pc,
                    space="call",
                )
            )
    return tuple(operations)


def infer_address_domain(operations: Sequence[MemoryOperation]) -> tuple[int, ...]:
    return tuple(sorted({operation.address for operation in operations}))


def run_latest_write_decode(
    operations: Sequence[MemoryOperation],
    config: LatestWriteDecodeConfig,
) -> DecodeRun:
    spaces = {operation.space for operation in operations}
    if len(spaces) > 1:
        raise ValueError("run_latest_write_decode currently expects operations from a single space.")

    linear_keys: list[tuple[int, Fraction]] = []
    linear_values: list[int] = []
    accelerated = HullKVCache()
    space = next(iter(spaces), "memory")
    candidate_rows: list[DecodeCandidateRow] = []

    def append_candidate_row(*, kind: Literal["default", "store"], address: int, step: int, value: int) -> None:
        row_index = len(candidate_rows)
        if kind == "default":
            label = f"default:{space}:a{address}"
        else:
            label = f"store:{space}:a{address}:s{step}:r{row_index}"
        candidate_rows.append(
            DecodeCandidateRow(
                row_index=row_index,
                kind=kind,
                address=address,
                step=step,
                value=value,
                space=space,
                label=label,
            )
        )

    seed_step = -1
    for address in config.addresses:
        key = encode_latest_write_key(address, seed_step, config.epsilon)
        linear_keys.append(key)
        linear_values.append(config.default_value)
        accelerated.insert(key, config.default_value)
        append_candidate_row(kind="default", address=address, step=seed_step, value=config.default_value)

    observations: list[DecodeObservation] = []
    for operation in operations:
        if operation.kind == "store":
            key = encode_latest_write_key(operation.address, operation.step, config.epsilon)
            linear_keys.append(key)
            linear_values.append(operation.value)
            accelerated.insert(key, operation.value)
            append_candidate_row(
                kind="store",
                address=operation.address,
                step=operation.step,
                value=operation.value,
            )
            continue

        query = encode_latest_write_query(operation.address)
        linear_result = brute_force_hardmax_2d(linear_keys, linear_values, query)
        accelerated_result = accelerated.query(query)
        linear_value = linear_result.value
        accelerated_value = accelerated_result.value
        if not isinstance(linear_value, int) or not isinstance(accelerated_value, int):
            raise TypeError("Latest-write decode expects scalar integer values.")

        observations.append(
            DecodeObservation(
                step=operation.step,
                address=operation.address,
                expected_value=operation.value,
                linear_value=linear_value,
                accelerated_value=accelerated_value,
                linear_maximizer_indices=linear_result.maximizer_indices,
                accelerated_maximizer_indices=accelerated_result.maximizer_indices,
            )
        )

    return DecodeRun(
        config=config,
        operations=tuple(operations),
        candidate_rows=tuple(candidate_rows),
        observations=tuple(observations),
    )


def config_for_operations(
    operations: Sequence[MemoryOperation],
    *,
    default_value: int = 0,
) -> LatestWriteDecodeConfig:
    if not operations:
        raise ValueError("At least one memory operation is required.")
    max_steps = max(operation.step for operation in operations)
    addresses = infer_address_domain(operations)
    return LatestWriteDecodeConfig(
        max_steps=max_steps,
        addresses=addresses,
        default_value=default_value,
    )


def run_latest_write_decode_for_events(
    events: Sequence[TraceEvent],
    *,
    default_value: int = 0,
) -> DecodeRun:
    operations = extract_memory_operations(events)
    config = config_for_operations(operations, default_value=default_value)
    return run_latest_write_decode(operations, config)


def run_latest_write_decode_for_stack_events(
    events: Sequence[TraceEvent],
    *,
    default_value: int = 0,
) -> DecodeRun:
    operations = extract_stack_slot_operations(events)
    config = config_for_operations(operations, default_value=default_value)
    return run_latest_write_decode(operations, config)


def run_latest_write_decode_for_call_events(
    events: Sequence[TraceEvent],
    *,
    default_value: int = 0,
) -> DecodeRun:
    operations = extract_call_frame_operations(events)
    config = config_for_operations(operations, default_value=default_value)
    return run_latest_write_decode(operations, config)
