# TODO

Legacy note: the remaining unchecked row is tracked in
`docs/milestones/H1_legacy_backlog_reconciliation/classification_matrix.md`
and is not active on the current frozen paper scope by default.

- [x] Implement brute-force hard-max reference
- [x] Implement correctness-first `HullKVCache`
- [x] Add unit tests for ties and degeneracies
- [x] Add benchmark script
- [x] Run exhaustive and randomized tests
- [x] Record the first benchmark outputs in `results/M2_geometry_core/`
- Dormant follow-up: decide between dynamic hull maintenance and better
  finite-precision scaling only if `R3` or `R4` reopens geometry as a current
  bottleneck.
