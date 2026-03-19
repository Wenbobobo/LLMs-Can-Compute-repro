# Publication Record

This directory is the paper-first evidence ledger for the repository. Formal
paper text is still evolving, but claim wording, figure/table ownership,
bundle boundaries, and public-safe evidence mapping should be treated as active
rather than speculative.

Current control docs:
- `current_stage_driver.md` — the canonical `active_driver` for the current
  current bounded reproduction-return packet in the `H4` / `E1a` / `E1b` /
  `H5` stage;
- `planning_state_taxonomy.md` — allowed planning-state labels and current
  assignments for active drivers, standing gates, dormant protocols, and
  historical-complete references;
- `paper_package_plan.md` — completed post-`P7` stage design retained as a
  `historical_complete` reference;
- `release_candidate_checklist.md` — restrained outward-sync
  `standing_gate` for the locked checkpoint;
- `conditional_reopen_protocol.md` — bounded reopen protocol still governing
  the current scientific-return stage; `E1c` remains conditional only.

Completed baseline:
- `H3` / `P10` / `P11` / `F1` remain the completed baseline that made the
  locked checkpoint auditable and handoff-safe before the active return packet
  resumed reproduction work.

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
  baseline for the locked submission-candidate bundle;
- `freeze_candidate_criteria.md` — explicit pass/fail standard for calling the
  manuscript bundle a freeze candidate;
- `submission_candidate_criteria.md` — explicit bundle-lock standard on the
  same frozen scope;
- `main_text_order.md` — fixed main-text figure/table sequence for the frozen
  scope;
- `appendix_companion_scope.md` — required versus optional appendix companions
  on the same frozen scope;
- `appendix_stub_notes.md` — near-prose appendix and reproducibility draft
  material;
- `caption_candidate_notes.md` — draft caption sentences for the fixed current
  main-text figures and tables;
- `paper_bundle_status.md` — current figure/table and bundle-readiness ledger;
- `submission_packet_index.md` — venue-agnostic packet index for current
  manuscript, appendix, ledgers, and audit anchors;
- `archival_repro_manifest.md` — regeneration, environment, and archive-safety
  manifest for the locked checkpoint;
- `review_boundary_summary.md` — packet-level summary of supported claims,
  blocked claims, and reopen routing;
- `external_release_note_skeleton.md` — downstream-only restrained release-note
  skeleton derived from the locked checkpoint;
- `release_summary_outline.md` — short downstream summary outline for future
  release-facing syncs;
- `release_summary_draft.md` — short release-facing draft approved as the
  source for future README-adjacent short updates.

Derivative-only aids:
- `abstract_contribution_pack.md` — venue-agnostic abstract and contribution
  language derived from the locked manuscript bundle;
- `derivative_material_pack.md` — downstream-only notes on what survived, what
  stayed blocked, and which artifact pairs matter most for future derivatives;
- `reviewer_boundary_note.md` — concise reviewer-facing note on current claims,
  non-claims, and reopen routing.

Patch-playbook references:
- `e1_patch_playbook_matrix.md` — lane-selection matrix retained as the
  routing reference for the current bounded patch stage;
- `e1a_precision_patch_playbook.md` — active bounded-precision protocol for the
  current `E1a` lane;
- `e1b_systems_patch_playbook.md` — active bounded-systems protocol for the
  current `E1b` lane;
- `e1c_compiled_boundary_patch_playbook.md` — still-dormant compiled-boundary
  protocol, used only if the current return stage exposes a `D0`
  contradiction.

Supporting references:
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
  future figure/table dependency must update these ledgers in the same batch;
- exactly one document set should act as the current `active_driver`, and that
  role currently belongs to `current_stage_driver.md`;
- future short public-surface syncs should derive from
  `release_summary_draft.md`, while the manuscript bundle remains the
  authoritative paper-facing source;
- derivative writing aids such as `abstract_contribution_pack.md`,
  `derivative_material_pack.md`, `reviewer_boundary_note.md`, and
  `external_release_note_skeleton.md` remain downstream-only and must not
  outrun the locked manuscript bundle;
- appendix-level diagnostics that strengthen an existing claim row without
  widening scope should stay tied to that claim and the `P1` paper bundle,
  rather than becoming a new claim layer by default;
- the current stage activates only `E1a` and `E1b` on named bounded conflicts;
  `E1c` remains dormant unless the active patches expose a true `D0`
  contradiction;
- `blog_outline.md` remains downstream and currently blocked: `M7` resolved as
  a no-widening decision, so broader blog prose should not outrun the present
  paper-grade endpoint.
