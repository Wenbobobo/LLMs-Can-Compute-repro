# Status

The geometry branch now has:

- an exact brute-force hard-max oracle,
- a correctness-first `HullKVCache`,
- tie and degeneracy tests,
- and a recorded benchmark in `results/M2_geometry_core/benchmark_geometry.json`.

Current recorded benchmark trend:

- about `42.8x` speedup at history length `128`,
- about `121.6x` at `512`,
- about `220.5x` at `2048`,
- about `249.1x` at `8192`.

This is still a correctness-first cache. The main remaining geometry question is
less about exactness and more about dynamic maintenance and finite-precision
address scaling.
