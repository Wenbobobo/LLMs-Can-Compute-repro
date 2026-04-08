"""Reference implementation for exact 2D hard-max retrieval."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

NumberLike = int | float | Fraction
ValueLike = NumberLike | Sequence[NumberLike]


def _as_fraction(value: NumberLike) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction(str(value))
    raise TypeError(f"Unsupported numeric type: {type(value)!r}")


def _normalize_number(value: Fraction) -> NumberLike:
    if value.denominator == 1:
        return int(value)
    return float(value)


def _coerce_key(key: Sequence[NumberLike]) -> tuple[Fraction, Fraction]:
    if len(key) != 2:
        raise ValueError(f"Expected a 2D key/query, got {len(key)} dimensions.")
    return (_as_fraction(key[0]), _as_fraction(key[1]))


def _coerce_value(value: ValueLike) -> tuple[tuple[Fraction, ...], bool]:
    if isinstance(value, (int, float, Fraction)):
        return ((_as_fraction(value),), True)

    coords = tuple(_as_fraction(coord) for coord in value)
    if not coords:
        raise ValueError("Value vectors must be non-empty.")
    return (coords, False)


def _restore_value(value: tuple[Fraction, ...], is_scalar: bool) -> NumberLike | tuple[NumberLike, ...]:
    restored = tuple(_normalize_number(coord) for coord in value)
    if is_scalar:
        return restored[0]
    return restored


def dot_2d(key: Sequence[NumberLike], query: Sequence[NumberLike]) -> Fraction:
    kx, ky = _coerce_key(key)
    qx, qy = _coerce_key(query)
    return (kx * qx) + (ky * qy)


@dataclass(frozen=True, slots=True)
class HardmaxResult:
    """Exact hard-max retrieval result."""

    score: NumberLike
    value: NumberLike | tuple[NumberLike, ...]
    maximizer_indices: tuple[int, ...]


def brute_force_hardmax_2d(
    keys: Sequence[Sequence[NumberLike]],
    values: Sequence[ValueLike],
    query: Sequence[NumberLike],
) -> HardmaxResult:
    """Return the exact hard-max result over 2D keys.

    Ties are resolved by averaging the values of all maximizers elementwise.
    """

    if len(keys) != len(values):
        raise ValueError("keys and values must have the same length.")
    if not keys:
        raise ValueError("At least one key/value pair is required.")

    scalar_flags = []
    coerced_values: list[tuple[Fraction, ...]] = []
    for value in values:
        coerced, is_scalar = _coerce_value(value)
        scalar_flags.append(is_scalar)
        coerced_values.append(coerced)

    first_shape = len(coerced_values[0])
    if any(len(item) != first_shape for item in coerced_values):
        raise ValueError("All values must have the same dimensionality.")

    if any(flag != scalar_flags[0] for flag in scalar_flags):
        raise ValueError("Do not mix scalar and vector values in one retrieval call.")

    qx, qy = _coerce_key(query)
    best_score: Fraction | None = None
    maximizer_indices: list[int] = []

    for index, key in enumerate(keys):
        # Inline dot product to avoid repeated tuple allocation and length checking
        kx, ky = _coerce_key(key)
        score = (kx * qx) + (ky * qy)
        if best_score is None or score > best_score:
            best_score = score
            maximizer_indices = [index]
        elif score == best_score:
            maximizer_indices.append(index)

    assert best_score is not None

    accumulator = [Fraction(0) for _ in range(first_shape)]
    for index in maximizer_indices:
        for coord_index, coord in enumerate(coerced_values[index]):
            accumulator[coord_index] += coord

    divisor = Fraction(len(maximizer_indices))
    averaged = tuple(coord / divisor for coord in accumulator)
    return HardmaxResult(
        score=_normalize_number(best_score),
        value=_restore_value(averaged, scalar_flags[0]),
        maximizer_indices=tuple(maximizer_indices),
    )


__all__ = ["HardmaxResult", "ValueLike", "brute_force_hardmax_2d", "dot_2d"]
