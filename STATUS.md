# Status

## Current Scientific State

- Append-only trace semantics and exact 2D hard-max retrieval remain validated
  on the current scope.
- Staged-neural execution stays caveated by legality structure; the widened
  `opcode_shape` regime fails on held-out rollout, and the provenance follow-up
  ties many later `step_budget` rows to earlier semantic divergence.
- The precision story is a bounded positive, not a broad robustness claim;
  float32 single-head fails on `12/25` tracked real/organic streams,
  `7/25` already at `1x`, while at least one decomposition stays exact on
  `25/25` tracked streams in the validated suite.
- The current compiled endpoint is tiny typed bytecode, with deterministic
  verifier coverage, exact-trace / exact-final-state agreement on the frozen
  starter suite, memory-surface diagnostics, and a stress/reference companion.
- The systems result is mixed; geometry shows a strong asymptotic
  cache-vs-bruteforce win, but the lowered `exec_trace` path is still about
  `1.82x` slower than the best current reference/oracle path on positive `D0`
  suites.
- Frontend widening is not authorized, README-level release is acceptable, and
  broader blog/demo prose remains blocked.

## Current Paper State

- The paper bundle has a locked manuscript bundle, appendix package, caption
  notes, layout decisions, and machine-audited public-surface / callout guards
  under `docs/publication_record/`.
- `results/P1_paper_readiness/summary.json` reports `10/10` ready figure/table
  items and no blocked or partial items on the frozen current scope.
- The `P8` stage is complete on the current frozen scope: the manuscript,
  appendix minimum package, and paper-facing ledgers are locked together under
  explicit submission-candidate criteria.
- The `P9` stage is complete on the same scope: `README.md`, `STATUS.md`,
  `release_summary_draft.md`, and blocked-blog controls are synchronized as a
  restrained release-candidate checkpoint.
- The current active post-`P9` operational stage is checkpoint consolidation
  and archive readiness under `docs/publication_record/current_stage_driver.md`.
- `H3`, `P10`, `P11`, and `F1` are the active non-claim-expanding lanes on top
  of the locked checkpoint.
- No `E1` patch lane is active on the current repo state.

## Immediate Next Actions

1. Keep `README.md`, `STATUS.md`, `docs/publication_record/README.md`, and
   future short public-surface syncs aligned with
   `docs/publication_record/current_stage_driver.md`.
2. Keep `results/P1_paper_readiness/summary.json`,
   `results/P5_public_surface_sync/summary.json`,
   `results/P5_callout_alignment/summary.json`, and
   `results/H2_bundle_lock_audit/summary.json` green while the locked bundle
   remains the active baseline.
3. Build and maintain the venue-agnostic packet under
   `docs/publication_record/submission_packet_index.md` and
   `docs/publication_record/archival_repro_manifest.md` without widening scope.
4. Keep derivative-only writing material downstream of the manuscript bundle
   and keep any future evidence change behind
   `docs/publication_record/conditional_reopen_protocol.md`.

## Known Blockers

- Broader compiled demos remain blocked by the current no-widening boundary.
- Broader outward narrative remains blocked by the current restrained-release
  policy.
- Current-scope end-to-end systems superiority remains unsupported by the
  current systems gate.
- No operational repo-hygiene blocker is active on the current worktrees.
