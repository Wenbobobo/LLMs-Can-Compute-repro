"""Finite-precision stress tests for 2D latest-write addressing."""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass
from typing import Callable, Literal, Sequence

from model.exact_hardmax import MemoryOperation

PrecisionFormat = Literal["float64", "float32", "bfloat16", "float16"]
CheckKind = Literal["identity", "latest_write"]
CheckMode = Literal["exhaustive", "local"]
PrecisionScheme = Literal["single_head", "radix2", "block_recentered"]


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


@dataclass(frozen=True, slots=True)
class PrecisionSchemeFailure:
    scheme: PrecisionScheme
    kind: CheckKind
    query_address: int
    expected_address: int
    expected_step: int
    competing_address: int
    competing_step: int
    expected_scores: tuple[float, ...]
    competing_scores: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class PrecisionSchemeCheckResult:
    fmt: PrecisionFormat
    scheme: PrecisionScheme
    kind: CheckKind
    mode: CheckMode
    address_limit: int
    max_steps: int
    passed: bool
    first_failure: PrecisionSchemeFailure | None


@dataclass(frozen=True, slots=True)
class PrecisionSchemeSweepRow:
    address_limit: int
    passed: bool
    first_failure_query: int | None


@dataclass(frozen=True, slots=True)
class PrecisionSchemeConfig:
    scheme: PrecisionScheme
    base: int = 64


@dataclass(frozen=True, slots=True)
class PrecisionStressReport:
    fmt: PrecisionFormat
    scheme: PrecisionScheme
    kind: CheckKind
    mode: CheckMode
    rows: tuple[PrecisionSchemeSweepRow, ...]


@dataclass(frozen=True, slots=True)
class RealTracePrecisionFailure:
    space: str
    read_step: int
    query_address: int
    expected_address: int
    expected_step: int
    competing_address: int
    competing_step: int
    expected_scores: tuple[float, ...]
    competing_scores: tuple[float, ...]
    failure_type: Literal["wrong_address", "stale_read", "tie_collapse"]


@dataclass(frozen=True, slots=True)
class RealTracePrecisionResult:
    fmt: PrecisionFormat
    scheme: PrecisionScheme
    base: int
    space: str
    max_steps: int
    read_count: int
    write_count: int
    passed: bool
    first_failure: RealTracePrecisionFailure | None


class PrecisionStressRunner:
    """Run scheme-aware finite-precision sweeps with fixed configuration."""

    def __init__(
        self,
        *,
        fmt: PrecisionFormat,
        scheme: PrecisionScheme,
        base: int = 64,
    ) -> None:
        self.fmt = fmt
        self.scheme = scheme
        self.base = base

    def run(
        self,
        *,
        kind: CheckKind,
        address_limit: int,
        mode: CheckMode = "exhaustive",
        max_steps: int | None = None,
    ) -> PrecisionSchemeCheckResult:
        return check_precision_scheme_range(
            address_limit,
            fmt=self.fmt,
            kind=kind,
            mode=mode,
            scheme=self.scheme,
            base=self.base,
            max_steps=max_steps,
        )

    def sweep(
        self,
        ranges: Sequence[int],
        *,
        kind: CheckKind,
        mode: CheckMode,
        max_steps_fn: Callable[[int], int] | None = None,
    ) -> PrecisionStressReport:
        return PrecisionStressReport(
            fmt=self.fmt,
            scheme=self.scheme,
            kind=kind,
            mode=mode,
            rows=sweep_precision_scheme_ranges(
                ranges,
                fmt=self.fmt,
                kind=kind,
                mode=mode,
                scheme=self.scheme,
                base=self.base,
                max_steps_fn=max_steps_fn,
            ),
        )


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


def quantized_identity_score(
    query_address: int,
    candidate_address: int,
    *,
    fmt: PrecisionFormat,
) -> float:
    q0 = quantize(2.0 * query_address, fmt)
    q1 = quantize(1.0, fmt)
    k0 = quantize(float(candidate_address), fmt)
    k1 = quantize(float(-(candidate_address**2)), fmt)
    return quantized_add(quantized_mul(q0, k0, fmt), quantized_mul(q1, k1, fmt), fmt)


