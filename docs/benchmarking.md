# Benchmarking

## Rules

- Always compare against a clear reference path.
- Record hardware, Python version, and exact script invocation.
- Separate insertion cost from query cost when possible.
- Report both asymptotic trends and constant-factor caveats.
- Treat correctness failures as benchmark blockers, not footnotes.

## Geometry Benchmarks

- Compare brute-force hard-max against `HullKVCache`.
- Use at least two orders of magnitude in history length.
- Include tie-heavy and tie-light query regimes separately when relevant.

## Executor Benchmarks

- Report exact full-trace success rate, not only next-token accuracy.
- Bucket by trace length and show first-error position distributions.
- Keep linear-scan and accelerated decode timings separate.
