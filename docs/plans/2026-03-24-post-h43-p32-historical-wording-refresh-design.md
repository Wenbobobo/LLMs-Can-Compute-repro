# 2026-03-24 Post-H43 P32 Historical Wording Refresh Design

## Objective

Keep the scientific stage fixed at
`H43_post_r44_useful_case_refreeze` while refreshing the remaining preserved
machine-readable and regeneration-facing surfaces that still describe `D0` as
the whole current paper endpoint. The design goal is narrow:

- keep `H43` as the current active docs-only scientific packet;
- keep `P31` as the current low-priority operational/docs wave;
- treat `P32` as a completed auxiliary follow-on packet only;
- refresh `H0` and `P3` regeneration-facing wording so preserved first-step
  `D0` support is no longer described as the whole current paper endpoint;
- refresh minimal index, status, and handoff surfaces so they record `P32`
  without displacing `P31`;
- leave `next_required_lane = no_active_downstream_runtime_lane`; and
- avoid reopening any runtime or claim-widening lane.

## Options

### Recommended: `P32_post_h43_historical_wording_refresh`

Land one narrow auxiliary operational/docs packet downstream of completed
`P31`. This keeps the current-wave story stable: `P31` remains the active
low-priority refresh wave, while `P32` records that the remaining preserved
`H0/P3` machine-readable regeneration wording now treats `D0` as preserved
first compiled support inside the broader current `H43` paper endpoint.

### Rejected: promote `P32` to the current low-priority wave

That would create unnecessary churn across the existing `P28/P29/P30/P31`
guardrail exporters even though the actual change set is small and
historical/regeneration-only.

### Rejected: reopen broader runtime or historical rewrite lanes

`P32` must not reinterpret historical same-endpoint results, reopen blocked
runtime work, or rewrite preserved plans and manifests beyond the minimum
current-state honesty needed for still-regenerated machine-readable surfaces.

## Packet Shape

`P32` should export:

- `summary.json`
- `checklist.json`
- `snapshot.json`

The packet should refresh only the minimum historical/regeneration surfaces
that still lag the landed `H43/P31` stack:

- `scripts/export_h0_release_hygiene.py`
- `scripts/export_p3_paper_freeze.py`
- regenerated `results/H0_repo_consolidation_and_release_hygiene/public_surface_audit.json`
- regenerated `results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json`
- regenerated `results/P3_paper_freeze_and_evidence_mapping/artifact_map.json`
- focused tests covering the refreshed wording
- `STATUS.md`
- `docs/publication_record/README.md`
- `docs/publication_record/experiment_manifest.md`
- `docs/plans/README.md`
- `docs/milestones/README.md`
- `tmp/active_wave_plan.md`

## Expected Outcome

Selected outcome:

- `historical_wording_regeneration_surfaces_refreshed_to_h43`

Machine-readable consequences:

- `active_scientific_stage = h43_post_r44_useful_case_refreeze`
- `current_low_priority_wave = p31_post_h43_blog_guardrails_refresh`
- `refresh_packet = p32_post_h43_historical_wording_refresh`
- `refresh_scope = historical_regeneration_wording_surfaces`
- `preserved_compiled_boundary_line = d0_first_compiled_step_historical_support_only`
- `merge_executed = false`
- `next_required_lane = no_active_downstream_runtime_lane`

## Non-Goals

- no new runtime lane after `H43`;
- no merge to `main`;
- no displacement of `P31` as the current low-priority wave;
- no broader blog or release unblocking;
- no reinterpretation of old same-endpoint `D0` packets as current scientific
  state; and
- no historical rewrite of preserved plans or manifest rows beyond the narrow
  current-state correction captured here.
