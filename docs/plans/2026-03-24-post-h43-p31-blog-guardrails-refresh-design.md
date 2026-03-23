# 2026-03-24 Post-H43 P31 Blog Guardrails Refresh Design

## Objective

Keep the scientific stage fixed at
`H43_post_r44_useful_case_refreeze` while refreshing the remaining blocked-
blog and helper guardrail surfaces that still describe the preserved
`H32/H34` compiled-boundary line as the current paper-grade endpoint. The
design goal is narrow:

- keep `H43` as the current active docs-only scientific packet;
- keep `H36` as the preserved routing/refreeze packet underneath the stack;
- keep completed `P30` as the prior manuscript-surface refresh packet and
  completed `P29` as the prior release/public audit refresh packet;
- refresh blocked downstream blog/helper docs so they stop implying that the
  current paper-grade endpoint still terminates at `H34`;
- refresh manuscript, caption, reviewer, and appendix helper docs that still
  treat the preserved first `D0` compiled step as the whole current endpoint;
- refresh current-wave status and index/handoff surfaces so they record `P31`
  explicitly as the new low-priority operational wave;
- keep the preserved first `D0` compiled boundary as historical support only,
  not the whole current endpoint; and
- leave `next_required_lane = no_active_downstream_runtime_lane`.

## Options

### Recommended: `P31_post_h43_blog_guardrails_refresh`

Land one low-priority operational blocked-blog/helper guardrail refresh packet
downstream of completed `P30`. This keeps the scientific/control split
explicit: `H43` remains the current scientific stage, while `P31` records that
blocked downstream blog helpers now align to the landed
`H36/H40/R42/F20/H41/P27/R43/R45/H42/R44/H43` chain.

### Rejected: leave stale blocked-blog wording in place

The blog remains blocked either way, but leaving helper docs frozen at the
preserved `H34` line creates unnecessary current-state drift for later agents
and any future release audit.

### Rejected: broader public blog release

This packet must not unblock the blog, rewrite public framing broadly, or turn
blocked helper surfaces into an outward release lane.

## Packet Shape

`P31` should export:

- `summary.json`
- `checklist.json`
- `snapshot.json`

The packet should refresh only the minimum blocked-blog/helper operational
surfaces that still lag the landed `H43` stack:

- `STATUS.md`
- `docs/publication_record/blog_outline.md`
- `docs/publication_record/blog_release_rules.md`
- `docs/publication_record/manuscript_stub_notes.md`
- `docs/publication_record/section_caption_notes.md`
- `docs/publication_record/caption_candidate_notes.md`
- `docs/publication_record/figure_table_narrative_roles.md`
- `docs/publication_record/manuscript_section_map.md`
- `docs/publication_record/appendix_boundary_map.md`
- `docs/publication_record/appendix_stub_notes.md`
- `docs/publication_record/appendix_companion_scope.md`
- `docs/publication_record/freeze_candidate_criteria.md`
- `docs/publication_record/reviewer_boundary_note.md`
- `docs/publication_record/claim_evidence_table.md`
- `docs/publication_record/release_summary_draft.md`
- `docs/publication_record/README.md`
- `docs/publication_record/experiment_manifest.md`
- `docs/plans/README.md`
- `docs/milestones/README.md`
- `tmp/active_wave_plan.md`

## Expected Outcome

Selected outcome:

- `blocked_blog_guardrails_refreshed_to_h43`

Machine-readable consequences:

- `active_scientific_stage = h43_post_r44_useful_case_refreeze`
- `refresh_packet = p31_post_h43_blog_guardrails_refresh`
- `current_blog_endpoint = h43_current_paper_grade_endpoint`
- `completed_prior_manuscript_refresh_packet = p30_post_h43_manuscript_surface_refresh`
- `completed_prior_release_audit_refresh_packet = p29_post_h43_release_audit_refresh`
- `preserved_compiled_boundary_line = h32_h34_compiled_boundary_historical_support_only`
- `blog_release_state = blocked_pending_explicit_later_packet`
- `merge_executed = false`
- `next_required_lane = no_active_downstream_runtime_lane`

## Non-Goals

- no new runtime lane after `H43`;
- no merge to `main`;
- no unblocking of the blog itself;
- no broader public-claim widening;
- no reinterpretation of coequal `R45` model evidence as a substitute for
  exact `R43`;
- no rewrite of the frozen manuscript bundle beyond the minimum helper-doc
  honesty needed here; and
- no historical rewrite of earlier post-`H34` packets beyond current-state
  correction in still-active helper docs.
