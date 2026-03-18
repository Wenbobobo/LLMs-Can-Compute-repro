# Status

## Working State

- M0 scaffold: complete
- M1 claims/scope docs: complete
- M2 geometry exactness: initial implementation added
- M3 trace executor: stack plus bounded-RAM reference semantics implemented
- M4 exact hard-max decode: deterministic latest-write bridge implemented for immediate and dynamic memory addressing plus stack-slot retrieval
- M4 narrow trainable slice: two-parameter stack latest-write scorer fitted and validated on held-out longer traces
- M4 free-running exact executor: linear and accelerated online rollout now match the reference trace on current countdown, branch, and bounded-RAM programs
- M4 induced causal executor: structured transition rules fitted from reference traces now generate exact online events on held-out countdown, branch, and indirect-memory programs
- M4 finite-precision stress: recorded address-range failure sweeps for float64/32/bfloat16/float16
- M5 scaffold: structured trace dataset, vocabulary helpers, optional Torch baseline definition, and dataset preview artifact added
- M5 CUDA baseline run: first teacher-forced training run completed on the tiny 2D-head softmax model, with nontrivial teacher-forced accuracy but zero exact free-running rollout on current eval groups
- M5 representation ablation: atomic whole-token vs factorized digit-level serialization now runs side by side; factorization cuts vocab size sharply and delays first error, but exact rollout still remains zero
- Runtime environment export: Python 3.12.9, `torch==2.10.0+cu128`, and CUDA device info are now recorded under `results/runtime_environment.json`
- Packaging fix: renamed the trace package to avoid the Python stdlib conflict
- Public GitHub repo created and initial push completed

## Immediate Next Actions

1. Replace the current induced structured executor with a genuinely neural token/event-level causal branch, or explicitly keep the synthesis-first branch as a separate claim line.
2. Decide the next `M5` move after the factorized ablation: prompt/rollout boundary, event grouping, or model-side changes, because tokenization alone did not produce exact rollout.
3. Push `M4-B` further with address decomposition or rescaling, because `float32` latest-write collapse still blocks any serious long-horizon claim.

## Known Blockers

- None at the repository/bootstrap layer.
- The main remaining risks are scientific: representation choices, tie semantics
  at scale, finite-precision address collapse, tokenization-induced baseline
  brittleness, and how far the current fast path generalizes beyond the toy
  executor.
