# Submission Candidate Criteria

This file defines the minimum conditions for upgrading the current
archive-first closeout checkpoint into a submission-candidate bundle on the
same frozen paper scope. Active control is now anchored on
`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`,
`P51_post_h62_paper_facing_partial_falsification_package`,
`P52_post_h62_clean_descendant_hygiene_and_merge_prep`, and
`F38_post_h62_r63_dormant_eligibility_profile_dossier`, while preserving
`H58_post_r62_origin_value_boundary_closeout_packet` as the strongest
executor-value closeout and `H43_post_r44_useful_case_refreeze` as the
preserved paper-grade endpoint.

## Must-pass criteria

1. Freeze-candidate conditions still hold.
   `freeze_candidate_criteria.md` remains the base gate; a submission bundle
   cannot soften the existing frozen paper scope.
2. Manuscript bundle and supporting ledgers are locked together.
   `manuscript_bundle_draft.md`, `caption_candidate_notes.md`,
   `figure_table_narrative_roles.md`, and `manuscript_section_map.md` must
   agree on the current claim-bearing artifact set and section ownership.
3. Appendix minimum package is explicit and complete.
   Required companions under `appendix_companion_scope.md` and
   `appendix_boundary_map.md` must be present, and optional companions must
   stay clearly optional.
4. Claim, threat, and negative-result ledgers stay synchronized.
   `claim_ladder.md`, `claim_evidence_table.md`, `negative_results.md`, and
   `threats_to_validity.md` must describe the same archive-first closeout
   reading: narrow mechanism support survives, the strongest justified
   executor-value lane is closed negative, the broad headline does not land,
   and `R63` remains dormant and non-runtime only.
5. Release-facing summaries remain downstream.
   `release_summary_draft.md`, `README.md`, and `STATUS.md` may summarize the
   locked bundle, but they may not outrun it, blur active `H63` control with
   preserved `H58/H43`, or imply a new runtime lane.
6. Standing audits remain green.
   `P1`, `P5` public-surface sync, `P5` callout alignment, the `H2`
   bundle-lock audit, and `release_preflight_checklist_audit` must all report
   zero blocked release-facing items on the current repo state.
7. Repo hygiene stays publication-safe.
   `P52` and `release_worktree_hygiene_snapshot` must keep clean-descendant-only
   merge posture explicit, dirty root `main` quarantined, and large raw-row
   artifacts out of git.

## Required evidence anchors

- `results/P1_paper_readiness/summary.json`
- `results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json`
- `results/P51_post_h62_paper_facing_partial_falsification_package/summary.json`
- `results/P52_post_h62_clean_descendant_hygiene_and_merge_prep/summary.json`
- `results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json`
- `results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json`
- `results/H43_post_r44_useful_case_refreeze/summary.json`
- `results/P5_public_surface_sync/summary.json`
- `results/P5_callout_alignment/summary.json`
- `results/H2_bundle_lock_audit/summary.json`
- `results/release_preflight_checklist_audit/summary.json`
- `docs/publication_record/current_stage_driver.md`
- `docs/publication_record/main_text_order.md`
- `docs/publication_record/appendix_companion_scope.md`
- `docs/publication_record/conditional_reopen_protocol.md`

## Reopen only if

- a manuscript sentence no longer matches the frozen claim/evidence table;
- a required appendix companion is missing for a main-text claim;
- an audit reports a real bundle-lock or release-surface failure; or
- a later explicit paper-facing control packet authorizes a new downstream
  wording change without reopening runtime.
