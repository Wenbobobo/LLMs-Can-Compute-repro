"""Finite-precision stress tests for 2D latest-write addressing."""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass
from typing import Callable, Literal, Sequence

PrecisionFormat = Literal["float64", "float32", "bfloat16", "float16"]
CheckKind = Literal["identity", "latest_write"]
CheckMode = Literal["exhaustive", "local"]


def _quantize_float64(value: float) -> float:
    return float(value)


def _quantize_float32(value: float) -> float:
    return struct.unpack(">f", struct.pack(">f", float(value)))[0]


def _quantize_float16(value: float) -> float:
    try:
        return struct.unpack(">e", struct.pack(">e", float(value)))[0]
    except OverflowError:
        return math.copysign(math.inf, value)


def _quantize_bfloat16(value: float) -> float:
    packed = struct.unpack(">I", struct.pack(">f", float(value)))[0]
    rounding_bias = 0x7FFF + ((packed >> 16) & 1)
    rounded = packed + rounding_bias
    truncated = rounded & 0xFFFF0000
    return struct.unpack(">f", struct.pack(">I", truncated))[0]


QUANTIZERS: dict[PrecisionFormat, Callable[[float], float]] = {
    "float64": _quantize_float64,
    "float32": _quantize_float32,
    "bfloat16": _quantize_bfloat16,
    "float16": _quantize_float16,
}


@dataclass(frozen=True, slots=True)
class PrecisionFailure:
    kind: CheckKind
    query_address: int
    expected_address: int
    expected_step: int
    competing_address: int
    competing_step: int
    expected_score: float
    competing_score: float


@dataclass(frozen=True, slots=True)
class PrecisionCheckResult:
    fmt: PrecisionFormat
    kind: CheckKind
    mode: CheckMode
    address_limit: int
    max_steps: int
    passed: bool
    first_failure: PrecisionFailure | None


@dataclass(frozen=True, slots=True)
class RangeSweepRow:
    address_limit: int
    passed: bool
    first_failure_query: int | None


def quantize(value: float, fmt: PrecisionFormat) -> float:
    return QUANTIZERS[fmt](value)


def quantized_add(left: float, right: float, fmt: PrecisionFormat) -> float:
    return quantize(quantize(left, fmt) + quantize(right, fmt), fmt)


def quantized_mul(left: float, right: float, fmt: PrecisionFormat) -> float:
    return quantize(quantize(left, fmt) * quantize(right, fmt), fmt)


def quantized_latest_write_score(
    query_address: int,
    candidate_address: int,
    candidate_step: int,
    *,
    max_steps: int,
    fmt: PrecisionFormat,
) -> float:
    epsilon = quantize(1.0 / (max_steps + 2), fmt)
    q0 = quantize(2.0 * query_address, fmt)
    q1 = quantize(1.0, fmt)
    k0 = quantize(float(candidate_address), fmt)
    base = quantize(float(-(candidate_address**2)), fmt)
    time_term = quantized_mul(epsilon, float(candidate_step), fmt)
    k1 = quantized_add(base, time_term, fmt)
    return quantized_add(quantized_mul(q0, k0, fmt), quantized_mul(q1, k1, fmt), fmt)


def check_precision_range(
    address_limit: int,
    *,
    fmt: PrecisionFormat,
    kind: CheckKind,
    mode: CheckMode = "exhaustive",
    max_steps: int | None = None,
) -> PrecisionCheckResult:
    if address_limit <= 0:
        raise ValueError("address_limit must be positive.")
    max_steps = max_steps or max(32, address_limit)

    for query_address in range(address_limit):
        failure = _check_single_query(
            query_address,
            address_limit=address_limit,
            fmt=fmt,
            kind=kind,
            mode=mode,
            max_steps=max_steps,
        )
        if failure is not None:
            return PrecisionCheckResult(
                fmt=fmt,
                kind=kind,
                mode=mode,
                address_limit=address_limit,
                max_steps=max_steps,
                passed=False,
                first_failure=failure,
            )

    return PrecisionCheckResult(
        fmt=fmt,
        kind=kind,
        mode=mode,
        address_limit=address_limit,
        max_steps=max_steps,
        passed=True,
        first_failure=None,
    )


def sweep_precision_ranges(
    ranges: Sequence[int],
    *,
    fmt: PrecisionFormat,
    kind: CheckKind,
    mode: CheckMode,
    max_steps_fn: Callable[[int], int] | None = None,
) -> tuple[RangeSweepRow, ...]:
    rows: list[RangeSweepRow] = []
    for address_limit in ranges:
        result = check_precision_range(
            address_limit,
            fmt=fmt,
            kind=kind,
            mode=mode,
            max_steps=(max_steps_fn(address_limit) if max_steps_fn is not None else None),
        )
        rows.append(
            RangeSweepRow(
                address_limit=address_limit,
                passed=result.passed,
                first_failure_query=None if result.first_failure is None else result.first_failure.query_address,
            )
        )
    return tuple(rows)


def _check_single_query(
    query_address: int,
    *,
    address_limit: int,
    fmt: PrecisionFormat,
    kind: CheckKind,
    mode: CheckMode,
    max_steps: int,
) -> PrecisionFailure | None:
    expected_step = 1 if kind == "latest_write" else 0
    expected_score = quantized_latest_write_score(
        query_address,
        query_address,
        expected_step,
        max_steps=max_steps,
        fmt=fmt,
    )

    for candidate_address, candidate_step in _candidate_iter(
        query_address=query_address,
        address_limit=address_limit,
        kind=kind,
        mode=mode,
    ):
        if candidate_address == query_address and candidate_step == expected_step:
            continue
        competing_score = quantized_latest_write_score(
            query_address,
            candidate_address,
            candidate_step,
            max_steps=max_steps,
            fmt=fmt,
        )
        if competing_score >= expected_score:
            return PrecisionFailure(
                kind=kind,
                query_address=query_address,
                expected_address=query_address,
                expected_step=expected_step,
                competing_address=candidate_address,
                competing_step=candidate_step,
                expected_score=expected_score,
                competing_score=competing_score,
            )
    return None


def _candidate_iter(
    *,
    query_address: int,
    address_limit: int,
    kind: CheckKind,
    mode: CheckMode,
) -> tuple[tuple[int, int], ...]:
    if mode == "exhaustive":
        candidates = [(address, 0) for address in range(address_limit)]
        if kind == "latest_write":
            candidates.extend((address, 1) for address in range(address_limit))
        return tuple(candidates)

    local_candidates = []
    if kind == "latest_write":
        local_candidates.append((query_address, 0))
    if query_address > 0:
        local_candidates.append((query_address - 1, 1 if kind == "latest_write" else 0))
    if query_address + 1 < address_limit:
        local_candidates.append((query_address + 1, 1 if kind == "latest_write" else 0))
    return tuple(local_candidates)
