# Freeze Candidate Criteria

This file defines the minimum conditions for calling the current manuscript
bundle a freeze candidate on the frozen paper scope.

## Must-pass criteria

1. Claim boundaries stay fixed.
   The manuscript, release summary, README, and STATUS must keep the current
   narrow scope explicit: append-only traces, exact latest-write retrieval, the
   staged-neural caveat, the bounded precision story, the mixed systems gate,
   and the tiny typed-bytecode `D0` endpoint. No arbitrary-C, general-LLM, or
   broader systems-superiority language may appear.
2. The current main-text artifact set stays fixed and ready.
   The paper-ready bundle must continue to report the existing `10/10` ready
   figure/table items on the frozen scope, and the intended main-text order
   must match `main_text_order.md`.
3. Manuscript structure and callouts stay synchronized.
   The section-ordered manuscript bundle, caption notes, narrative-role ledger,
   and section map must agree on which artifacts belong to which sections. The
   Methods section stays prose-first, and the systems gate stays an inline
   paragraph rather than a standalone main-text table.
4. Appendix companions stay scoped and auditable.
   Required appendix companions and allowed optional companions must follow
   `appendix_companion_scope.md`. No companion artifact may be promoted into a
   broader claim without a separate recorded scope change.
5. Release-facing derivatives remain downstream.
   `release_summary_draft.md` remains the short-update source for README and
   STATUS. Those public surfaces may summarize the frozen paper scope, but they
   may not outrun the manuscript bundle or soften the blocked-blog rule.
6. Narrow audits remain green.
   The public-surface sync audit and the main-text callout-alignment audit must
   pass on the current repo state before the bundle is called frozen.

## Required evidence anchors

- `results/P1_paper_readiness/summary.json`
- `results/P5_public_surface_sync/summary.json`
- `results/P5_callout_alignment/summary.json`
- `docs/publication_record/main_text_order.md`
- `docs/publication_record/appendix_companion_scope.md`
- `docs/publication_record/release_preflight_checklist.md`

## Reopen only if

- a new evidence wave deliberately reopens precision, systems, or frontend
  scope;
- the mandatory figure/table set changes;
- the manuscript no longer matches the current callout or appendix ledgers.
