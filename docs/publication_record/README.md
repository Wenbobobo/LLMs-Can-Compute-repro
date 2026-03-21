# Publication Record

This directory is the paper-first evidence ledger for the repository. Formal
paper text is still evolving, but claim wording, figure/table ownership,
bundle boundaries, and public-safe evidence mapping should be treated as active
rather than speculative.

Current control docs:
- `current_stage_driver.md` — the canonical `active_driver` for the current
  `H21` frozen same-endpoint state, with the completed `H20/R22/R23`
  follow-up packet preserved underneath it, `H19` preserved as the immediate
  pre-refreeze control, `H17` preserved as the prior same-scope refreeze,
  `H15` preserved as the prior refreeze-and-decision-sync stage,
  `H10/H11/R8/R9/R10/H12` preserved as the latest earlier same-endpoint
  follow-up packet, `H13/V1` preserved as the governance/runtime handoff, and
  future frontier work left conditional on a new explicit plan;
- `docs/plans/2026-03-21-post-r22-r23-h21-mainline-design.md` — the current
  execution plan for conservative post-`H21` closeout, with `P12` now the
  immediate next-priority lane, `P13` kept downstream-only, and `F2` still
  planning-only;
- `results/H21_refreeze_after_r22_r23/summary.json` — machine-readable
  refreeze for the post-`R22/R23` same-endpoint packet, including the current
  `supported_here` / `unsupported_here` / `disconfirmed_here` partition and
  the downstream `P12` handoff;
- `results/H20_post_h19_mainline_reentry_and_hygiene_split/summary.json` —
  machine-readable reentry guard for the `H19 -> R22/R23/H21` handoff;
- `results/H18_post_h17_mainline_reopen_guard/summary.json` — machine-readable
  planning guard confirming that the post-`H17` same-scope reopen is ready
  without changing the frozen-evidence state;
- `results/R19_d0_pointer_like_surface_generalization_gate/summary.json` — the
  landed `R19` runtime gate, carrying the admitted-plus-heldout
  exactness/runtime verdict for the first same-endpoint generalization batch;
- `results/R20_d0_runtime_mechanism_ablation_matrix/summary.json` — the
  landed `R20` mechanism lane, showing that the fixed same-endpoint
  pointer-like path stayed exact while the bounded negative controls failed;
- `results/R21_d0_exact_executor_boundary_break_map/summary.json` — the
  landed `R21` boundary scan, showing that the bounded executor grid stayed
  exact on every executed candidate and did not yet localize a failure inside
  that scan;
- `H18` / `R19` / `R20` / `R21` / `H19` now define the preserved
  pre-`R22/R23` same-endpoint reopen/refreeze packet, `H20` / `R22` / `R23` /
  `H21` define the current follow-up packet, `H17` is the preserved prior
  same-scope refreeze, `H15` is the completed predecessor refreeze stage, and
  `H14` / `R11` / `R12` remain the completed prior reopen packet;
- `planning_state_taxonomy.md` — allowed planning-state labels and current
  assignments for active drivers, standing gates, dormant protocols, and
  historical-complete references;
- `paper_package_plan.md` — completed post-`P7` stage design retained as a
  `historical_complete` reference;
- `release_candidate_checklist.md` — restrained outward-sync
  `standing_gate` for the locked checkpoint;
- `conditional_reopen_protocol.md` — bounded reopen protocol still governing
  the current bounded `D0` packet; `E1c` remains conditional only.

Completed baselines:
- `H14` / `R11` / `R12` / `H15` remain the completed bounded core-first
  reopen/refreeze packet on the same endpoint; `R11` keeps geometry parity
  exact while blocking same-endpoint speedup wording, `R12` keeps current
  executor exports exact while making the harder-slice inventory explicit, and
  `H15` leaves `R13` inactive plus `R14` unjustified on current evidence;
- `R15` remains the first landed same-scope lane under `H16`; it complements
  rather than replaces `R8` by covering the four `R6` families that were still
  missing retrieval-pressure evidence;
- `R16` remains the second landed same-scope lane under `H16`; it saturates
  the admitted `R8/R15` memory-surface precision follow-up without widening
  endpoint scope and hands the current packet forward to `R17`;
- `R17` remains the third landed same-scope lane under `H16`; it closes the
  full admitted runtime surface with a negative bridge result, keeps `0`
  contradiction candidates, and names one bounded `R18` target on
  `helper_checkpoint_braid_long/retrieval_total`;
- `R18` now remains the completed comparator-only runtime repair packet under
  `H16`; `R18a` failed its narrow decomp-first gate, but `R18b` closed the
  same-surface packet with exact focused probes and exact `8/8` confirmation,
  so `R18c` was not needed;
