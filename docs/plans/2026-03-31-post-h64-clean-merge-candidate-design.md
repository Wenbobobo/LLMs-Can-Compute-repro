# 2026-03-31 Post-H64 Clean Merge-Candidate Design

## Recommended Main Route

`P56_post_h64_clean_merge_candidate_packet` is the recommended main route.

Why this route dominates:

- it preserves `H64` as the current active docs-only packet;
- it continues the clean-descendant-only posture without routing through dirty
  root `main`;
- it keeps runtime closed and leaves `R63` dormant and non-runtime only; and
- it produces concrete merge-prep, paper-facing, archive-facing, and control
  artifacts without reopening speculative science.

The approved execution order is:

`P56 -> (P57 || P58) -> P59`

where `P57` and `P58` are operational sidecars beneath the stable `H64`
packet, and `P59` is the serial control/handoff refresh after those sidecars
land.

## Locked Facts

- active docs-only packet:
  `H64_post_p53_p54_p55_f38_archive_first_freeze_packet`
- preserved prior active packet:
  `H63_post_p50_p51_p52_f38_archive_first_closeout_packet`
- preserved strongest executor-value closeout:
  `H58_post_r62_origin_value_boundary_closeout_packet`
- preserved paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- current dormant future dossier:
  `F38_post_h62_r63_dormant_eligibility_profile_dossier`
- default downstream lane:
  `archive_or_hygiene_stop`
- merge posture:
  `clean_descendant_only_never_dirty_root_main`
- dirty root `main` remains quarantine-only
- runtime remains closed
- `R63` remains dormant and non-runtime only
- do not mint `H65` in this phase

## Wave 1

### `P56_post_h64_clean_merge_candidate_packet`

Objective:
stage a `P27`-style explicit clean merge-candidate packet above the published
`H64` freeze stack without executing any merge.

Required inputs:

- `results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json`
- `results/P54_post_h63_clean_descendant_hygiene_and_artifact_slimming/summary.json`
- `results/P55_post_h63_clean_descendant_promotion_prep/summary.json`
- the clean source branch `wip/h64-post-h63-archive-first-freeze`
- the clean main snapshot worktree `wip/p56-main-scratch`

Expected outputs:

- `docs/milestones/P56_post_h64_clean_merge_candidate_packet/`
- `scripts/export_p56_post_h64_clean_merge_candidate_packet.py`
- `tests/test_export_p56_post_h64_clean_merge_candidate_packet.py`
- `results/P56_post_h64_clean_merge_candidate_packet/`

Stop conditions:

- source branch is not readable or not comparable against `main`;
- dirty root quarantine is missing; or
- tracked oversize artifacts reappear on the clean descendant line.

Go / no-go:

- go only if `H64`, `P54`, and `P55` summaries stay green and the packet keeps
  `merge_executed = false`;
- no-go if the packet tries to authorize runtime, reopen the executor-value
  lane, or treat dirty root `main` as an integration base.

Expected commits:

- one grouped `P56` docs/scripts/tests/results commit

Worktree / subagent:

- new worktree required:
  `D:/zWenbo/AI/wt/p56-post-h64-clean-merge-candidate`
- clean `main` scratch worktree required:
  `D:/zWenbo/AI/wt/p56-main-scratch`
- subagents optional for read-only review only

## Wave 2

### `P57_post_h64_paper_submission_package_sync`

Objective:
refresh paper-facing and submission-facing package surfaces so they describe
the current `H64 + P56/P57/P58/P59 + F38 + H58/H43` posture coherently.

Required inputs:

- `results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json`
- `results/P56_post_h64_clean_merge_candidate_packet/summary.json`
- the current paper and submission docs under `docs/publication_record/`

Expected outputs:

- `docs/milestones/P57_post_h64_paper_submission_package_sync/`
- `scripts/export_p57_post_h64_paper_submission_package_sync.py`
- `tests/test_export_p57_post_h64_paper_submission_package_sync.py`
- `results/P57_post_h64_paper_submission_package_sync/`

