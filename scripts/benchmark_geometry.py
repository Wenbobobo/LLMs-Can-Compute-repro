"""Benchmark brute-force hard-max against the correctness-first HullKVCache."""

from __future__ import annotations

import json
import random
import time

from geometry import HullKVCache, brute_force_hardmax_2d


def timed_call(fn, *args, repeats: int = 1):
    started = time.perf_counter()
    for _ in range(repeats):
        fn(*args)
    finished = time.perf_counter()
    return finished - started


def main() -> None:
    rng = random.Random(0)
    sizes = [128, 512, 2048, 8192]
    query_count = 2_000
    rows = []

    for size in sizes:
        keys = [(rng.randint(-500, 500), rng.randint(-500, 500)) for _ in range(size)]
        values = [rng.randint(-100, 100) for _ in range(size)]
        queries = [
            (rng.randint(-500, 500), rng.choice([value for value in range(-500, 501) if value != 0]))
            for _ in range(query_count)
        ]

        cache = HullKVCache()
        insert_seconds = timed_call(cache.extend, keys, values)
        brute_seconds = timed_call(
            lambda: [brute_force_hardmax_2d(keys, values, query) for query in queries]
        )
        cache_seconds = timed_call(lambda: [cache.query(query) for query in queries])

        rows.append(
            {
                "history_size": size,
                "query_count": query_count,
                "insert_seconds": insert_seconds,
                "brute_force_seconds": brute_seconds,
                "cache_seconds": cache_seconds,
                "cache_speedup_vs_bruteforce": brute_seconds / cache_seconds if cache_seconds else None,
            }
        )

    print(json.dumps({"benchmark": "geometry_hardmax", "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