- `H8` / `R6` / `R7` / `H9` remain the completed bounded long-horizon direct
  baseline on the same endpoint; `R7` preserves the full admitted family set
  but only profiles the top `4` heaviest representatives in its bounded
  runtime stop result;
- `H6` / `R3` / `R4` / inactive `R5` / `H7` remain the completed bounded
  exactness/mechanism baseline underneath the current packet;
- `H4` / `E1a` / `E1b` / `H5` remain the completed bounded return packet that
  sharpened precision and same-scope systems wording without widening scope;
- `H3` / `P10` / `P11` / `F1` remain the completed control baseline that made
  the locked checkpoint auditable and handoff-safe before the active return
  packets resumed reproduction work.

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
  routing reference for historical `E1a/E1b` patch work and any future
  bounded reopen;
- `e1a_precision_patch_playbook.md` — completed bounded-precision protocol for
  the historical `E1a` lane;
- `e1b_systems_patch_playbook.md` — completed bounded-systems protocol for the
  historical `E1b` lane;
- `e1c_compiled_boundary_patch_playbook.md` — still-dormant compiled-boundary
  protocol, used only if the current bounded `D0` packet exposes a `D0`
  contradiction.

Supporting references:
- `release_preflight_checklist.md` — outward release checklist for README /
  STATUS / release summary and paper-facing ledgers; now paired with the
  machine-readable `release_preflight_checklist_audit` export;
- `results/release_worktree_hygiene_snapshot/summary.json` — operational
  repo-cleanliness snapshot used to decide whether an outward sync commit is
  currently blocked by a dirty worktree;
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
- the next operational wave may be planned in detail before it lands, but
  planned work must stay clearly separated from frozen evidence;
- future short public-surface syncs should derive from
  `release_summary_draft.md`, while the manuscript bundle remains the
  authoritative paper-facing source;
- planning guards such as `H18` and `H20` may guide unattended execution
  before new runtime evidence lands, but once runtime exports such as `R19`,
  `R20`, `R21`, `R22`, and `R23` exist they must be recorded explicitly and
  then frozen by a later closeout such as `H19` or `H21` before outward
  wording moves downstream;
- derivative writing aids remain downstream-only and must not outrun the locked
  manuscript bundle;
- appendix-level diagnostics that strengthen an existing claim row without
  widening scope should stay tied to that claim and the `P1` paper bundle,
  rather than becoming a new claim layer by default;
- the current frozen state preserves `H8/R6/R7/H9` as the completed direct baseline,
  preserves `H6/R3/R4/(inactive R5)/H7` as the deeper historical baseline,
  preserves `H10/H11/R8/R9/R10/H12` as the latest earlier same-endpoint
  follow-up packet, preserves `H13/V1` as the completed governance/runtime
  handoff, preserves `H14/R11/R12/H15` as the completed reopen/refreeze
  packet, preserves `H16/R15/R16/R17/R18/H17` as the completed prior
  same-scope reopen/refreeze packet, preserves `H18/R19/R20/R21/H19` as the
  completed immediate pre-refreeze mainline packet, keeps `H21` as the current
  frozen same-endpoint state, keeps `H19` as the preserved prior same-endpoint
  refreeze decision, keeps `H17` as the preserved prior same-scope
  refreeze decision, keeps `H15` as the preserved prior refreeze decision,
  uses the bounded timing follow-up as the current operational reference for
  full-suite runtime behavior, and leaves `E1c` dormant unless a completed
  packet or later explicit review exposes a true `D0` contradiction;
- short-form alignment for guards: `H21` is the current frozen driver state,
  `H20` remains the completed reentry-and-hygiene split guard,
  `H19` remains the preserved prior same-endpoint refreeze stage,
  `H18` remains the completed same-endpoint reopen-and-scope-lock packet,
  `H17` remains the preserved prior same-scope refreeze stage,
  `H16` remains the completed earlier same-scope reopen-and-scope-lock packet,
  `R19` remains the landed admitted-plus-heldout runtime generalization lane,
  `R20` remains the landed mechanism lane, `R21` remains the landed bounded
  executor-boundary lane, `R22` remains the landed harder boundary follow-up,
  `R23` remains the landed same-endpoint systems follow-up, `R18` remains the completed comparator-only repair
  closeout, `H14` / `R11` / `R12` remain the completed prior reopen packet,
  `H13` / `V1` remain the completed governance/runtime handoff,
  `H10` / `H11` / `R8` / `R9` / `R10` / `H12` remain the latest older
  same-endpoint packet, and `H8` / `R6` / `R7` / `H9` remain the completed
  bounded long-horizon direct baseline;
- `blog_outline.md` remains downstream and currently blocked: `M7` resolved as
  a no-widening decision, so broader blog prose should not outrun the present
  paper-grade endpoint.
