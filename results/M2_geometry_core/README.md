# M2 Geometry Core Results

## Current Recorded Benchmark

Source: `benchmark_geometry.json`

The first benchmark compares:

- brute-force exact 2D hard-max retrieval,
- correctness-first `HullKVCache` query-time retrieval.

Recorded speedups vs brute force:

- history size 128: about `42.8x`
- history size 512: about `121.6x`
- history size 2048: about `220.5x`
- history size 8192: about `249.1x`

## Caveats

- The current cache uses rebuild-based insertion. These numbers should be read as
  evidence for query-path scaling, not as the final end-to-end systems result.
- Tie cases still fall back to an exact scan over aggregated points.
- The benchmark is a first internal checkpoint, not yet a publication-grade
  evaluation.
