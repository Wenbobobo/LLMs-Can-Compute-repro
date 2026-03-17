from __future__ import annotations

import math
import random

from geometry import HullKVCache, brute_force_hardmax_2d


def _assert_same_result(left, right) -> None:
    if isinstance(left.value, tuple):
        assert isinstance(right.value, tuple)
        assert len(left.value) == len(right.value)
        for l_coord, r_coord in zip(left.value, right.value, strict=True):
            assert math.isclose(float(l_coord), float(r_coord), rel_tol=0.0, abs_tol=1e-9)
    else:
        assert math.isclose(float(left.value), float(right.value), rel_tol=0.0, abs_tol=1e-9)

    assert math.isclose(float(left.score), float(right.score), rel_tol=0.0, abs_tol=1e-9)
    assert set(left.maximizer_indices) == set(right.maximizer_indices)


def test_bruteforce_averages_duplicate_maximizers() -> None:
    result = brute_force_hardmax_2d(
        keys=[(2, 3), (2, 3), (0, 0)],
        values=[1, 3, 100],
        query=(1, 1),
    )
    assert result.score == 5
    assert result.value == 2
    assert set(result.maximizer_indices) == {0, 1}


def test_cache_matches_collinear_tie_case() -> None:
    keys = [(0, 0), (1, 1), (2, 2)]
    values = [10, 20, 30]
    query = (1, -1)

    cache = HullKVCache()
    cache.extend(keys, values)

    brute = brute_force_hardmax_2d(keys, values, query)
    accelerated = cache.query(query)
    _assert_same_result(brute, accelerated)


def test_cache_matches_zero_query_average() -> None:
    keys = [(-1, 4), (2, 2), (2, 2)]
    values = [2, 4, 6]

    cache = HullKVCache()
    cache.extend(keys, values)

    brute = brute_force_hardmax_2d(keys, values, (0, 0))
    accelerated = cache.query((0, 0))
    _assert_same_result(brute, accelerated)


def test_cache_matches_vector_value_tie() -> None:
    keys = [(0, 0), (1, 1)]
    values = [(1, 3), (5, 7)]
    query = (1, -1)

    cache = HullKVCache()
    cache.extend(keys, values)

    brute = brute_force_hardmax_2d(keys, values, query)
    accelerated = cache.query(query)
    _assert_same_result(brute, accelerated)


def test_cache_matches_randomized_reference() -> None:
    rng = random.Random(0)
    keys = [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(25)]
    values = [rng.randint(-20, 20) for _ in range(25)]

    cache = HullKVCache()
    cache.extend(keys, values)

    for _ in range(200):
        query = (rng.randint(-5, 5), rng.randint(-5, 5))
        brute = brute_force_hardmax_2d(keys, values, query)
        accelerated = cache.query(query)
        _assert_same_result(brute, accelerated)
