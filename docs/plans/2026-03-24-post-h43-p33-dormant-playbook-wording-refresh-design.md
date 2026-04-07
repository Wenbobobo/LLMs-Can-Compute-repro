# 2026-03-24 Post-H43 P33 Dormant Playbook Wording Refresh Design

## Objective

Keep the scientific stage fixed at
`H43_post_r44_useful_case_refreeze` while refreshing the remaining dormant
playbook and historical-helper wording surfaces that still describe preserved
same-endpoint `R2` or the preserved first compiled `D0` boundary as if they
were still the whole current paper endpoint. The design goal is narrow:

- keep `H43` as the current active docs-only scientific packet;
- keep `P31` as the current low-priority operational/docs wave;
- keep `P32` as a completed auxiliary historical/regeneration sidecar;
- treat `P33` as a completed auxiliary follow-on packet only;
- refresh dormant `E1` playbooks, helper layout notes, and selected
  historical manifest rows so preserved same-endpoint `R2/D0` surfaces are
  named honestly relative to the broader current `H43` paper endpoint;
- refresh minimal status, plan, milestone, publication, and active-wave
  handoff surfaces so they record `P33` without displacing `P31`;
- leave `next_required_lane = no_active_downstream_runtime_lane`; and
- avoid reopening any runtime, patch-playbook activation, or claim-widening
  lane.

## Options

### Recommended: `P33_post_h43_dormant_playbook_wording_refresh`

Land one narrow auxiliary operational/docs packet downstream of completed
`P31` and `P32`. This keeps the current-wave story stable: `P31` remains the
current low-priority wave, `P32` remains the earlier completed auxiliary
historical/regeneration packet, and `P33` only refreshes dormant playbooks and
historical helper wording that still speak as though preserved same-endpoint
`R2/D0` scope were the live paper endpoint.

### Rejected: promote `P33` to the current low-priority wave

That would create unnecessary churn across the existing `P28/P29/P30/P31/P32`
control story even though the actual change set is narrow and wording-only.

### Rejected: reopen dormant `E1` execution or broader historical rewrite

`P33` must not activate `E1a/E1b/E1c`, rerun any old same-endpoint science, or
rewrite broad historical plan stacks. It only corrects still-live helper and
dormant-playbook wording so those docs no longer imply that preserved
same-endpoint `D0/R2` scope is still the whole current endpoint.

## Packet Shape

`P33` should export:

- `summary.json`
- `checklist.json`
- `snapshot.json`

The packet should refresh only the minimum dormant/helper surfaces that still
lag the landed `H43/P31/P32` stack:

- `docs/publication_record/e1_patch_playbook_matrix.md`
- `docs/publication_record/e1b_systems_patch_playbook.md`
- `docs/publication_record/e1c_compiled_boundary_patch_playbook.md`
- `docs/publication_record/layout_decision_log.md`
- selected historical rows in `docs/publication_record/experiment_manifest.md`
- `STATUS.md`
- `docs/publication_record/README.md`
- `docs/plans/README.md`
- `docs/milestones/README.md`
- `tmp/active_wave_plan.md`
- focused tests covering the refreshed wording

## Expected Outcome

Selected outcome:

- `dormant_playbook_wording_surfaces_refreshed_to_h43`

Machine-readable consequences:

- `active_scientific_stage = h43_post_r44_useful_case_refreeze`
- `current_low_priority_wave = p31_post_h43_blog_guardrails_refresh`
- `refresh_packet = p33_post_h43_dormant_playbook_wording_refresh`
- `refresh_scope = dormant_playbook_and_historical_helper_wording_surfaces`
- `preserved_compiled_boundary_line = d0_first_compiled_step_historical_support_only`
- `merge_executed = false`
- `next_required_lane = no_active_downstream_runtime_lane`

## Non-Goals

- no new runtime lane after `H43`;
- no activation of dormant `E1` playbooks;
- no merge to `main`;
- no displacement of `P31` as the current low-priority wave;
- no reinterpretation of old same-endpoint `D0/R2` packets as current
  scientific state; and
- no broad historical rewrite beyond the narrow current-state honesty captured
  here.