def quantized_scheme_score(
    query_address: int,
    candidate_address: int,
    candidate_step: int,
    *,
    max_steps: int,
    fmt: PrecisionFormat,
    scheme: PrecisionScheme,
    base: int = 64,
) -> tuple[float, ...]:
    if scheme == "single_head":
        return (
            quantized_latest_write_score(
                query_address,
                candidate_address,
                candidate_step,
                max_steps=max_steps,
                fmt=fmt,
            ),
        )

    if base <= 1:
        raise ValueError("base must be greater than 1 for decomposed precision schemes.")

    query_high, query_low = divmod(query_address, base)
    candidate_high, candidate_low = divmod(candidate_address, base)
    coarse = quantized_identity_score(query_high, candidate_high, fmt=fmt)

    if scheme == "radix2":
        fine_query = query_low
        fine_candidate = candidate_low
    elif scheme == "block_recentered":
        center = query_high * base
        fine_query = query_address - center
        fine_candidate = candidate_address - center
    else:
        raise ValueError(f"Unsupported precision scheme: {scheme}")

    fine = quantized_latest_write_score(
        fine_query,
        fine_candidate,
        candidate_step,
        max_steps=max_steps,
        fmt=fmt,
    )
    return (coarse, fine)


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


def check_precision_scheme_range(
    address_limit: int,
    *,
    fmt: PrecisionFormat,
    kind: CheckKind,
    mode: CheckMode = "exhaustive",
    scheme: PrecisionScheme = "single_head",
    base: int = 64,
    max_steps: int | None = None,
) -> PrecisionSchemeCheckResult:
    if address_limit <= 0:
        raise ValueError("address_limit must be positive.")
    max_steps = max_steps or max(32, address_limit)

    for query_address in range(address_limit):
        failure = _check_single_query_for_scheme(
            query_address,
            address_limit=address_limit,
            fmt=fmt,
            kind=kind,
            mode=mode,
            max_steps=max_steps,
            scheme=scheme,
            base=base,
        )
        if failure is not None:
            return PrecisionSchemeCheckResult(
                fmt=fmt,
                scheme=scheme,
                kind=kind,
                mode=mode,
                address_limit=address_limit,
                max_steps=max_steps,
                passed=False,
                first_failure=failure,
            )

    return PrecisionSchemeCheckResult(
        fmt=fmt,
        scheme=scheme,
        kind=kind,
        mode=mode,
        address_limit=address_limit,
        max_steps=max_steps,
        passed=True,
        first_failure=None,
    )


def sweep_precision_scheme_ranges(
    ranges: Sequence[int],
    *,
    fmt: PrecisionFormat,
    kind: CheckKind,
    mode: CheckMode,
    scheme: PrecisionScheme,
    base: int = 64,
    max_steps_fn: Callable[[int], int] | None = None,
) -> tuple[PrecisionSchemeSweepRow, ...]:
    rows: list[PrecisionSchemeSweepRow] = []
    for address_limit in ranges:
        result = check_precision_scheme_range(
            address_limit,
            fmt=fmt,
            kind=kind,
            mode=mode,
            scheme=scheme,
            base=base,
            max_steps=(max_steps_fn(address_limit) if max_steps_fn is not None else None),
        )
        rows.append(
            PrecisionSchemeSweepRow(
                address_limit=address_limit,
                passed=result.passed,
                first_failure_query=None if result.first_failure is None else result.first_failure.query_address,
            )
        )
    return tuple(rows)


