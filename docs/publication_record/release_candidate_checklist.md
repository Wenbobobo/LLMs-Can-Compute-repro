# Release Candidate Checklist

State: `standing_gate`.

This checklist defines the minimum outward-facing sync required for a restrained
release-candidate state after the current submission-candidate bundle lock on
the current `H58` active docs-only closeout packet plus preserved prior
`H56/H57/H54/H52/H50` control context plus `H43` paper-grade useful-case
refreeze / `H36` preserved-active /
`R42-R43-R44-R45-R58-R59-R60-R61-R62` completed current and preserved-late
evidence stack / preserved prior `R49-R50-R51-R52-R55-R56-R57` useful-case
and mechanism stack / blocked `F27/R53/R54` /
`P40-P38-P28-P27` completed downstream sync-and-explicit-no-merge posture /
`F31-F20-F16-F17-F18-F19-F15-F30-F29` current-control-support /
`H57-H56-H54-H53-H52-H50-H42-H41-H40-H38-H37-P26-P25`
preserved immediate-predecessor support /
`H35-H34-H33-H32-H31-H30` preserved question-selection-and-decision /
`H29` preserved-upstream-refreeze / `H27-H28`
preserved-closeout-and-pivot stack.

## Wording and scope

- [ ] `README.md` keeps the narrow endpoint and blocked non-goals explicit.
- [ ] `STATUS.md` matches the same frozen scope and the current next action
  recorded by active `H58`, preserved `H56/H57/H54/H52/H50`, preserved
  `H43/H42/H41/H40/H38/H37`, preserved `H36`, completed
  `R42/R43/R44/R45/R58/R59/R60/R61/R62`, blocked `F27/R53/R54`, completed
  `P40/P38/P28/P27`, current `F31/F20/F16/F17/F18/F19`, preserved `P26/P25`,
  and current `F15`.
- [ ] `release_summary_draft.md` remains the short public-surface source.
- [ ] `P20`, `F5`, and `F6` remain aligned with the same no-reopen
  interpretation and do not imply a new evidence wave.
- [ ] `F7`, `F8`, `F10`, `F12`, `F13`, `F14`, and `P23` remain aligned with
  that same planning-only no-reopen interpretation, while `P21/P22` stay
  preserved prior syncs, `F9` stays blocked, `F11` stays new-substrate, and
  none of them imply a new evidence wave, `R41`, merge authorization, or a
  broadened runtime family.
- [ ] No outward wording implies a new evidence wave or broader compiled scope.

## Paper-facing dependencies

- [ ] `submission_candidate_criteria.md` is satisfied on the current repo state.
- [ ] `paper_bundle_status.md`, `layout_decision_log.md`, and
  `publication_record/README.md` all describe the same `H58` current control /
  `H43` paper-grade endpoint / `H36` preserved active /
  `R42-R43-R44-R45-R58-R59-R60-R61-R62` completed current gate stack /
  preserved prior `R49-R50-R51-R52-R55-R56-R57` support stack /
  `P40-P38-P28-P27` completed operational sync-and-explicit-no-merge posture /
  `F31-F20-F16-F17-F18-F19-F15-F30-F29` current support /
  `H57-H56-H54-H53-H52-H50-H42-H41-H40-H38-H37-P26-P25`
  preserved immediate-predecessor support /
  `H35-H34-H33-H32-H31-H30-H29-H27-H28` preserved current control package.
- [ ] `plans/README.md`, the saved post-`P20/F5/F6` handoff surfaces, and the
  saved post-`H34` planning-wave surface still present docs/planning
  maintenance as admissible while runtime remains inactive by default.
- [ ] `publication_record/README.md` and the saved planning-wave surfaces
  present the completed `F31/H57/R62/H58` wave above preserved
  `H56/H54/H52/H43/H36`, the preserved `H40/R42/P26/F17/F18/F19/H38/F16/P25/F15/H37`
  support wave, the
  preserved `F7/F8/P21` wave, the preserved `F10/P22` bridge wave, and the
  preserved `F12/F13/F14/P23` family-first wave while keeping `F9` blocked
  and `F11` new-substrate.
- [ ] The blocked-blog rule remains explicit in both `blog_release_rules.md`
  and `blog_outline.md`.

## Machine-audited guards

- [ ] `results/P1_paper_readiness/summary.json` still reports `10/10` ready
  items on the frozen scope.
- [ ] `results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json`
  reports the current active docs-only closeout packet,
  `stop_as_mechanism_supported_but_no_bounded_executor_value`, and
  `next_required_lane = no_active_downstream_runtime_lane`.
- [ ] `results/H57_post_h56_last_discriminator_authorization_packet/summary.json`
  reports the preserved prior last-discriminator authorization packet and
  `authorize_one_last_native_useful_kernel_value_discriminator_gate`.
