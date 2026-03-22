# Active Wave Plan

## Current Wave

Current scientific/control stack:

- current active decision packet:
  `H32_post_r38_compiled_boundary_refreeze`;
- current docs-only control packet:
  `H33_post_h32_conditional_next_question_packet`;
- preserved later explicit packet:
  `H31_post_h30_later_explicit_boundary_decision_packet`;
- preserved prior compiled-boundary refreeze packet:
  `H30_post_r36_r37_scope_decision_packet`;
- preserved prior Origin-core refreeze packet:
  `H29_refreeze_after_r34_r35_origin_core_gate`;
- preserved same-endpoint closeout packet:
  `H27_refreeze_after_r32_r33_same_endpoint_decision`;
- preserved upstream primitive gate:
  `R34_origin_retrieval_primitive_contract_gate`;
- preserved upstream execution gate:
  `R35_origin_append_only_stack_vm_execution_gate`;
- preserved narrow precision lane:
  `R36_origin_long_horizon_precision_scaling_gate`;
- preserved tiny compiled-boundary lane:
  `R37_origin_compiler_boundary_gate`;
- preserved richer control-surface extension lane:
  `R38_origin_compiler_control_surface_extension_gate`;
- completed same-substrate dependency audit lane:
  `R39_origin_compiler_control_surface_dependency_audit`;
- blocked future lanes:
  `R29_d0_same_endpoint_systems_recovery_execution_gate` and
  `F3_post_h23_scope_lift_decision_bundle`;
- future frontier review:
  `F2_future_frontier_recheck_activation_matrix` remains planning-only.

Immediate active wave:

Origin-core refreeze remains active while `H33` holds the docs-only control
surface and `R39` sits as a completed downstream audit awaiting a later
explicit decision packet

## Current Facts

- `H27` closes the old same-endpoint `D0` recovery wave at
  `systems_more_sharply_negative`.
- `H28` reanchored the scientific target around append-only traces, exact `2D`
  hard-max retrieval, and a small exact stack/VM executor.
- `H29` freezes `R34` and `R35` as a positive Origin-core evidence chain on the
  current bundle.
- `R36` makes the narrow precision boundary explicit: float32 `single_head`
  collapses on selected inflated-horizon memory/stack rows while `radix2` and
  `block_recentered` stay exact on the same rows.
- `R37` then shows that one admitted tiny bytecode subset stays exact across
  source reference, lowered interpreter, and accelerated free-running
  execution on the current substrate.
- `H30` freezes that result as narrow compiled-boundary evidence only.
- `H31` authorizes exactly one more tiny extension on the same substrate.
- `R38` shows that one richer subroutine/control family and one longer
  same-family boundary probe stay exact without widening the opcode surface.
- `H32` freezes that result as narrow same-substrate evidence only.
- `R39` then shows that one declared helper-body permutation with target
  renumbering preserves exact source/lowered/free-running execution and final
  state on both the admitted row and the named same-family boundary probe,
  while changing trace on both rows.
- `R29`, `F3`, and frontier/demo widening remain blocked.

## Immediate Objectives

1. Preserve `H32` as the current active routing packet.
2. Preserve `H30`, `H31`, and `R38` as the narrow compiled-boundary evidence
   chain above `H29/R36/R37`.
3. Keep the compiled-boundary result narrow: one tiny subset plus one richer
   control/call family only.
4. Avoid reopening `R29`, `F3`, broader compiler/demo scope, or frontier
   widening by momentum.
5. Treat `P18_post_h32_clean_worktree_promotion` as completed operational
   closeout on this clean branch.
6. Preserve `H33` as the current docs-only packet selecting exactly one
   narrow same-substrate question.
7. Preserve `R39_origin_compiler_control_surface_dependency_audit` as a
   completed downstream same-substrate audit, not a routing change by itself.
8. Keep `F2_future_frontier_recheck_activation_matrix` planning-only and
   downstream of `H33/R39`.

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
`R39_origin_compiler_control_surface_dependency_audit`

## Next Conditional Order

later explicit post-`R39` decision packet

## Current References

- `docs/plans/2026-03-23-post-h32-conditional-next-packet-design.md`
- `docs/plans/2026-03-23-post-h33-r39-origin-core-substrate-question-design.md`
- `docs/plans/2026-03-22-post-h30-h31-r38-extension-plan.md`
- `docs/milestones/P18_post_h32_clean_worktree_promotion/`
- `docs/milestones/H33_post_h32_conditional_next_question_packet/`
- `docs/milestones/R39_origin_compiler_control_surface_dependency_audit/`
- `docs/milestones/F2_future_frontier_recheck_activation_matrix/`
- `docs/plans/2026-03-22-post-h30-explicit-next-wave-design.md`
- `docs/milestones/H31_post_h30_later_explicit_boundary_decision_packet/`
- `docs/milestones/R38_origin_compiler_control_surface_extension_gate/`
- `docs/milestones/H32_post_r38_compiled_boundary_refreeze/`
- `results/H30_post_r36_r37_scope_decision_packet/summary.json`
- `results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json`
- `results/R38_origin_compiler_control_surface_extension_gate/summary.json`
- `results/H32_post_r38_compiled_boundary_refreeze/summary.json`
- `results/H33_post_h32_conditional_next_question_packet/summary.json`
- `results/R39_origin_compiler_control_surface_dependency_audit/summary.json`

## If Blocked

- `P17` closeout remains complete on `wip/p17-h30-clean`; do not reopen it;
- `P18` is the current clean-branch packaging surface; do not merge back into
  dirty `main` or dirty `wip/h27-promotion` by momentum;
- do not treat `H33` or the local `R39` positive result as broader compiled or
  frontier authorization by themselves;
- do not reopen `R29` or `F3` by wording alone;
- do not relabel one richer compiled control family as arbitrary-language
  support;
- do not skip the saved post-`H30` / `H31` / `R38` plan, the saved
  post-`H32` plan, or the landed `R39` audit when evaluating any later
  broader lane;
- require a later explicit post-`R39` decision packet before any routing or
  scope change.
