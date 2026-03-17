"""Exact hard-max causal decode helpers for latest-write memory semantics."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal, Sequence

from exec_trace import TraceEvent
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


@dataclass(frozen=True, slots=True)
class DecodeObservation:
    step: int
    address: int
    expected_value: int
    linear_value: int
    accelerated_value: int


@dataclass(frozen=True, slots=True)
class DecodeRun:
    config: LatestWriteDecodeConfig
    operations: tuple[MemoryOperation, ...]
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
            operations.append(MemoryOperation(step=event.step, kind="store", address=address, value=value))
        if event.memory_read_address is not None:
            if event.memory_read_value is None:
                raise ValueError(f"Read event at step {event.step} is missing a memory_read_value.")
            operations.append(
                MemoryOperation(
                    step=event.step,
                    kind="load",
                    address=event.memory_read_address,
                    value=event.memory_read_value,
                )
            )
    return tuple(operations)


def infer_address_domain(operations: Sequence[MemoryOperation]) -> tuple[int, ...]:
    return tuple(sorted({operation.address for operation in operations}))


def run_latest_write_decode(
    operations: Sequence[MemoryOperation],
    config: LatestWriteDecodeConfig,
) -> DecodeRun:
    linear_keys: list[tuple[int, Fraction]] = []
    linear_values: list[int] = []
    accelerated = HullKVCache()

    seed_step = -1
    for address in config.addresses:
        key = encode_latest_write_key(address, seed_step, config.epsilon)
        linear_keys.append(key)
        linear_values.append(config.default_value)
        accelerated.insert(key, config.default_value)

    observations: list[DecodeObservation] = []
    for operation in operations:
        if operation.kind == "store":
            key = encode_latest_write_key(operation.address, operation.step, config.epsilon)
            linear_keys.append(key)
            linear_values.append(operation.value)
            accelerated.insert(key, operation.value)
            continue

        query = encode_latest_write_query(operation.address)
        linear_value = brute_force_hardmax_2d(linear_keys, linear_values, query).value
        accelerated_value = accelerated.query(query).value
        if not isinstance(linear_value, int) or not isinstance(accelerated_value, int):
            raise TypeError("Latest-write decode expects scalar integer values.")

        observations.append(
            DecodeObservation(
                step=operation.step,
                address=operation.address,
                expected_value=operation.value,
                linear_value=linear_value,
                accelerated_value=accelerated_value,
            )
        )

    return DecodeRun(
        config=config,
        operations=tuple(operations),
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
