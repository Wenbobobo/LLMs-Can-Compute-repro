# Release Candidate Checklist

State: `standing_gate`.

This checklist defines the minimum outward-facing sync required for a
restrained release-candidate posture after the current
`H63_post_p50_p51_p52_f38_archive_first_closeout_packet` stack.

## Wording and scope

- [ ] `README.md` keeps the narrow endpoint and blocked non-goals explicit.
- [ ] `STATUS.md` matches active `H63`, preserved prior active `H62`, current
  `P50/P51/P52/F38`, default downstream lane `archive_or_hygiene_stop`, and
  closed runtime.
- [ ] `release_summary_draft.md` remains the short public-surface source for
  archive-first partial falsification.
- [ ] No outward wording implies a new runtime lane, a same-lane replay, broad
  Wasm, arbitrary `C`, or a dirty-root-`main` merge.

## Paper-facing dependencies

- [ ] `submission_candidate_criteria.md` is satisfied on the current repo
  state.
- [ ] `paper_bundle_status.md`, `review_boundary_summary.md`,
  `publication_record/README.md`, and `current_stage_driver.md` all describe
  the same current `H63/P50/P51/P52/F38` package together with preserved
  `H58/H43`.
- [ ] `submission_packet_index.md` and `archival_repro_manifest.md` present
  the same handoff: `H63` as current active packet, `P51` as paper-facing
  package, `P52` as hygiene sidecar, `F38` as the dormant future dossier, and
  `H58/H43` as preserved scientific endpoints underneath.
- [ ] `external_release_note_skeleton.md` stays downstream of archive-first
  partial falsification, keeps the broad headline negative, and keeps `R63`
  dormant and non-runtime only.
- [ ] The blocked-blog rule remains explicit in both `blog_release_rules.md`
  and any derivative release-note surface.

## Machine-audited guards

- [ ] `results/P1_paper_readiness/summary.json` still reports `10/10` ready
  items on the frozen scope.
- [ ] `results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json`
  reports the current active packet and archive-first closeout outcome.
- [ ] `results/P50_post_h62_archive_first_control_sync/summary.json` reports
  locked control surfaces.
- [ ] `results/P51_post_h62_paper_facing_partial_falsification_package/summary.json`
  reports archive-first partial falsification with dormant non-runtime future
  posture.
- [ ] `results/P52_post_h62_clean_descendant_hygiene_and_merge_prep/summary.json`
  reports clean-descendant-only hygiene, zero tracked oversize artifacts, and
  active raw-row ignore rules.
- [ ] `results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json`
  keeps runtime closed and the cost-profile fields unresolved.
- [ ] `results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json`
  preserves the strongest justified executor-value lane as closed negative.
- [ ] `results/H43_post_r44_useful_case_refreeze/summary.json` preserves the
  paper-grade endpoint.
- [ ] `results/release_preflight_checklist_audit/summary.json` reports
  `docs_and_audits_green`.
- [ ] `results/release_worktree_hygiene_snapshot/summary.json` reports a clean
  or warnings-only diff state.

## Release hygiene

- [ ] Any outward commit is blocked if `release_worktree_hygiene_snapshot`
  reports a dirty release state.
- [ ] No release or archive step routes through dirty root `main`.
- [ ] No public-facing note cites `docs/origin/` or `docs/Origin/` directly.
