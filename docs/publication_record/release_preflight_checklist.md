# Release Preflight Checklist

This checklist defines the minimum outward-facing sync required after the
current freeze candidate is assembled.

## Wording and scope

- [ ] `README.md` stays a restrained landing page and keeps the current narrow
  non-goals explicit.
- [ ] `STATUS.md` reflects current `H58` as the active docs-only closeout
  packet, preserved prior `H56/H57/H54/H52/H50` as the useful-kernel,
  compiled-boundary, mechanism, and broader-route closeout history,
  preserved `H43` as the paper-grade endpoint, preserved `H42/H41` prior
  docs-only packets, preserved `H36` routing/refreeze packet, completed
  `R42/R43/R44/R45/R58/R59/R60/R61/R62` gate stack, blocked `F27/R53/R54`,
  current `F31/F20/F16/F17/F18/F19` bundles, completed `P40/P27` operational
  posture, preserved `P38/P26/H40/H38/H37/P25` prior support lanes, current
  `F15` derivative bundle, and keeps `merge_executed = false`.
- [ ] `release_summary_draft.md` remains the source for short public-surface
  wording downstream of landed
  `H58/R62/H57/F31/H56/R61/R60/H55/F30/H54/R59/R58/H53/F29/H52/H50/H43/H42/H41/F20/P40/P27/P38/R45/R44/R43/H40/H36/R42`
  while preserving the narrow Origin-core limits and the paper-grade role of
  `H43`.
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
  `P23_post_f13_planning_surface_sync` remain aligned with the current
  post-`H37` no-reopen interpretation, while `P21/P22` stay preserved prior
  syncs, `F9` stays blocked, `F11` stays new-substrate, and none of them
  imply `R41`, merge authorization, or a broadened runtime family.

## Paper-facing ledgers

- [ ] `manuscript_bundle_draft.md` still matches the fixed section and artifact
  ownership on current scope.
- [ ] `paper_bundle_status.md`, `layout_decision_log.md`,
  `freeze_candidate_criteria.md`, `main_text_order.md`, and
  `appendix_companion_scope.md` remain synchronized.
- [ ] `release_candidate_checklist.md`, `submission_candidate_criteria.md`,
  `claim_ladder.md`, and `archival_repro_manifest.md` all expose the same
  current `H58/H56/H57/H54/H52/H50/H43/H36/R42/R43/R44/R45/R58/R59/R60/R61/R62/P40/P27/P38`
  release-control stack while preserving `H43` as the paper-grade endpoint and
  do not revert wording back to earlier `H40` or `H32/H34` control states.
- [ ] `publication_record/README.md` and `plans/README.md` both expose the
  completed `F31/H57/R62/H58` closeout stack above preserved
  `H56/H54/H52/H43/H36`, the preserved `F7/F8/P21` wave, the preserved `F10/P22`
  bridge wave, and the preserved `F12/F13/F14/P23` family-first planning wave
  without widening wording.
- [ ] `blog_release_rules.md` still records the blocked-blog state explicitly.

## Machine-audited guards

- [ ] `results/P1_paper_readiness/summary.json` still reports `10/10` ready
  figure/table items on the frozen scope.
- [ ] `results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json`
  reports `stop_as_mechanism_supported_but_no_bounded_executor_value` and
  `next_required_lane = no_active_downstream_runtime_lane`.
- [ ] `results/H57_post_h56_last_discriminator_authorization_packet/summary.json`
  reports `authorize_one_last_native_useful_kernel_value_discriminator_gate`.
- [ ] `results/R62_origin_native_useful_kernel_value_discriminator_gate/summary.json`
  reports `native_useful_kernel_route_lacks_bounded_value` on `4/4` exact rows
  across `2/2` kernels.
- [ ] `results/P40_post_h56_successor_worktree_and_artifact_hygiene_sync/summary.json`
  reports zero blocked items and preserves the closed-wave operational/docs
  sync posture for the final discriminator wave.
- [ ] `results/H56_post_r60_r61_useful_kernel_decision_packet/summary.json`
  reports `freeze_minimal_useful_kernel_bridge_supported_without_bounded_value`
  and `next_required_lane = no_active_downstream_runtime_lane`.
- [ ] `results/R61_origin_compiled_useful_kernel_value_gate/summary.json`
  reports `compiled_useful_kernel_route_lacks_bounded_value`.
- [ ] `results/R60_origin_compiled_useful_kernel_carryover_gate/summary.json`
  reports `compiled_useful_kernel_carryover_supported_exactly` on `5/5`
  exact rows.
- [ ] `results/H54_post_r58_r59_compiled_boundary_decision_packet/summary.json`
  reports `freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value`
  and `next_required_lane = no_active_downstream_runtime_lane`.
- [ ] `results/H53_post_h52_compiled_boundary_reentry_packet/summary.json`
  reports `authorize_compiled_boundary_reentry_through_r58_first`.
- [ ] `results/R59_origin_compiled_trace_vm_execution_gate/summary.json`
  reports `compiled_trace_vm_execution_supported_exactly` on `5/5` exact rows.
- [ ] `results/R58_origin_restricted_stack_bytecode_lowering_contract_gate/summary.json`
  reports `restricted_stack_bytecode_lowering_supported_narrowly` on `5/5`
  fixed rows.
- [ ] `results/H52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json`
  remains available as the preserved prior mechanism closeout.