- [ ] `results/R62_origin_native_useful_kernel_value_discriminator_gate/summary.json`
  reports the completed native value-negative discriminator on `4/4` exact rows
  across `2/2` kernels.
- [ ] `results/P40_post_h56_successor_worktree_and_artifact_hygiene_sync/summary.json`
  reports the completed operational/docs sidecar for the closed final
  discriminator wave.
- [ ] `results/H56_post_r60_r61_useful_kernel_decision_packet/summary.json`
  reports the preserved prior compiled useful-kernel closeout packet,
  `freeze_minimal_useful_kernel_bridge_supported_without_bounded_value`, and
  `next_required_lane = no_active_downstream_runtime_lane`.
- [ ] `results/R61_origin_compiled_useful_kernel_value_gate/summary.json`
  reports the preserved prior compiled useful-kernel value-negative gate.
- [ ] `results/R60_origin_compiled_useful_kernel_carryover_gate/summary.json`
  reports the preserved prior exact compiled useful-kernel carryover gate.
- [ ] `results/H54_post_r58_r59_compiled_boundary_decision_packet/summary.json`
  reports the preserved prior compiled-boundary closeout packet,
  `freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value`,
  and `next_required_lane = no_active_downstream_runtime_lane`.
- [ ] `results/H53_post_h52_compiled_boundary_reentry_packet/summary.json`
  reports the preserved prior compiled-boundary reentry packet and
  `authorize_compiled_boundary_reentry_through_r58_first`.
- [ ] `results/F29_post_h52_restricted_compiled_boundary_bundle/summary.json`
  reports the preserved current planning bundle and
  `next_required_lane = r58_origin_restricted_stack_bytecode_lowering_contract_gate`.
- [ ] `results/H52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json`
  reports the preserved prior mechanism closeout packet,
  `freeze_origin_mechanism_supported_without_fastpath_value`, and
  `next_required_lane = no_active_downstream_runtime_lane`.
- [ ] `results/H43_post_r44_useful_case_refreeze/summary.json` reports the
  preserved paper-grade useful-case refreeze packet,
  `freeze_r44_as_narrow_supported_here`, and `claim_d_state =
  supported_here_narrowly`.
- [ ] `results/H50_post_r51_r52_scope_decision_packet/summary.json` reports the
  preserved broader-route closeout packet and `stop_as_exact_without_system_value`.
- [ ] `results/R58_origin_restricted_stack_bytecode_lowering_contract_gate/summary.json`
  reports the completed exact compiled-boundary lowering gate.
- [ ] `results/R59_origin_compiled_trace_vm_execution_gate/summary.json`
  reports the completed exact compiled trace-VM execution gate.
- [ ] `results/R55_origin_2d_hardmax_retrieval_equivalence_gate/summary.json`
  remains available as the preserved exact retrieval-equivalence gate.
- [ ] `results/R56_origin_append_only_trace_vm_semantics_gate/summary.json`
  remains available as the preserved exact trace-VM semantics gate.
- [ ] `results/R57_origin_accelerated_trace_vm_comparator_gate/summary.json`
  remains available as the preserved negative fast-path comparator gate.
- [ ] `results/R42_origin_append_only_memory_retrieval_contract_gate/summary.json`
  reports the completed preserved retrieval-contract gate,
  `keep_semantic_boundary_route`, exact value plus maximizer-row identity, and
  `later_explicit_packet_required = true`.
- [ ] `results/R43_origin_bounded_memory_small_vm_execution_gate/summary.json`
  reports the completed current exact bounded-memory gate on `5/5` fixed
  families.
- [ ] `results/R44_origin_restricted_wasm_useful_case_execution_gate/summary.json`
  reports the completed current restricted useful-case gate,
  `useful_case_surface_supported_narrowly`, and `exact_kernel_count = 3`.
- [ ] `results/R45_origin_dual_mode_model_mainline_gate/summary.json`
  reports the completed current coequal model lane without replacing exact
  evidence.
- [ ] `results/P28_post_h43_publication_surface_sync/summary.json` reports the
  completed publication/control sync packet that keeps the paper-grade `H43`
  bundle aligned.
- [ ] `results/P27_post_h41_clean_promotion_and_explicit_merge_packet/summary.json`
  reports the completed explicit merge packet and keeps
  `merge_executed = false`.
- [ ] `results/P38_post_h52_compiled_boundary_hygiene_sync/summary.json`
  reports the completed operational/docs sidecar for the closed
  compiled-boundary wave.
- [ ] `results/H42_post_r43_route_selection_packet/summary.json` reports the
  preserved prior docs-only packet that authorized exact `R44`.
