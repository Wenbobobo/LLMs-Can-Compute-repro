# Active Wave Plan

## Current Wave

Current scientific/control stack:

- current active docs-only decision packet:
  `H38_post_f16_runtime_relevance_reopen_decision_packet`;
- preserved active routing/refreeze packet:
  `H36_post_r40_bounded_scalar_family_refreeze`;
- completed operational promotion/artifact audit lane:
  `P26_post_h37_promotion_and_artifact_hygiene_audit`;
- current canonical origin-facing derivative bundle:
  `F15_post_h36_origin_goal_reanchor_bundle`;
- current candidate-isolation bundle:
  `F16_post_h37_r41_candidate_isolation_bundle`;
- current same-substrate exit bundle:
  `F17_post_h38_same_substrate_exit_criteria_bundle`;
- current long-arc planning bundle:
  `F18_post_h38_origin_core_long_arc_bundle`;
- current semantic-boundary useful-case roadmap:
  `F19_post_f18_restricted_wasm_useful_case_roadmap`;
- preserved prior docs-only runtime-relevance decision packet:
  `H37_post_h36_runtime_relevance_decision_packet`;
- preserved prior clean promotion-prep lane:
  `P25_post_h36_clean_promotion_prep`;
- deferred future runtime blueprint:
  `R41_origin_runtime_relevance_threat_stress_audit`;
- deferred future semantic-boundary gates:
  `R42_origin_append_only_memory_retrieval_contract_gate`,
  `R43_origin_bounded_memory_small_vm_execution_gate`,
  `R44_origin_restricted_wasm_useful_case_execution_gate`;
- blocked future lanes:
  `R29_d0_same_endpoint_systems_recovery_execution_gate` and
  `F3_post_h23_scope_lift_decision_bundle`.

Immediate active wave:

`F18` fixes the post-`H38` claim ladder, preferred route, and worktree/merge
policy, while `F19` turns the preserved `F9` family into a decision-complete
semantic-boundary roadmap and freezes `R42/R43/R44` as deferred future gates
without creating a runtime lane.

## Current Facts

- `wip/p25-f15-h37-exec` remains the preserved prior clean source branch for
  the landed `P25/F15/H37` wave.
- `wip/f16-h38-p26-exec` is the current clean audit branch for the
  `F16/H38/P26/F17` control wave.
- dirty `main` remains untouched by design in this wave.
- `H36` still preserves
  `bounded_scalar_family_refrozen_narrowly` and
  `no_active_downstream_runtime_lane`.
- `F16` assigns `nonunique`, `nonunique`, and `inadmissible` across the three
  saved `R41` candidates and ends at `no_candidate_ready`.
- `H38` selects `keep_h36_freeze` and names no active runtime candidate.
- `P26` keeps promotion posture at `audit_only` and records no immediate
  `.gitignore` change for the user-mentioned `R20` raw file because it is not
  present on the current clean source branch.
- `F17` separates later same-substrate, restricted-semantics, hybrid, and
  publication-only routes without authorizing any now.
- `F18` makes `F9` the default forward planning family after `H38`.
- `F19` fixes a bounded restricted-Wasm / tiny-`C` surface plus the three
  useful kernels:
  `sum_i32_buffer`,
  `count_nonzero_i32_buffer`,
  `histogram16_u8`.
- `wip/f18-f19-planning` is the clean planning branch for this wave.

## Immediate Objectives

1. Preserve `H38` as the current active docs-only decision packet.
2. Preserve `H36` as the active routing/refreeze packet underneath the stack.
3. Preserve `F16` as `no_candidate_ready`.
4. Preserve `P26` as `audit_only`, not merge authorization.
5. Preserve `F17` as planning-only route storage.
6. Land `F18` as the long-arc route-fixing bundle.
7. Land `F19` as the semantic-boundary useful-case roadmap.
8. Keep `R41` deferred until a later explicit post-`H38` packet authorizes it.
9. Keep `R42/R43/R44` deferred until a later explicit semantic-boundary packet
   authorizes them.
10. Avoid reopening `R29`, `F3`, broader compiler/demo scope, or frontier
   widening by momentum.

## Last Completed Order

Immediate completed order:

