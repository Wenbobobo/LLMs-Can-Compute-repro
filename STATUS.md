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
- The `P7` stage is now complete on the current frozen scope: the manuscript
  freeze pass, appendix freeze pass, and release-preflight lane are defined and
  synchronized under explicit freeze criteria and blocked-blog rules.
- `results/P1_paper_readiness/summary.json` now reports `10/10` ready
  figure/table items and no blocked or partial items on the frozen current
  scope.
- The current repository therefore remains at the freeze-candidate checkpoint,
  and the post-`P7` stabilization lanes are now defined: `P8` locks the
  submission-candidate bundle, `H2` promotes bundle-lock/release-hygiene
  audits, and `P9` freezes the restrained public surface.

## Immediate Next Actions

1. Keep `README.md`, `STATUS.md`, and future short public-surface syncs
   downstream of `docs/publication_record/release_summary_draft.md` and
   `docs/publication_record/release_candidate_checklist.md`.
2. Execute `P8` against the frozen manuscript bundle, appendix minimum package,
   and paper-facing ledgers without widening claims.
3. Keep `P1`, `P5`, and `H2` audits green while the post-`P7` stabilization
   package is active.
4. Reopen precision, systems, or compiled-boundary evidence only through the
   explicit `E1` conditional reopen protocol; otherwise keep the current `D0`
   endpoint fixed.

## Known Blockers

- Broader compiled demos remain blocked by the current no-widening boundary.
- Broader outward narrative remains blocked by the current restrained-release
  policy.
- Current-scope end-to-end systems superiority remains unsupported by the
  current systems gate.
- No operational repo-hygiene blocker is active on the current worktrees.