def check_real_trace_precision(
    operations: Sequence[MemoryOperation],
    *,
    fmt: PrecisionFormat,
    scheme: PrecisionScheme = "single_head",
    base: int = 64,
    default_value: int = 0,
) -> RealTracePrecisionResult:
    if not operations:
        raise ValueError("At least one operation is required for real-trace precision checks.")

    spaces = {operation.space for operation in operations}
    if len(spaces) != 1:
        raise ValueError("Real-trace precision checks expect operations from a single logical space.")

    space = next(iter(spaces))
    max_steps = max(operation.step for operation in operations)
    prior_writes: list[MemoryOperation] = []
    read_count = 0

    for operation in operations:
        if operation.kind == "store":
            prior_writes.append(operation)
            continue

        read_count += 1
        expected = _expected_real_trace_candidate(
            operation.address,
            prior_writes,
            space=space,
            default_value=default_value,
        )
        expected_scores = quantized_scheme_score(
            operation.address,
            expected.address,
            expected.step,
            max_steps=max_steps,
            fmt=fmt,
            scheme=scheme,
            base=base,
        )

        candidates = list(prior_writes)
        if expected.step == -1:
            candidates.append(expected)

        for candidate in candidates:
            if candidate.address == expected.address and candidate.step == expected.step:
                continue
            competing_scores = quantized_scheme_score(
                operation.address,
                candidate.address,
                candidate.step,
                max_steps=max_steps,
                fmt=fmt,
                scheme=scheme,
                base=base,
            )
            if competing_scores >= expected_scores:
                return RealTracePrecisionResult(
                    fmt=fmt,
                    scheme=scheme,
                    base=base,
                    space=space,
                    max_steps=max_steps,
                    read_count=read_count,
                    write_count=len(prior_writes),
                    passed=False,
                    first_failure=RealTracePrecisionFailure(
                        space=space,
                        read_step=operation.step,
                        query_address=operation.address,
                        expected_address=expected.address,
                        expected_step=expected.step,
                        competing_address=candidate.address,
                        competing_step=candidate.step,
                        expected_scores=expected_scores,
                        competing_scores=competing_scores,
                        failure_type=_classify_real_trace_failure(expected, candidate, expected_scores, competing_scores),
                    ),
                )

    return RealTracePrecisionResult(
        fmt=fmt,
        scheme=scheme,
        base=base,
        space=space,
        max_steps=max_steps,
        read_count=read_count,
        write_count=sum(1 for operation in operations if operation.kind == "store"),
        passed=True,
        first_failure=None,
    )


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


def _check_single_query_for_scheme(
    query_address: int,
    *,
    address_limit: int,
    fmt: PrecisionFormat,
    kind: CheckKind,
    mode: CheckMode,
    max_steps: int,
    scheme: PrecisionScheme,
    base: int,
) -> PrecisionSchemeFailure | None:
    expected_step = 1 if kind == "latest_write" else 0
    expected_scores = quantized_scheme_score(
        query_address,
        query_address,
        expected_step,
        max_steps=max_steps,
        fmt=fmt,
        scheme=scheme,
        base=base,
    )

    for candidate_address, candidate_step in _candidate_iter(
        query_address=query_address,
        address_limit=address_limit,
        kind=kind,
        mode=mode,
    ):
        if candidate_address == query_address and candidate_step == expected_step:
            continue
        competing_scores = quantized_scheme_score(
            query_address,
            candidate_address,
            candidate_step,
            max_steps=max_steps,
            fmt=fmt,
            scheme=scheme,
            base=base,
        )
        if competing_scores >= expected_scores:
            return PrecisionSchemeFailure(
                scheme=scheme,
                kind=kind,
                query_address=query_address,
                expected_address=query_address,
                expected_step=expected_step,
                competing_address=candidate_address,
                competing_step=candidate_step,
                expected_scores=expected_scores,
                competing_scores=competing_scores,
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


def _expected_real_trace_candidate(
    query_address: int,
    prior_writes: Sequence[MemoryOperation],
    *,
    space: str,
    default_value: int,
) -> MemoryOperation:
    for candidate in reversed(prior_writes):
        if candidate.address == query_address:
            return candidate
    return MemoryOperation(
        step=-1,
        kind="store",
        address=query_address,
        value=default_value,
        space=space,
    )


def _classify_real_trace_failure(
    expected: MemoryOperation,
    competing: MemoryOperation,
    expected_scores: tuple[float, ...],
    competing_scores: tuple[float, ...],
) -> Literal["wrong_address", "stale_read", "tie_collapse"]:
    if competing_scores == expected_scores:
        return "tie_collapse"
    if expected.address != competing.address:
        return "wrong_address"
    return "stale_read"
