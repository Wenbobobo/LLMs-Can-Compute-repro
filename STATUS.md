# Status

## Current Scientific State

- `A1/B1`: append-only trace semantics and exact 2D hard-max retrieval remain
  validated on the current scope.
- `C2h`: staged-neural execution stays caveated by legality structure; the
  widened `opcode_shape` regime fails on held-out rollout, and the provenance
  follow-up ties many later `step_budget` rows to earlier semantic divergence.
- `C3e/R1`: the precision story is a bounded positive, not a broad robustness
  claim; float32 single-head fails on `12/25` tracked real/organic streams,
  `7/25` already at `1x`, while at least one decomposition stays exact on
  `25/25` tracked streams in the validated suite.
- `D0`: the current compiled endpoint is tiny typed bytecode, with deterministic
  verifier coverage, exact-trace / exact-final-state agreement on the frozen
  starter suite, memory-surface diagnostics, and a stress/reference companion.
- `R2`: the systems result is mixed; geometry shows a strong asymptotic
  cache-vs-bruteforce win, but the lowered `exec_trace` path is still about
  `1.82x` slower than the best current reference/oracle path on positive `D0`
  suites.
- `M7/P4`: frontend widening is not authorized, README-level release is
  acceptable, and broader blog/demo prose remains blocked.

## Current Paper State

- `P5` now has a manuscript section draft, appendix draft, caption candidates,
  and layout decisions under `docs/publication_record/`.
- `results/P1_paper_readiness/summary.json` now reports `10/10` ready
  figure/table items and no blocked or partial items on the frozen current
  scope.
- Remaining paper-lane work is sentence-level polish, figure/table callout
  cleanup, and restrained public-surface maintenance, not new claim expansion.

## Immediate Next Actions

1. Keep `README.md`, `STATUS.md`, and `docs/publication_record/` aligned, with
   future short public-surface syncs derived from
   `docs/publication_record/release_summary_draft.md`.
2. Reopen `R1` or `R2` only if the project deliberately chooses a new evidence
   wave; otherwise keep the current `D0` endpoint fixed.
3. Keep frontend widening and blog release blocked unless a future scope change
   clears both the systems and public-release gates.

## Known Blockers

- Broader compiled demos remain blocked by `M7`.
- Broader outward narrative remains blocked by `P4`.
- Current-scope end-to-end systems superiority remains unsupported by `R2`.
- No operational repo-hygiene blocker is active on the current worktrees.
