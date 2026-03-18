# Status

## Working State

- M0 scaffold: complete
- M1 claims/scope docs: complete
- M2 geometry exactness: initial implementation added
- M3 trace executor: stack plus bounded-RAM reference semantics implemented
- M4 exact hard-max decode: deterministic latest-write bridge implemented for immediate and dynamic memory addressing plus stack-slot retrieval
- M4 narrow trainable slice: two-parameter stack latest-write scorer fitted and validated on held-out longer traces
- M4 free-running exact executor: linear and accelerated online rollout now match the reference trace on current countdown, branch, and bounded-RAM programs
- M4 finite-precision stress: recorded address-range failure sweeps for float64/32/bfloat16/float16
- M5 scaffold: structured trace dataset, vocabulary helpers, optional Torch baseline definition, and dataset preview artifact added
- Packaging fix: renamed the trace package to avoid the Python stdlib conflict
- Public GitHub repo created and initial push completed

## Immediate Next Actions

1. Replace the fixed stack candidate-set scorer with a causal learned decode loop that emits or selects event decisions online.
2. Decide whether the next learned `M4` target should be mixed memory-plus-stack execution or a deeper stack-only family without exact memory fallback.
3. Install and run the first actual `M5` softmax baseline training slice.

## Known Blockers

- None at the repository/bootstrap layer.
- The main remaining risks are scientific: representation choices, tie semantics
  at scale, finite-precision address collapse, and how far the current fast path
  generalizes beyond the toy executor.
