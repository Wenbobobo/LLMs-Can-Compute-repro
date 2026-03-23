# 2026-03-24 Post-H43 P34 Live-Surface Wording Guardrail Design

## Objective

Keep the scientific stage fixed at
`H43_post_r44_useful_case_refreeze` while converting the recent post-`H43`
wording cleanup into a machine-checkable guardrail on current live/control
surfaces. The design goal is narrow:

- keep `H43` as the current active docs-only scientific packet;
- keep `P31` as the current low-priority operational/docs wave;
- keep `P32` and `P33` as completed auxiliary wording sidecars;
- treat `P34` as a completed auxiliary follow-on packet only;
- add one machine-readable guardrail that audits the current live helper/control
  surfaces for stale “current compiled endpoint/boundary” drift on preserved
  same-endpoint `D0` support;
- keep historical plans, results, and drift-description rows out of the lint
  scope unless they are the current live surface;
- refresh minimal status, plan, milestone, publication, and active-wave
  handoff surfaces so they record `P34` without displacing `P31`;
- leave `next_required_lane = no_active_downstream_runtime_lane`; and
- avoid reopening any runtime, dormant `E1`, or claim-widening lane.

## Options

### Recommended: `P34_post_h43_live_surface_wording_guardrail`

Land one narrow auxiliary operational/docs packet downstream of completed
`P31/P32/P33`. This keeps the current-wave story stable while adding a simple
guardrail exporter/test that future unattended runs can rerun mechanically.
The guard scans current live helper/control surfaces only and blocks the main
positive stale phrases that previously implied preserved `D0` scope was still
the whole current endpoint.

### Rejected: keep relying on ad hoc manual wording sweeps

That would preserve the current surfaces today but leave the repo exposed to
future drift as more auxiliary packets and helper-doc edits accumulate.

### Rejected: broaden the guardrail to all historical plans and results

Historical packets legitimately describe older current-at-the-time states or
explain what drift a later packet corrected. Linting them as though they were
current live control surfaces would create noise and encourage low-value
historical rewrites.

## Packet Shape

`P34` should export:

- `summary.json`
- `checklist.json`
- `snapshot.json`

The packet should add only the minimum guardrail surfaces:

- `scripts/export_p34_post_h43_live_surface_wording_guardrail.py`
- `tests/test_export_p34_post_h43_live_surface_wording_guardrail.py`
- `results/P34_post_h43_live_surface_wording_guardrail/*`
- minimal status/index/handoff updates:
  - `STATUS.md`
  - `docs/publication_record/README.md`
  - `docs/publication_record/experiment_manifest.md`
  - `docs/plans/README.md`
  - `docs/milestones/README.md`
  - `tmp/active_wave_plan.md`

The guarded current live surfaces should include:

- `docs/publication_record/current_stage_driver.md`
- blocked-blog/helper prose surfaces refreshed by `P31`
- current release-summary/helper surfaces that later agents are likely to reuse

## Expected Outcome

Selected outcome:

- `live_surface_wording_guardrail_landed`

Machine-readable consequences:

- `active_scientific_stage = h43_post_r44_useful_case_refreeze`
- `current_low_priority_wave = p31_post_h43_blog_guardrails_refresh`
- `refresh_packet = p34_post_h43_live_surface_wording_guardrail`
- `refresh_scope = current_live_control_and_helper_wording_guardrails`
- `guarded_surface_rule = preserved_d0_support_not_whole_current_endpoint`
- `merge_executed = false`
- `next_required_lane = no_active_downstream_runtime_lane`

## Non-Goals

- no new runtime lane after `H43`;
- no activation of dormant `E1` playbooks;
- no merge to `main`;
- no displacement of `P31` as the current low-priority wave;
- no broad historical rewrite of preserved plans/results; and
- no reinterpretation of preserved same-endpoint `D0/R2` packets as current
  scientific state.
