# Release Preflight Checklist

This checklist defines the minimum outward-facing sync required after the
current freeze candidate is assembled.

## Wording and scope

- [ ] `README.md` stays a restrained landing page and keeps the current narrow
  non-goals explicit.
- [ ] `STATUS.md` reflects the current active `H32` routing/refreeze packet,
  the current docs-only `H34` control packet above it, preserves `H33` as the
  prior question-selection step plus `R39` as completed downstream evidence,
  preserves `H31/H30` as upstream decision packets plus `H29` as the upstream
  refreeze and `H27/H28` as the preserved closeout/pivot packet pair, and
  keeps later compiler-boundary extension / `R29` / `F3` execution conditional
  or blocked as appropriate with no active downstream runtime lane.
- [ ] `release_summary_draft.md` remains the source for short public-surface
  wording downstream of landed `H34/H32/R39/H33/H31/H30` while preserving the
  narrow Origin-core limits.
- [ ] `P20_post_h34_manuscript_narrative_resync`,
  `F5_post_h34_contradiction_scout_matrix`, and
  `F6_post_p20_future_option_matrix` remain aligned with the same no-reopen
  interpretation and do not imply a new runtime lane.
- [ ] `F7_post_h34_reopen_trigger_specification_bundle`,
  `F8_post_h34_beyond_origin_bridge_roadmap`,
  `F10_post_h34_executor_value_comparator_matrix`,
  `F12_post_f10_origin_claim_delta_reanchor_bundle`,
  `F13_post_f12_bounded_scalar_value_family_spec`,
  `F14_post_f13_conditional_reopen_readiness_bundle`, and
  `P23_post_f13_planning_surface_sync` remain aligned with that same
  planning-only no-reopen interpretation, while `P21/P22` stay preserved
  prior syncs, `F9` stays blocked, `F11` stays new-substrate, and none of
  them imply `H35`, `R40`, or a broadened runtime family.

## Paper-facing ledgers

- [ ] `manuscript_bundle_draft.md` still matches the fixed section and artifact
  ownership on current scope.
- [ ] `paper_bundle_status.md`, `layout_decision_log.md`,
  `freeze_candidate_criteria.md`, `main_text_order.md`, and
  `appendix_companion_scope.md` remain synchronized.
- [ ] `publication_record/README.md` and `plans/README.md` both expose the
  completed `P20/F5/F6` closeout plus the preserved `F7/F8/P21` wave and the
  preserved `F10/P22` bridge wave plus the current `F12/F13/F14/P23`
  family-first planning wave without widening wording.
- [ ] `blog_release_rules.md` still records the blocked-blog state explicitly.

## Machine-audited guards

- [ ] `results/P1_paper_readiness/summary.json` still reports `10/10` ready
  figure/table items on the frozen scope.
- [ ] `results/H32_post_r38_compiled_boundary_refreeze/summary.json`
  reports zero blocked items on the current active routing/refreeze packet.
- [ ] `results/H34_post_r39_later_explicit_scope_decision_packet/summary.json`
  reports the current docs-only freeze-complete-for-now control packet and no
  active downstream runtime lane.
- [ ] `results/R39_origin_compiler_control_surface_dependency_audit/summary.json`
  remains available as the completed same-substrate dependency audit on one
  declared helper-body permutation with target renumbering.
- [ ] `results/H33_post_h32_conditional_next_question_packet/summary.json`
  remains available as the preserved prior docs-only question-selection packet.
- [ ] `results/R38_origin_compiler_control_surface_extension_gate/summary.json`
  remains available as the current richer same-substrate compiled control gate.
- [ ] `results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json`
  remains available as the preserved explicit later-decision packet.
- [ ] `results/H30_post_r36_r37_scope_decision_packet/summary.json`
  remains available as the preserved prior compiled-boundary refreeze packet.
- [ ] `results/R37_origin_compiler_boundary_gate/summary.json` remains
  available as the preserved tiny compiled-boundary gate.
- [ ] `results/H29_refreeze_after_r34_r35_origin_core_gate/summary.json`
  remains available as the preserved upstream refreeze packet.
- [ ] `results/H28_post_h27_origin_core_reanchor_packet/summary.json` remains
  available as the current Origin-core pivot packet.
- [ ] `results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`
  remains available as the preserved negative same-endpoint closeout packet.
- [ ] `results/R34_origin_retrieval_primitive_contract_gate/summary.json`
  remains available as the current primitive-contract gate.
- [ ] `results/R35_origin_append_only_stack_vm_execution_gate/summary.json`
  remains available as the current exact execution gate.
- [ ] `results/R36_origin_long_horizon_precision_scaling_gate/summary.json`
  remains available as the current narrow precision-boundary follow-up.
- [ ] `results/H17_refreeze_and_conditional_frontier_recheck/summary.json`
  still reports zero blocked items on the preserved prior same-scope refreeze
  surface.
- [ ] `results/H15_refreeze_and_decision_sync/summary.json` reports zero
  blocked items on the preserved prior refrozen control surface.
- [ ] `results/H14_core_first_reopen_guard/summary.json` reports zero blocked
  items on the preserved core-first reopen control surface.
- [ ] `results/H13_post_h12_governance_stage_health/summary.json` reports zero
  blocked items on the preserved governance/runtime handoff.
- [ ] `results/P5_public_surface_sync/summary.json` reports zero blocked items.
- [ ] `results/P5_callout_alignment/summary.json` reports zero blocked rows.
- [ ] `results/H2_bundle_lock_audit/summary.json` reports zero blocked items.
- [ ] `results/release_worktree_hygiene_snapshot/summary.json` classifies the
  current release-commit readiness and reports no diff-check content issues.
- [ ] `results/V1_full_suite_validation_runtime_timing_followup/summary.json`
  reports `healthy_but_slow` with zero timed-out files.

## Release hygiene

- [ ] Use `results/release_worktree_hygiene_snapshot/summary.json` to decide
  whether an outward sync commit is currently blocked by a dirty tree.
- [ ] No local-only source material under `docs/Origin/` or `docs/origin/`
  enters the public surface.
- [ ] Blog work remains blocked unless `blog_release_rules.md` is satisfied in
  full.
