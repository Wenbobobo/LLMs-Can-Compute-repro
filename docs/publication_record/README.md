# Publication Record

This directory is now the paper-first evidence ledger for the repository.
Formal paper text is still evolving, but claim wording, figure/table ownership,
and public-safe evidence mapping should be treated as active rather than
speculative.

Core ledgers:
- `claim_ladder.md` — which claims are validated, partial, negative, or still
  open;
- `claim_evidence_table.md` — concrete artifacts already supporting published
  claims;
- `manuscript_section_map.md` — current section-to-artifact ownership for the
  paper lane;
- `section_caption_notes.md` — caption-ready section notes and phrasing
  guardrails for the current manuscript skeleton;
- `manuscript_stub_notes.md` — near-prose section stubs for the most
  boundary-sensitive parts of the draft;
- `manuscript_bundle_draft.md` — current layout-disciplined manuscript
  baseline for freeze-candidate work and release preflight;
- `freeze_candidate_criteria.md` — explicit pass/fail standard for calling the
  current manuscript bundle a freeze candidate;
- `main_text_order.md` — fixed main-text figure/table sequence for the frozen
  scope;
- `appendix_companion_scope.md` — required versus optional appendix companions
  on the same frozen scope;
- `appendix_stub_notes.md` — near-prose appendix and reproducibility draft
  material;
- `caption_candidate_notes.md` — draft caption sentences for the fixed current
  main-text figures and tables;
- `release_summary_outline.md` — short downstream summary outline for future
  release-facing syncs;
- `release_summary_draft.md` — short release-facing draft derived from the
  manuscript bundle and approved as the source for future README-adjacent short
  updates;
- `release_preflight_checklist.md` — outward release checklist for README /
  STATUS / release summary and paper-facing ledgers;
- `blog_release_rules.md` — explicit downstream preconditions before any future
  blog derivative is allowed to move;
- `section_draft_upgrade_outline.md` — record of the structural pass that
  converted the bundle into a more paper-shaped section draft;
- `figure_table_narrative_roles.md` — fixed argumentative role for each current
  main-text figure and table;
- `appendix_boundary_map.md` — explicit main-text versus appendix boundary for
  companion artifacts;
- `layout_decision_log.md` — records layout choices that affect evidence
  placement or claim wording;
- `figure_backlog.md` — reserved future figures and tables;
- `experiment_manifest.md` — reproducibility ledger for unattended runs;
- `threats_to_validity.md` — constraints, caveats, and external-threat notes;
- `negative_results.md` — results that narrow or block claims;
- `paper_outline.md` and `blog_outline.md` — downstream writing structure once
  the evidence stabilizes.

Operating rule:
- every unattended batch that changes a claim boundary, a milestone gate, or a
  future figure/table dependency must update these ledgers in the same batch.
- appendix-level diagnostics that strengthen an existing claim row without
  widening scope should stay tied to that claim and the `P1` paper bundle,
  rather than becoming a new claim layer by default.
- future short public-surface syncs should derive from
  `release_summary_draft.md`, while the manuscript bundle remains the
  authoritative paper-facing source.
- `paper_outline.md` is active planning material for the current paper-first
  workflow.
- `blog_outline.md` remains downstream and currently blocked: `M7` resolved as
  a no-widening decision, so broader blog prose should not outrun the present
  paper-grade endpoint.
