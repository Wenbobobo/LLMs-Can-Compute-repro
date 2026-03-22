# Active Wave Plan

## Current Wave

Current scientific/control stack:

- current active decision packet:
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
- blocked future lanes:
  `R29_d0_same_endpoint_systems_recovery_execution_gate` and
  `F3_post_h23_scope_lift_decision_bundle`;
- future frontier review:
  `F2_future_frontier_recheck_activation_matrix` remains planning-only.

Immediate active wave:

Origin-core refreeze active after one narrow compiled-boundary confirmation

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
- `R29`, `F3`, and frontier/demo widening remain blocked.

## Immediate Objectives

1. Preserve `H30` as the current active routing packet.
2. Preserve `H29`, `R36`, and `R37` as the frozen upstream evidence chain.
3. Keep the compiled-boundary result narrow: one tiny lowered subset only.
4. Avoid reopening `R29`, `F3`, broader compiler/demo scope, or frontier
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
`H30_post_r36_r37_scope_decision_packet`

## Next Conditional Order

later explicit packet ->
conditional compiler-boundary extension or language-boundary clarification
packet

## Current References

- `docs/plans/2026-03-22-post-h30-explicit-next-wave-design.md`
- `docs/milestones/P17_h30_commit_hygiene_and_clean_worktree_promotion/`
- `docs/plans/2026-03-22-post-r36-explicit-next-wave-design.md`
- `docs/milestones/H29_refreeze_after_r34_r35_origin_core_gate/`
- `docs/milestones/R36_origin_long_horizon_precision_scaling_gate/`
- `docs/milestones/R37_origin_compiler_boundary_gate/`
- `docs/milestones/H30_post_r36_r37_scope_decision_packet/`
- `results/H29_refreeze_after_r34_r35_origin_core_gate/summary.json`
- `results/R36_origin_long_horizon_precision_scaling_gate/summary.json`
- `results/R37_origin_compiler_boundary_gate/summary.json`
- `results/H30_post_r36_r37_scope_decision_packet/summary.json`

## If Blocked

- `P17` closeout is already complete on `wip/p17-h30-clean`; do not reopen it
  unless the clean packet needs to be restaged;
- do not reopen `R29` or `F3` by momentum;
- do not convert `H27` into a soft authorization for same-endpoint recovery;
- do not relabel one tiny compiled boundary as arbitrary-language support;
- do not skip the saved post-`H30` plan when evaluating the next explicit
  packet;
- require a later explicit packet before any further compiler-boundary
  extension.
