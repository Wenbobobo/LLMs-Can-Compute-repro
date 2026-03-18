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
- M4 neural event executor: a trainable structured-event decoder now learns opcode-conditioned transition labels and reaches exact rollout on current held-out countdown, branch, and memory families
- M4 finite-precision stress: scheme-aware address-range failure sweeps now compare single-head, radix-2, and block-recentered latest-write addressing
- M4 factorized event decoder: a richer direct event-value decoder now trains on recent event history plus top-of-stack summaries; it reaches moderate teacher-forced label accuracy but still collapses in free-running rollout
- M4 real-trace precision: offset real-trace checks now confirm that single-head finite-precision failures reappear on real memory streams, while the current radix/block schemes recover the current offset suite
- M5 scaffold: structured trace dataset, vocabulary helpers, optional Torch baseline definition, and dataset preview artifact added
- M5 CUDA baseline run: first teacher-forced training run completed on the tiny 2D-head softmax model, with nontrivial teacher-forced accuracy but zero exact free-running rollout on current eval groups
- M5 representation ablation: atomic whole-token vs factorized digit-level vs event-grouped serializations now run side by side; event grouping reduces sequence length and improves held-out teacher-forced accuracy slightly, but exact rollout still remains zero
- M5 event-level baseline: the final standard softmax baseline now shares the factorized event target with the richer M4 branch; it remains a stronger negative control with near-zero exact-label accuracy and zero exact rollout
- Runtime environment export: Python 3.12.9, `torch==2.10.0+cu128`, and CUDA device info are now recorded under `results/runtime_environment.json`
- Packaging fix: renamed the trace package to avoid the Python stdlib conflict
- Public GitHub repo created and initial push completed

## Immediate Next Actions

1. Decide whether the direct `M4` factorized event decoder should get one more structural intervention, likely staged address/value decoding or pointer-like value heads, before freezing it as the current hard case.
2. Extend `M4-B` from the current offset real-trace suite to longer horizons and base sweeps, because real traces now validate the failure mode but not yet the full scaling envelope.
3. Freeze `M5` as the current negative control unless one last narrowly scoped repair is justified by the new event-level artifact.

## Known Blockers

- None at the repository/bootstrap layer.
- The main remaining risks are scientific: direct event-value rollout stability,
  tie semantics at scale, finite-precision address collapse on longer real
  traces, whether staged decoding is enough to close the direct-decoder gap,
  and whether the `M5` baseline has any remaining scientific value beyond a
  documented negative control.