Stop conditions:

- any wording implies runtime reopen, broad Wasm, arbitrary `C`, or dirty-root
  merge;
- any paper-facing doc blurs active `H64` control with preserved `H58/H43`.

Go / no-go:

- go only if the paper/submission surfaces stay downstream of archive-first
  partial falsification;
- no-go if the wave widens the scientific claim boundary.

Expected commits:

- one grouped `P57` docs/scripts/tests/results commit, or one combined
  `P57/P58` sidecar commit if the write set is shared

Worktree / subagent:

- reuse the `P56` worktree
- subagents are discouraged for write work because the paper/archive surfaces
  overlap heavily

## Wave 3

### `P58_post_h64_archive_release_closeout_sync`

Objective:
refresh archive-facing and release-facing closeout surfaces so the current
handoff package is explicit and audit-friendly.

Required inputs:

- `results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json`
- `results/P56_post_h64_clean_merge_candidate_packet/summary.json`
- `results/P57_post_h64_paper_submission_package_sync/summary.json`
- release/archive docs under `docs/publication_record/`

Expected outputs:

- `docs/milestones/P58_post_h64_archive_release_closeout_sync/`
- `scripts/export_p58_post_h64_archive_release_closeout_sync.py`
- `tests/test_export_p58_post_h64_archive_release_closeout_sync.py`
- `results/P58_post_h64_archive_release_closeout_sync/`

Stop conditions:

- release/archive docs fall out of sync with the paper-facing package;
- the outward wording stops being restrained; or
- the wave implies merge execution or runtime reopen.

Go / no-go:

- go only if the archive/release docs preserve `H64`, `F38`, `H58`, `H43`, and
  the closed runtime posture;
- no-go if the sidecar contradicts the `P56` merge-prep rules.

Expected commits:

- grouped together with `P57` if the doc write set is still overlapping

Worktree / subagent:

- reuse the `P56` worktree
- no separate write-side subagent unless the write set is made disjoint first

## Wave 4

### `P59_post_h64_control_and_handoff_sync`

Objective:
refresh the control driver, milestone/plan indexes, active-wave file, and next
handoff/startup prompt to the landed `H64 + P56/P57/P58/P59` state.

Required inputs:

- `results/P56_post_h64_clean_merge_candidate_packet/summary.json`
- `results/P57_post_h64_paper_submission_package_sync/summary.json`
- `results/P58_post_h64_archive_release_closeout_sync/summary.json`
- current control surfaces:
  `docs/publication_record/current_stage_driver.md`,
  `docs/plans/README.md`,
  `docs/milestones/README.md`,
  `tmp/active_wave_plan.md`

Expected outputs:

- `docs/milestones/P59_post_h64_control_and_handoff_sync/`
- `scripts/export_p59_post_h64_control_and_handoff_sync.py`
- `tests/test_export_p59_post_h64_control_and_handoff_sync.py`
- `results/P59_post_h64_control_and_handoff_sync/`
- post-`P59` handoff and startup prompt docs

Stop conditions:

- control surfaces disagree about the current active packet or current sidecars;
- the next startup prompt accidentally reopens runtime or same-lane science.

Go / no-go:

- go only if `H64` remains active and `P56/P57/P58/P59` remain operational
  follow-through only;
- no-go if the wave tries to relabel `P56` as a real merge or `P59` as a new
  scientific packet.

Expected commits:

- one grouped `P59` control-sync commit

Worktree / subagent:

- reuse the `P56` worktree
- subagent review is useful only after the control surfaces are written

## Verification

After all four waves:

- run the new packet exporters and tests for `P56`, `P57`, `P58`, and `P59`;
- rerun standing audits:
  `release_worktree_hygiene_snapshot`,
  `release_preflight_checklist_audit`,
  `P10_submission_archive_ready`;
- require the final machine-readable summaries to report:
  `clean_worktree_ready_if_other_gates_green`,
  `docs_and_audits_green`,
  and `archive_ready`.
