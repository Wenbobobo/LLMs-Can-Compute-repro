# Release Preflight Checklist

This checklist defines the minimum outward-facing sync required after the
current archive-first closeout bundle is assembled.

## Wording and scope

- [ ] `README.md` stays a restrained landing page and keeps the blocked broad
  non-goals explicit.
- [ ] `STATUS.md` reflects current
  `H64_post_p53_p54_p55_f38_archive_first_freeze_packet` as the active
  docs-only packet, preserves
  `H63_post_p50_p51_p52_f38_archive_first_closeout_packet` as the prior
  active packet, and exposes `P53/P54/P55/F38` plus
  `archive_or_hygiene_stop`.
- [ ] `release_summary_draft.md` uses archive-first partial falsification as
  the outward shorthand: narrow mechanistic reproduction survives, the broad
  headline does not, the strongest justified executor-value lane is closed
  negative, and `R63` remains dormant and non-runtime only.
- [ ] `release_candidate_checklist.md`,
  `submission_candidate_criteria.md`, `claim_ladder.md`, and
  `archival_repro_manifest.md` expose the same current `H64/P53/P54/P55/F38`
  stack while preserving `H58` as the value-negative closeout and `H43` as the
  preserved paper-grade endpoint.
- [ ] `publication_record/README.md` and `plans/README.md` both expose the
  completed `H64/P53/P54/P55/F38` chain above preserved `H63/H62/H61/H60/H59/H58`
  and preserved paper-grade `H43`.
- [ ] `blog_release_rules.md` still records the blocked-blog state explicitly.

## Paper-facing ledgers

- [ ] `manuscript_bundle_draft.md`, `paper_bundle_status.md`,
  `layout_decision_log.md`, `freeze_candidate_criteria.md`,
  `main_text_order.md`, and `appendix_companion_scope.md` remain
  synchronized.
- [ ] `submission_candidate_criteria.md` preserves `H43` as the paper-grade
  endpoint under active `H63` control rather than treating `H43` as the
  current active packet.
- [ ] `review_boundary_summary.md` and
  `external_release_note_skeleton.md` stay downstream of archive-first partial
  falsification and do not imply runtime reopen, same-lane executor-value
  replay, broad Wasm, or arbitrary `C`.
- [ ] No outward-facing text treats `R63` as runtime-authorized or imports
  private source material from `docs/origin/` or `docs/Origin/`.

## Machine-audited guards

- [ ] `results/P1_paper_readiness/summary.json` still reports `10/10` ready
  figure/table items on the frozen scope.
- [ ] `results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json`
  reports
  `archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant`,
  `archive_or_hygiene_stop`, and closed runtime.
- [ ] `results/P53_post_h63_paper_archive_claim_sync/summary.json` reports
  `paper_archive_review_surfaces_locked_to_h64_archive_first_freeze`.
- [ ] `results/P54_post_h63_clean_descendant_hygiene_and_artifact_slimming/summary.json`
  reports
  `clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution`,
  `tracked_oversize_count = 0`, and `raw_row_ignore_rules_active = true`.
- [ ] `results/P55_post_h63_clean_descendant_promotion_prep/summary.json`
  reports `clean_descendant_promotion_prep_refreshed_for_h64_archive_first_freeze`
  and `merge_execution_state = false`.
- [ ] `results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json`
  reports `runtime_authorization = closed`, keeps the exact target declared,
  and keeps cost share, query:insert ratio, tie burden, and materially
  different cost model unresolved.
- [ ] `results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json`
  reports
  `stop_as_mechanism_supported_but_no_bounded_executor_value`.
- [ ] `results/H43_post_r44_useful_case_refreeze/summary.json` still reports
  `freeze_r44_as_narrow_supported_here` and
  `claim_d_state = supported_here_narrowly`.
- [ ] `results/P5_public_surface_sync/summary.json`,
  `results/P5_callout_alignment/summary.json`, and
  `results/H2_bundle_lock_audit/summary.json` all report zero blocked items.
- [ ] `results/release_worktree_hygiene_snapshot/summary.json` still classifies
  release-commit readiness without `git diff --check` content issues.
- [ ] `results/V1_full_suite_validation_runtime_timing_followup/summary.json`
  reports `healthy_but_slow` with zero timed-out files.

## Release hygiene

- [ ] Use `results/release_worktree_hygiene_snapshot/summary.json` to decide
  whether an outward sync commit is currently blocked by a dirty tree.
- [ ] No public release surface routes through dirty root `main`.
- [ ] No local-only source material under `docs/Origin/` or `docs/origin/`
  enters the public surface.
- [ ] Blog work remains blocked unless `blog_release_rules.md` is satisfied in
  full.
