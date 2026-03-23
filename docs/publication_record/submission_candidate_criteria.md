# Submission Candidate Criteria

This file defines the minimum conditions for upgrading the current
freeze-candidate checkpoint into a submission-candidate bundle on the same
frozen scope, currently anchored on the active `H43` docs-only useful-case
refreeze packet, the preserved active `H36` routing/refreeze packet, and the
completed `R42/R43/R44/R45` semantic-boundary gate stack, while preserving
`H42/H41/P28/P27` as immediate decision-and-operational context and
`H35/H34/H33/H32` as earlier same-substrate context.

## Must-pass criteria

1. Freeze-candidate conditions still hold.
   `freeze_candidate_criteria.md` remains the base gate; `P8` can add
   consistency and ledger lock requirements, but it cannot soften the existing
   scope boundaries.
2. Manuscript bundle and supporting ledgers are locked together.
   `manuscript_bundle_draft.md`, `caption_candidate_notes.md`,
   `figure_table_narrative_roles.md`, and `manuscript_section_map.md` must
   agree on the current claim-bearing main-text artifacts and section
   ownership.
3. Appendix minimum package is explicit and complete.
   Required companions under `appendix_companion_scope.md` and
   `appendix_boundary_map.md` must be present, and optional companions must stay
   clearly optional.
4. Claim, threat, and negative-result ledgers stay synchronized.
   `claim_ladder.md`, `claim_evidence_table.md`, `negative_results.md`, and
   `threats_to_validity.md` must describe the same frozen endpoint, the same
   blocked claims, and the same post-`H43` routing boundaries.
5. Release-facing summaries remain downstream.
   `release_summary_draft.md`, `README.md`, and `STATUS.md` may summarize the
   locked bundle, but they may not outrun it, imply a new evidence wave, or
   blur the distinction between active `H43` stage wording, preserved active
   `H36` routing, completed `R42/R43/R44/R45` gate evidence, preserved
   `H42/H41/P28/P27` operational context, and earlier `H35/H34/H33/H32`
   same-substrate evidence.
6. Standing audits remain green.
   `P1`, `P5` public-surface sync, `P5` callout alignment, and the `H2`
   bundle-lock audit must all report zero blocked items on the current repo
   state.

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
- `results/H2_bundle_lock_audit/summary.json`
- `docs/publication_record/current_stage_driver.md`
- `docs/publication_record/main_text_order.md`
- `docs/publication_record/appendix_companion_scope.md`
- `docs/publication_record/conditional_reopen_protocol.md`

## Reopen only if

- a manuscript sentence no longer matches the frozen claim/evidence table;
- a required appendix companion is missing for a main-text claim;
- an audit reports a real bundle-lock failure;
- a later review deliberately authorizes one `E1` patch lane.
