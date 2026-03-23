# Freeze Candidate Criteria

This file defines the minimum conditions for calling the current manuscript
bundle a freeze candidate on the frozen paper scope, currently anchored on the
active `H43` docs-only useful-case refreeze packet, the preserved active
`H36` routing/refreeze packet, and the completed `R42/R43/R44/R45`
semantic-boundary gate stack, while preserving `H42/H41/P28/P27` as immediate
decision-and-operational context and `H35/H34/H33/H32` as earlier
same-substrate context.

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
   may not outrun the manuscript bundle, blur the distinction between active
   `H43` stage wording, preserved active `H36` routing, completed
   `R42/R43/R44/R45` gate evidence, preserved `H42/H41/P28/P27` operational
   context, and earlier `H35/H34/H33/H32` same-substrate context, or soften
   the blocked-blog rule.
6. Narrow audits remain green.
   The public-surface sync audit and the main-text callout-alignment audit must
   pass on the current repo state before the bundle is called frozen.

## Required evidence anchors

- `results/P1_paper_readiness/summary.json`
- `results/H43_post_r44_useful_case_refreeze/summary.json`
- `results/H36_post_r40_bounded_scalar_family_refreeze/summary.json`
- `results/R43_origin_bounded_memory_small_vm_execution_gate/summary.json`
- `results/R44_origin_restricted_wasm_useful_case_execution_gate/summary.json`
- `results/R45_origin_dual_mode_model_mainline_gate/summary.json`
- `results/P27_post_h41_clean_promotion_and_explicit_merge_packet/summary.json`
- `results/P28_post_h43_publication_surface_sync/summary.json`
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
