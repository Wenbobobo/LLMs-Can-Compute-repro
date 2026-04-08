"""Correctness-first accelerated cache for exact 2D hard-max retrieval.

The current insertion path is rebuild-based and intentionally prioritizes exact
semantics over optimal update asymptotics. Query-time retrieval uses a dual
upper-envelope representation for log-time candidate lookup, with an exact
full-scan fallback on breakpoint tie cases.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from .hardmax import (
    HardmaxResult,
    NumberLike,
    ValueLike,
    _coerce_key,
    _coerce_value,
    _normalize_number,
    _restore_value,
)


@dataclass(frozen=True, slots=True)
class _PointAggregate:
    key: tuple[Fraction, Fraction]
    value_sum: tuple[Fraction, ...]
    count: int
    entry_indices: tuple[int, ...]

    @property
    def average_value(self) -> tuple[Fraction, ...]:
        divisor = Fraction(self.count)
        return tuple(coord / divisor for coord in self.value_sum)


@dataclass(frozen=True, slots=True)
class _EnvelopeLine:
    slope: Fraction
    intercept: Fraction
    point_index: int


@dataclass(frozen=True, slots=True)
class _Envelope:
    lines: tuple[_EnvelopeLine, ...]
    breakpoints: tuple[Fraction, ...]

    def point_index_for_slope(self, slope: Fraction) -> int:
        index = bisect_right(self.breakpoints, slope)
        return self.lines[index].point_index

    def is_breakpoint(self, slope: Fraction) -> bool:
        index = bisect_left(self.breakpoints, slope)
        return index < len(self.breakpoints) and self.breakpoints[index] == slope


def _add_vectors(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def _intersection_x(left: _EnvelopeLine, right: _EnvelopeLine) -> Fraction:
    return Fraction(left.intercept - right.intercept, right.slope - left.slope)


def _build_upper_envelope(points: Sequence[_PointAggregate], negate: bool = False) -> _Envelope:
    sign = Fraction(-1 if negate else 1)
    best_by_slope: dict[Fraction, _EnvelopeLine] = {}

    for point_index, point in enumerate(points):
        x_coord, y_coord = point.key
        candidate = _EnvelopeLine(
            slope=sign * x_coord,
            intercept=sign * y_coord,
            point_index=point_index,
        )
        existing = best_by_slope.get(candidate.slope)
        if existing is None or candidate.intercept > existing.intercept:
            best_by_slope[candidate.slope] = candidate

    ordered = sorted(best_by_slope.values(), key=lambda line: (line.slope, line.intercept))
    if not ordered:
        return _Envelope(lines=(), breakpoints=())

    hull: list[_EnvelopeLine] = []
    starts: list[Fraction | None] = []
    for candidate in ordered:
        start: Fraction | None = None
        while hull:
            intersection = _intersection_x(hull[-1], candidate)
            previous_start = starts[-1]
            if previous_start is not None and intersection <= previous_start:
                hull.pop()
                starts.pop()
                continue
            start = intersection
            break

        if not hull:
            start = None

        hull.append(candidate)
        starts.append(start)

    breakpoints = tuple(start for start in starts[1:] if start is not None)
    return _Envelope(lines=tuple(hull), breakpoints=breakpoints)


class HullKVCache:
    """Insert-only exact cache for 2D hard-max retrieval.

    Query time uses log-time candidate lookup against a rebuild-based envelope.
    Exact tie cases fall back to a full scan over aggregated points.
    """

    def __init__(self) -> None:
        self._entries: list[tuple[tuple[Fraction, Fraction], tuple[Fraction, ...]]] = []
        self._scalar_mode: bool | None = None
        self._value_width: int | None = None
        self._dirty = False

        self._points: tuple[_PointAggregate, ...] = ()
        self._upper_envelope = _Envelope((), ())
        self._negated_upper_envelope = _Envelope((), ())
        self._total_value_sum: tuple[Fraction, ...] = ()
        self._total_count = 0

    def __len__(self) -> int:
        return len(self._entries)

    def insert(self, key: Sequence[NumberLike], value: ValueLike) -> None:
        coerced_key = _coerce_key(key)
        coerced_value, is_scalar = _coerce_value(value)

        if self._scalar_mode is None:
            self._scalar_mode = is_scalar
            self._value_width = len(coerced_value)
        else:
            if self._scalar_mode != is_scalar:
                raise ValueError("Do not mix scalar and vector values in one cache.")
            if self._value_width != len(coerced_value):
                raise ValueError("All cached values must have the same dimensionality.")

        self._entries.append((coerced_key, coerced_value))
        self._dirty = True

    def extend(
        self,
        keys: Sequence[Sequence[NumberLike]],
        values: Sequence[ValueLike],
    ) -> None:
        if len(keys) != len(values):
            raise ValueError("keys and values must have the same length.")
        for key, value in zip(keys, values, strict=True):
            self.insert(key, value)

    def query(self, query: Sequence[NumberLike]) -> HardmaxResult:
        if not self._entries:
            raise ValueError("Cannot query an empty cache.")

        self._rebuild_if_needed()
        assert self._scalar_mode is not None

        qx, qy = _coerce_key(query)
        query_key = (qx, qy)

        if qx == 0 and qy == 0:
            divisor = Fraction(self._total_count)
            averaged = tuple(coord / divisor for coord in self._total_value_sum)
            all_indices = tuple(index for point in self._points for index in point.entry_indices)
            return HardmaxResult(
                score=0,
                value=_restore_value(averaged, self._scalar_mode),
                maximizer_indices=all_indices,
            )

        if qy == 0:
            return self._scan_maximizers(query_key)

        slope = qx / qy
        envelope = self._upper_envelope if qy > 0 else self._negated_upper_envelope
        point_index = envelope.point_index_for_slope(slope)
        point = self._points[point_index]
        kx, ky = point.key
        score = (kx * qx) + (ky * qy)

        if envelope.is_breakpoint(slope):
            return self._scan_maximizers(query_key, target_score=score)

        return HardmaxResult(
            score=_normalize_number(score),
            value=_restore_value(point.average_value, self._scalar_mode),
            maximizer_indices=point.entry_indices,
        )

    def _rebuild_if_needed(self) -> None:
        if not self._dirty:
            return

        aggregates: dict[tuple[Fraction, Fraction], dict[str, object]] = {}
        total_value_sum = [Fraction(0) for _ in range(self._value_width or 0)]

        for index, (key, value) in enumerate(self._entries):
            bucket = aggregates.setdefault(
                key,
                {"value_sum": [Fraction(0) for _ in value], "count": 0, "entry_indices": []},
            )
            for coord_index, coord in enumerate(value):
                bucket["value_sum"][coord_index] += coord
                total_value_sum[coord_index] += coord
            bucket["count"] += 1
            bucket["entry_indices"].append(index)

        points: list[_PointAggregate] = []
        for key in sorted(aggregates):
            bucket = aggregates[key]
            points.append(
                _PointAggregate(
                    key=key,
                    value_sum=tuple(bucket["value_sum"]),
                    count=int(bucket["count"]),
                    entry_indices=tuple(bucket["entry_indices"]),
                )
            )

        self._points = tuple(points)
        self._upper_envelope = _build_upper_envelope(self._points, negate=False)
        self._negated_upper_envelope = _build_upper_envelope(self._points, negate=True)
        self._total_value_sum = tuple(total_value_sum)
        self._total_count = len(self._entries)
        self._dirty = False

    def _scan_maximizers(
        self,
        query: tuple[Fraction, Fraction],
        target_score: Fraction | None = None,
    ) -> HardmaxResult:
        assert self._scalar_mode is not None

        best_score = target_score
        maximizers: list[_PointAggregate] = []

        qx, qy = query
        for point in self._points:
            kx, ky = point.key
            score = (kx * qx) + (ky * qy)
            if best_score is None or score > best_score:
                best_score = score
                maximizers = [point]
            elif score == best_score:
                maximizers.append(point)

        assert best_score is not None

        accumulator = [Fraction(0) for _ in range(self._value_width or 0)]
        total_count = 0
        entry_indices: list[int] = []
        for point in maximizers:
            for coord_index, coord in enumerate(point.value_sum):
                accumulator[coord_index] += coord
            total_count += point.count
            entry_indices.extend(point.entry_indices)

        averaged = tuple(coord / Fraction(total_count) for coord in accumulator)
        return HardmaxResult(
            score=_normalize_number(best_score),
            value=_restore_value(averaged, self._scalar_mode),
            maximizer_indices=tuple(entry_indices),
        )


__all__ = ["HullKVCache"]
