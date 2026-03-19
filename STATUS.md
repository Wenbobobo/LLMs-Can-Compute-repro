# Status

## Current Scientific State

- Append-only trace semantics and exact 2D hard-max retrieval remain validated
  on the current scope.
- Staged-neural execution stays caveated by legality structure; the
  widened `opcode_shape` regime fails on held-out rollout, and the provenance
  follow-up ties many later `step_budget` rows to earlier semantic divergence.
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
- Frontend widening is not authorized, README-level release is
  acceptable, and broader blog/demo prose remains blocked.

## Current Paper State

- The paper bundle now has a sentence-polished manuscript section draft,
  appendix draft, caption candidates, layout decisions, and machine-audited
  public-surface / callout guards under `docs/publication_record/`.
- The latest layout/readiness pass has stabilized local figure/table
  placement, caption wording, and release-readiness handoff on the same frozen
  current scope.
- `results/P1_paper_readiness/summary.json` now reports `10/10` ready
  figure/table items and no blocked or partial items on the frozen current
  scope.
- The layout-tightening and release-readiness pass is now complete; remaining
  paper-facing work is manuscript-freeze candidacy, release preflight, and
  restrained public-surface maintenance, not new claim expansion.

## Immediate Next Actions

1. Keep `README.md`, `STATUS.md`, and future short public-surface syncs
   downstream of `docs/publication_record/release_summary_draft.md`.
2. Reconcile remaining legacy unchecked rows under
   `docs/milestones/H1_legacy_backlog_reconciliation/` so unattended runs do
   not misread frozen historical branches as active work.
3. Run the next paper-facing wave as manuscript-freeze candidacy plus release
   preflight under
   `docs/milestones/P7_manuscript_freeze_candidate_and_release_preflight/`.
4. Reopen precision, systems, or frontend widening only if the project
   deliberately starts a new evidence wave; otherwise keep the current `D0`
   endpoint fixed.

## Known Blockers

- Broader compiled demos remain blocked by the current no-widening boundary.
- Broader outward narrative remains blocked by the current restrained-release
  policy.
- Current-scope end-to-end systems superiority remains unsupported by the
  current systems gate.
- No operational repo-hygiene blocker is active on the current worktrees.
