# 2026-03-24 Post-H43 P28 Publication Surface Sync Design

## Objective

Keep the scientific stage fixed at
`H43_post_r44_useful_case_refreeze` while bringing the paper-facing
publication ledgers up to the landed `H43/R44/R45/R43/P27` state. The design
goal is narrow:

- keep `H43` as the current active docs-only decision packet;
- keep `H36` as the preserved routing/refreeze packet underneath the stack;
- record `R43`, `R44`, and `R45` as completed current gates in the
  publication-facing ledgers;
- preserve `P27` as the explicit merge packet with `merge_executed = false`;
- sync review/release/submission helpers so they stop describing `R43/R44` as
  deferred; and
- leave `next_required_lane = no_active_downstream_runtime_lane`.

## Options

### Recommended: `P28_post_h43_publication_surface_sync`

Land one low-priority operational publication-sync packet downstream of the
already completed `H43` scientific state. This keeps the scientific/control
separation explicit: `H43` remains the current stage driver, while `P28`
records that the publication-facing ledgers caught up to the landed evidence.

### Rejected: ad hoc prose edits only

This would fix wording drift locally, but it would not give future unattended
work a machine-readable record of which publication surfaces have been synced
to `H43`.

### Rejected: merge review now

`P27` already records explicit merge posture and still leaves
`merge_executed = false`. A merge-review wave is a separate operational
decision and should not be mixed with publication-surface cleanup.

## Packet Shape

`P28` should export:

- `summary.json`
- `checklist.json`
- `surface_snapshot.json`

The packet should refresh only the minimum downstream publication/control
surfaces that still lag the landed `H43` stack:

- `docs/publication_record/README.md`
- `docs/publication_record/claim_evidence_table.md`
- `docs/publication_record/paper_bundle_status.md`
- `docs/publication_record/release_preflight_checklist.md`
- `docs/publication_record/release_summary_draft.md`
- `docs/publication_record/review_boundary_summary.md`
- `docs/publication_record/submission_packet_index.md`
- `docs/publication_record/experiment_manifest.md`
- `docs/plans/README.md`
- `docs/milestones/README.md`
- `tmp/active_wave_plan.md`

## Expected Outcome

Selected outcome:

- `publication_surfaces_synced_to_h43`

Machine-readable consequences:

- `active_scientific_stage = h43_post_r44_useful_case_refreeze`
- `sync_packet = p28_post_h43_publication_surface_sync`
- `current_completed_exact_runtime_gate = r43_origin_bounded_memory_small_vm_execution_gate`
- `current_completed_useful_case_gate = r44_origin_restricted_wasm_useful_case_execution_gate`
- `current_completed_coequal_model_gate = r45_origin_dual_mode_model_mainline_gate`
- `merge_executed = false`
- `next_required_lane = no_active_downstream_runtime_lane`

## Non-Goals

- no new runtime lane after `H43`;
- no merge to `main`;
- no widened scientific claims or manuscript claim lift;
- no reinterpretation of model evidence as a substitute for exact evidence;
- no historical rewrite of the earlier same-endpoint `D0` packet chain.
