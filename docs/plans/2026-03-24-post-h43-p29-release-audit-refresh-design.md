# 2026-03-24 Post-H43 P29 Release Audit Refresh Design

## Objective

Keep the scientific stage fixed at
`H43_post_r44_useful_case_refreeze` while refreshing the stale
release/public audit surfaces that still lag the landed
`H43/R44/R45/R43/P27/P28` control stack. The design goal is narrow:

- keep `H43` as the current active docs-only scientific packet;
- keep `H36` as the preserved routing/refreeze packet underneath the stack;
- refresh stale machine release/public audits so they stop reporting older
  checkpoints as current;
- refresh the last contradictory release-facing ledgers that still describe
  `H40` or `H32/H34` as current control;
- refresh the canonical release worktree hygiene snapshot on the clean `P29`
  worktree and remove orphan legacy hygiene outputs; and
- leave `next_required_lane = no_active_downstream_runtime_lane`.

## Options

### Recommended: `P29_post_h43_release_audit_refresh`

Land one low-priority operational release/public audit refresh packet
downstream of the already completed `H43` scientific state. This keeps the
scientific/control separation explicit: `H43` remains the current stage
driver, while `P29` records that the stale downstream audits and contradictory
release ledgers have been refreshed to the landed stack.

### Rejected: refresh only `P5` and `release_preflight`

This would fix the two clearest stale machine summaries, but it would leave
release-facing ledgers such as the release-candidate checklist and archival
manifest contradicting the refreshed machine state.

### Rejected: merge review now

`P27` already records explicit merge posture and still leaves
`merge_executed = false`. A merge-review wave is a separate operational
decision and should not be mixed with release/public audit refresh.

## Packet Shape

`P29` should export:

- `summary.json`
- `checklist.json`
- `snapshot.json`

The packet should refresh only the minimum downstream operational/control
surfaces that still lag the landed `H43` stack:

- `docs/publication_record/release_candidate_checklist.md`
- `docs/publication_record/freeze_candidate_criteria.md`
- `docs/publication_record/submission_candidate_criteria.md`
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/archival_repro_manifest.md`
- `docs/publication_record/release_preflight_checklist.md`
- `docs/publication_record/README.md`
- `docs/publication_record/experiment_manifest.md`
- `docs/plans/README.md`
- `docs/milestones/README.md`
- `tmp/active_wave_plan.md`
- `scripts/export_release_preflight_checklist_audit.py`
- `scripts/export_p5_public_surface_sync.py`
- `scripts/export_h2_bundle_lock_audit.py`
- `scripts/export_p10_submission_archive_ready.py`

## Expected Outcome

Selected outcome:

- `release_audit_surfaces_refreshed_to_h43`

Machine-readable consequences:

- `active_scientific_stage = h43_post_r44_useful_case_refreeze`
- `refresh_packet = p29_post_h43_release_audit_refresh`
- `current_completed_exact_runtime_gate = r43_origin_bounded_memory_small_vm_execution_gate`
- `current_completed_useful_case_gate = r44_origin_restricted_wasm_useful_case_execution_gate`
- `current_completed_coequal_model_gate = r45_origin_dual_mode_model_mainline_gate`
- `completed_publication_sync_packet = p28_post_h43_publication_surface_sync`
- `merge_executed = false`
- `next_required_lane = no_active_downstream_runtime_lane`

## Non-Goals

- no new runtime lane after `H43`;
- no merge to `main`;
- no widened scientific claims or manuscript claim lift;
- no reinterpretation of model evidence as a substitute for exact evidence;
- no historical rewrite of the earlier same-endpoint `D0` packet chain.