- [ ] `results/R57_origin_accelerated_trace_vm_comparator_gate/summary.json`
  remains available as the preserved negative fast-path comparator gate.
- [ ] `results/R56_origin_append_only_trace_vm_semantics_gate/summary.json`
  remains available as the preserved exact trace-VM semantics gate.
- [ ] `results/R55_origin_2d_hardmax_retrieval_equivalence_gate/summary.json`
  remains available as the preserved exact retrieval-equivalence gate.
- [ ] `results/H50_post_r51_r52_scope_decision_packet/summary.json` reports
  `stop_as_exact_without_system_value` and preserves the broader-route
  bounded-value falsifier.
- [ ] `results/H43_post_r44_useful_case_refreeze/summary.json` still reports
  `freeze_r44_as_narrow_supported_here`, `claim_d_state =
  supported_here_narrowly`, and the preserved paper-grade endpoint.
- [ ] `results/R44_origin_restricted_wasm_useful_case_execution_gate/summary.json`
  reports `useful_case_surface_supported_narrowly`, `exact_kernel_count = 3`,
  and bounded useful-case support only.
- [ ] `results/R45_origin_dual_mode_model_mainline_gate/summary.json` reports
  `coequal_model_lane_supported_without_replacing_exact` and keeps exact `R43`
  decisive.
- [ ] `results/R43_origin_bounded_memory_small_vm_execution_gate/summary.json`
  reports `keep_semantic_boundary_route` on `5/5` fixed families.
- [ ] `results/P27_post_h41_clean_promotion_and_explicit_merge_packet/summary.json`
  reports `promotion_mode = explicit_merge_wave` and `merge_executed = false`.
- [ ] `results/P38_post_h52_compiled_boundary_hygiene_sync/summary.json`
  reports zero blocked items and preserves the closed-wave operational/docs
  sync posture.
- [ ] `results/R42_origin_append_only_memory_retrieval_contract_gate/summary.json`
  reports `keep_semantic_boundary_route`, exact value plus maximizer-row
  identity, and `later_explicit_packet_required = true`.
- [ ] `results/H40_post_h38_semantic_boundary_activation_packet/summary.json`
  remains available as the preserved prior activation packet that authorized
  `R42`.
- [ ] `results/H38_post_f16_runtime_relevance_reopen_decision_packet/summary.json`
  reports `keep_h36_freeze` and remains available as the preserved prior
  docs-only decision packet.
- [ ] `results/P26_post_h37_promotion_and_artifact_hygiene_audit/summary.json`
  reports `audit_only`, `merge_recommended = false`, and the clean audit
  branch/worktree.
- [ ] `results/H37_post_h36_runtime_relevance_decision_packet/summary.json`
  reports `keep_h36_freeze` and remains available as the preserved earlier
  docs-only decision packet.
- [ ] `results/H36_post_r40_bounded_scalar_family_refreeze/summary.json`
  reports the preserved active routing/refreeze packet and keeps `R41`
  deferred.
- [ ] `results/P25_post_h36_clean_promotion_prep/summary.json` reports
  `prepare_only`, `merge_authorized = false`, and remains available as the
  preserved prior clean source-of-truth branch/worktree.
- [ ] `results/H35_post_p23_bounded_scalar_family_runtime_decision_packet/summary.json`
  remains available as the preserved prior docs-only bounded-scalar runtime
  authorization packet.
- [ ] `results/R40_origin_bounded_scalar_locals_and_flags_gate/summary.json`
  remains available as the completed bounded-scalar runtime gate on the
  current substrate.
- [ ] `results/H34_post_r39_later_explicit_scope_decision_packet/summary.json`
  remains available as the preserved earlier freeze-complete-for-now control
  packet.
- [ ] `results/H32_post_r38_compiled_boundary_refreeze/summary.json`
  reports zero blocked items on the preserved earlier compiled-boundary
  routing/refreeze packet.
- [ ] `results/R39_origin_compiler_control_surface_dependency_audit/summary.json`
  remains available as the completed same-substrate dependency audit on one
  declared helper-body permutation with target renumbering.
- [ ] `results/H33_post_h32_conditional_next_question_packet/summary.json`
  remains available as the preserved prior docs-only question-selection packet.
- [ ] `results/R38_origin_compiler_control_surface_extension_gate/summary.json`
  remains available as the preserved richer same-substrate compiled control
  gate.
- [ ] `results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json`
  remains available as the preserved explicit later-decision packet.
- [ ] `results/H30_post_r36_r37_scope_decision_packet/summary.json`
  remains available as the preserved prior compiled-boundary refreeze packet.
- [ ] `results/R37_origin_compiler_boundary_gate/summary.json` remains
  available as the preserved tiny compiled-boundary gate.
- [ ] `results/H29_refreeze_after_r34_r35_origin_core_gate/summary.json`
  remains available as the preserved upstream refreeze packet.
- [ ] `results/H28_post_h27_origin_core_reanchor_packet/summary.json` remains
  available as the preserved Origin-core pivot packet.
- [ ] `results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`
  remains available as the preserved negative same-endpoint closeout packet.
- [ ] `results/R34_origin_retrieval_primitive_contract_gate/summary.json`
  remains available as the preserved primitive-contract gate.
- [ ] `results/R35_origin_append_only_stack_vm_execution_gate/summary.json`
  remains available as the preserved exact execution gate.
- [ ] `results/R36_origin_long_horizon_precision_scaling_gate/summary.json`
  remains available as the preserved narrow precision-boundary follow-up.
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