- [ ] `results/H41_post_r42_aggressive_long_arc_decision_packet/summary.json`
  reports the preserved earlier docs-only decision packet that authorized
  exact `R43` plus coequal `R45`.
- [ ] `results/H40_post_h38_semantic_boundary_activation_packet/summary.json`
  remains available as the preserved prior activation packet that authorized
  `R42`.
- [ ] `results/H38_post_f16_runtime_relevance_reopen_decision_packet/summary.json`
  reports the preserved prior docs-only decision packet, `keep_h36_freeze`,
  and no active downstream runtime lane.
- [ ] `results/P26_post_h37_promotion_and_artifact_hygiene_audit/summary.json`
  reports the completed operational audit lane and `audit_only` merge posture.
- [ ] `results/H37_post_h36_runtime_relevance_decision_packet/summary.json`
  reports the preserved prior docs-only decision packet and
  `keep_h36_freeze`.
- [ ] `results/H36_post_r40_bounded_scalar_family_refreeze/summary.json`
  reports the preserved active routing/refreeze packet without widening scope.
- [ ] `results/P25_post_h36_clean_promotion_prep/summary.json` reports the
  preserved prior operational prep lane and `prepare_only` merge posture.
- [ ] `results/H35_post_p23_bounded_scalar_family_runtime_decision_packet/summary.json`
  records the preserved prior docs-only bounded-scalar runtime authorization
  packet.
- [ ] `results/R40_origin_bounded_scalar_locals_and_flags_gate/summary.json`
  records the completed bounded-scalar runtime gate and does not imply broader
  value semantics.
- [ ] `results/H34_post_r39_later_explicit_scope_decision_packet/summary.json`
  records the preserved earlier freeze-complete-for-now control packet.
- [ ] `results/H32_post_r38_compiled_boundary_refreeze/summary.json`
  reports the preserved earlier compiled-boundary routing/refreeze packet
  without widening scope.
- [ ] `results/R39_origin_compiler_control_surface_dependency_audit/summary.json`
  reports one declared helper-body permutation with target renumbering only
  and does not imply broader compiler support.
- [ ] `results/H33_post_h32_conditional_next_question_packet/summary.json`
  records the preserved prior docs-only question-selection packet.
- [ ] `results/R38_origin_compiler_control_surface_extension_gate/summary.json`
  reports one richer same-substrate compiled control family only and does not
  imply broader compiler support.
- [ ] `results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json`
  records the preserved explicit later-decision packet.
- [ ] `results/H30_post_r36_r37_scope_decision_packet/summary.json`
  records the preserved prior compiled-boundary refreeze packet without
  widening scope.
- [ ] `results/R37_origin_compiler_boundary_gate/summary.json` reports one
  tiny compiled-boundary gate only and does not imply broader compiler support.
- [ ] `results/H29_refreeze_after_r34_r35_origin_core_gate/summary.json`
  remains available as the preserved upstream Origin-core refreeze packet.
- [ ] `results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`
  still records the preserved negative same-endpoint closeout.
- [ ] `results/H28_post_h27_origin_core_reanchor_packet/summary.json` still
  records the preserved Origin-core pivot packet.
- [ ] `results/R36_origin_long_horizon_precision_scaling_gate/summary.json`
  still records the preserved narrow precision-boundary follow-up.
- [ ] `results/H15_refreeze_and_decision_sync/summary.json` reports zero
  blocked items on the preserved earlier refrozen control surface.
- [ ] `results/H14_core_first_reopen_guard/summary.json` reports zero blocked
  items on the preserved earlier core-first reopen control surface.
- [ ] `results/H13_post_h12_governance_stage_health/summary.json` reports zero
  blocked items on the preserved governance/runtime handoff.
- [ ] `results/P5_public_surface_sync/summary.json` reports zero blocked items
  on the current `H43`-aligned public surface.
- [ ] `results/P5_callout_alignment/summary.json` reports zero blocked rows.
- [ ] `results/H2_bundle_lock_audit/summary.json` reports zero blocked items.
- [ ] `results/release_worktree_hygiene_snapshot/summary.json` classifies
  whether the current worktree blocks an outward sync commit.
- [ ] `results/release_preflight_checklist_audit/summary.json` reports
  `docs_and_audits_green` with zero blocked items.
- [ ] `results/V1_full_suite_validation_runtime_timing_followup/summary.json`
  reports `healthy_but_slow` with zero timed-out files.

## Release hygiene

- [ ] `results/release_worktree_hygiene_snapshot/summary.json` is checked
  before the outward sync commit.
- [ ] No local-only source material under `docs/Origin/` or `docs/origin/`
  appears in public-facing docs or release notes.
- [ ] Blog work remains blocked unless this checklist and
  `blog_release_rules.md` are both satisfied in full.
