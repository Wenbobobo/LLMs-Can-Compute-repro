# 2026-03-24 Post-H43 P30 Manuscript Surface Refresh Design

## Objective

Keep the scientific stage fixed at
`H43_post_r44_useful_case_refreeze` while refreshing the remaining
manuscript-facing and derivative helper surfaces that still describe the
preserved `H32/H34` compiled-boundary line as the current manuscript endpoint.
The design goal is narrow:

- keep `H43` as the current active docs-only scientific packet;
- keep `H36` as the preserved routing/refreeze packet underneath the stack;
- keep the earlier `H32/H34` compiled-boundary line as preserved historical
  support inside the broader current paper endpoint rather than as the current
  top-level manuscript horizon;
- refresh stale paper-facing prose baselines and derivative helper docs so they
  stop implying that the manuscript still terminates at `H34`;
- refresh the contradictory top-level status block that still presents `H36`
  and `P24` as the current paper-facing operational state;
- record the new low-priority manuscript refresh wave explicitly in milestone,
  plan, publication-record, and handoff indexes; and
- leave `next_required_lane = no_active_downstream_runtime_lane`.

## Options

### Recommended: `P30_post_h43_manuscript_surface_refresh`

Land one low-priority operational manuscript-surface refresh packet downstream
of already completed `P29`. This keeps the scientific/control split explicit:
`H43` remains the current scientific stage, while `P30` records that
manuscript-facing prose baselines and derivative helper docs now align to the
landed `H35/H36/H40/R42/F20/H41/P27/R43/R45/H42/R44/H43` chain.

### Rejected: leave stale manuscript prose in place

The claim/evidence ledgers are authoritative, but leaving stale prose that
still names `H32/H34` as the current manuscript endpoint creates avoidable
drift inside paper-facing helper documents.

### Rejected: full manuscript rewrite

The goal here is bounded control-surface refresh, not a broad paper rewrite.
This packet should fix only the stale endpoint framing and derivative helper
surfaces that obviously lag the landed `H43` state.

## Packet Shape

`P30` should export:

- `summary.json`
- `checklist.json`
- `snapshot.json`

The packet should refresh only the minimum manuscript-facing operational
surfaces that still lag the landed `H43` stack:

- `STATUS.md`
- `docs/publication_record/paper_outline.md`
- `docs/publication_record/manuscript_bundle_draft.md`
- `docs/publication_record/paper_bundle_status.md`
- `docs/publication_record/derivative_material_pack.md`
- `docs/publication_record/abstract_contribution_pack.md`
- `docs/publication_record/external_release_note_skeleton.md`
- `docs/publication_record/release_summary_draft.md`
- `docs/publication_record/README.md`
- `docs/publication_record/experiment_manifest.md`
- `docs/plans/README.md`
- `docs/milestones/README.md`
- `tmp/active_wave_plan.md`

## Expected Outcome

Selected outcome:

- `manuscript_surfaces_refreshed_to_h43`

Machine-readable consequences:

- `active_scientific_stage = h43_post_r44_useful_case_refreeze`
- `refresh_packet = p30_post_h43_manuscript_surface_refresh`
- `current_manuscript_endpoint = h43_origin_core_semantic_boundary_line`
- `preserved_compiled_boundary_line = h32_h34_compiled_boundary_historical_support`
- `completed_publication_sync_packet = p28_post_h43_publication_surface_sync`
- `completed_release_audit_refresh_packet = p29_post_h43_release_audit_refresh`
- `merge_executed = false`
- `next_required_lane = no_active_downstream_runtime_lane`

## Non-Goals

- no new runtime lane after `H43`;
- no merge to `main`;
- no broader manuscript claim lift or public-claim widening;
- no reinterpretation of coequal `R45` model evidence as a substitute for exact
  `R43`;
- no historical rewrite of the earlier `P20` post-`H34` manuscript resync
  packet; and
- no broad paper-layout or figure-order rewrite beyond the minimum endpoint
  realignment needed for control-surface honesty.
