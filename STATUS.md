# Status

## Working State

- M0 scaffold: complete
- M1 claims/scope docs: complete
- M2 geometry exactness: initial implementation added
- M3 trace executor: stack plus bounded-RAM reference semantics implemented
- M4 exact hard-max decode: deterministic latest-write bridge implemented for immediate and dynamic memory addressing plus stack-slot retrieval
- M4 narrow trainable slice: two-parameter stack latest-write scorer fitted and validated on held-out longer traces
- Packaging fix: renamed the trace package to avoid the Python stdlib conflict
- Public GitHub repo created and initial push completed

## Immediate Next Actions

1. Decide whether the next `M4` step should be free-running prediction in the current stack family or mixed memory/stack retrieval.
2. Replace the fixed candidate-set scorer with a causal learned decode loop that must emit or select writes online.
3. Keep separating narrow validated claims from broader executor rhetoric.

## Known Blockers

- None at the repository/bootstrap layer.
- The main remaining risks are scientific: representation choices, tie semantics
  at scale, and how far the current fast path generalizes beyond the toy executor.