`P16_h25_commit_hygiene_and_clean_worktree_promotion` ->
clean-worktree `R32_d0_family_local_boundary_sharp_zoom` ->
`H26_refreeze_after_r32_boundary_sharp_zoom` ->
clean-worktree `R33_d0_non_retrieval_overhead_localization_audit` ->
`H27_refreeze_after_r32_r33_same_endpoint_decision` ->
`H28_post_h27_origin_core_reanchor_packet` ->
`R34_origin_retrieval_primitive_contract_gate` ->
`R35_origin_append_only_stack_vm_execution_gate` ->
`H29_refreeze_after_r34_r35_origin_core_gate` ->
`R36_origin_long_horizon_precision_scaling_gate` ->
`R37_origin_compiler_boundary_gate` ->
`H30_post_r36_r37_scope_decision_packet` ->
`H31_post_h30_later_explicit_boundary_decision_packet` ->
`R38_origin_compiler_control_surface_extension_gate` ->
`H32_post_r38_compiled_boundary_refreeze` ->
`H33_post_h32_conditional_next_question_packet` ->
`R39_origin_compiler_control_surface_dependency_audit` ->
`H34_post_r39_later_explicit_scope_decision_packet` ->
`H35_post_p23_bounded_scalar_family_runtime_decision_packet` ->
`R40_origin_bounded_scalar_locals_and_flags_gate` ->
`H36_post_r40_bounded_scalar_family_refreeze` ->
`P25_post_h36_clean_promotion_prep` ->
`F15_post_h36_origin_goal_reanchor_bundle` ->
`H37_post_h36_runtime_relevance_decision_packet` ->
`F16_post_h37_r41_candidate_isolation_bundle` ->
`H38_post_f16_runtime_relevance_reopen_decision_packet` ->
`P26_post_h37_promotion_and_artifact_hygiene_audit` ->
`F17_post_h38_same_substrate_exit_criteria_bundle` ->
`F18_post_h38_origin_core_long_arc_bundle` ->
`F19_post_f18_restricted_wasm_useful_case_roadmap`

## Current Rule

- `H38` is the current active docs-only packet.
- `H36` remains the active routing/refreeze packet underneath it.
- `P26` remains audit-only and keeps dirty `main` untouched.
- `F16` is allowed to isolate candidates but not to authorize runtime.
- `F17` is allowed to store routes but not to activate them.
- `F18` is allowed to fix the long-arc route but not to change active routing.
- `F19` is allowed to fix the semantic-boundary roadmap but not to authorize a
  gate.
- `R41` stays deferred until a later explicit packet names exactly one
  execution-ready candidate.
- `R42`, `R43`, and `R44` stay deferred until a later explicit semantic-
  boundary packet names them.

## Control References

- `docs/publication_record/current_stage_driver.md`
- `docs/plans/2026-03-23-post-h38-f18-f19-long-arc-design.md`
- `docs/plans/2026-03-23-post-h37-f16-h38-p26-candidate-isolation-design.md`
- `docs/milestones/F16_post_h37_r41_candidate_isolation_bundle/`
- `docs/milestones/H38_post_f16_runtime_relevance_reopen_decision_packet/`
- `docs/milestones/P26_post_h37_promotion_and_artifact_hygiene_audit/`
- `docs/milestones/F17_post_h38_same_substrate_exit_criteria_bundle/`
- `docs/milestones/F18_post_h38_origin_core_long_arc_bundle/`
- `docs/milestones/F19_post_f18_restricted_wasm_useful_case_roadmap/`
- `docs/milestones/R41_origin_runtime_relevance_threat_stress_audit/`
- `docs/milestones/R42_origin_append_only_memory_retrieval_contract_gate/`
- `docs/milestones/R43_origin_bounded_memory_small_vm_execution_gate/`
- `docs/milestones/R44_origin_restricted_wasm_useful_case_execution_gate/`
- `results/H38_post_f16_runtime_relevance_reopen_decision_packet/summary.json`
- `results/P26_post_h37_promotion_and_artifact_hygiene_audit/summary.json`
- `results/H37_post_h36_runtime_relevance_decision_packet/summary.json`
- `results/H36_post_r40_bounded_scalar_family_refreeze/summary.json`
