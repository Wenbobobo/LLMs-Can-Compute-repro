# Active Wave Plan

## Current Wave

Current scientific/control stack:

- current active docs-only decision packet:
  `H56_post_r60_r61_useful_kernel_decision_packet`;
- preserved prior docs-only closeout:
  `H54_post_r58_r59_compiled_boundary_decision_packet`;
- preserved prior useful-kernel reentry packet:
  `H55_post_h54_useful_kernel_reentry_packet`;
- preserved prior paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`;
- preserved active routing/refreeze packet:
  `H36_post_r40_bounded_scalar_family_refreeze`;
- current planning bundle:
  `F30_post_h54_useful_kernel_bridge_bundle`;
- current low-priority operational/docs wave:
  `P39_post_h54_successor_worktree_hygiene_sync`;
- completed useful-kernel carryover gate:
  `R60_origin_compiled_useful_kernel_carryover_gate`;
- completed value gate:
  `R61_origin_compiled_useful_kernel_value_gate`;
- current downstream scientific lane:
  `no_active_downstream_runtime_lane`;
- blocked future storage:
  `F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle`,
  `R53_origin_transformed_executor_entry_gate`, and
  `R54_origin_trainable_executor_comparator_gate`.

Immediate active wave:

`F30_post_h54_useful_kernel_bridge_bundle` remains the preserved planning
bundle that fixed `H55 -> R60 -> R61 -> H56` as the only admissible order.

`H55_post_h54_useful_kernel_reentry_packet` remains the preserved prior
useful-kernel reentry packet. It selected
`authorize_useful_kernel_carryover_through_r60_first` and kept `H54`
visible rather than overturning it.

`P39_post_h54_successor_worktree_hygiene_sync` remains the current
low-priority operational/docs wave. It keeps the clean control worktree,
raw-row dumps and artifacts above roughly `10 MiB` out-of-git by default,
and explicit no-merge posture for this wave.

`R60_origin_compiled_useful_kernel_carryover_gate` is completed with
`compiled_useful_kernel_carryover_supported_exactly` on `5/5` admitted
preserved `sum/count` variants with translation-identity exact carryover and
exact source/spec/lowered plus exact linear/accelerated internal execution.

`R61_origin_compiled_useful_kernel_value_gate` is completed with
`compiled_useful_kernel_route_lacks_bounded_value` on the exact `R60` rows:
all declared comparators stay exact on `5/5`, but accelerated execution is
slower than transparent and external baselines once compiler/lowering overhead
is counted.

`H56_post_r60_r61_useful_kernel_decision_packet` is now the current active
packet and selects
`freeze_minimal_useful_kernel_bridge_supported_without_bounded_value`.

## Immediate Objectives

1. Preserve `H54` as a landed prior compiled-boundary closeout.
2. Preserve `H43` as the paper-grade endpoint.
3. Preserve `H36` as the routing/refreeze packet underneath the current stack.
4. Preserve `H55` as the explicit useful-kernel reentry history.
5. Preserve `R60` as completed exact compiled useful-kernel carryover evidence.
6. Preserve `R61` as completed value-negative comparator evidence.
7. Keep `H56` as the current docs-only closeout packet.
8. Keep the downstream scientific lane at `no_active_downstream_runtime_lane`.
9. Keep `F27`, `R53`, and `R54` blocked.
10. Keep dirty root `main` out of scope for scientific execution.
11. Keep raw row dumps and artifacts above roughly `10 MiB` out of git by
    default.

## Current Order

Completed forward order:

`F30_post_h54_useful_kernel_bridge_bundle` ->
`H55_post_h54_useful_kernel_reentry_packet` ->
`R60_origin_compiled_useful_kernel_carryover_gate` ->
`R61_origin_compiled_useful_kernel_value_gate` ->
`H56_post_r60_r61_useful_kernel_decision_packet`

Low-priority sidecar:

`P39_post_h54_successor_worktree_hygiene_sync`

## Current Rule

- `H56` is the current active docs-only packet.
- `H54` is preserved prior closeout and remains scientifically binding.
- `H55` is preserved prior useful-kernel reentry history.
- `F30` is the preserved planning bundle.
- `P39` is the current low-priority operational/docs wave.
- `R60` is the completed exact compiled useful-kernel carryover gate.
- `R61` is the completed value-negative comparator gate.
- `no_active_downstream_runtime_lane` is the current downstream lane state.
- `F27`, `R53`, and `R54` remain blocked.
- no merge back to `main` occurs during this wave.

## Execution Posture

- This wave is already closed at `H56`.
- No remaining runtime gate or docs-only packet is pending on this branch.
- If later work is authorized, it must start from a new planning packet rather
  than by extending this closed useful-kernel bridge lane.

## Control References

- `docs/publication_record/current_stage_driver.md`
- `docs/plans/2026-03-25-post-h54-useful-kernel-stopgo-design.md`
- `docs/milestones/F30_post_h54_useful_kernel_bridge_bundle/`
- `docs/milestones/H55_post_h54_useful_kernel_reentry_packet/`
- `docs/milestones/H56_post_r60_r61_useful_kernel_decision_packet/`
- `docs/milestones/P39_post_h54_successor_worktree_hygiene_sync/`
- `docs/milestones/R60_origin_compiled_useful_kernel_carryover_gate/`
- `docs/milestones/R61_origin_compiled_useful_kernel_value_gate/`
- `results/F30_post_h54_useful_kernel_bridge_bundle/summary.json`
- `results/H54_post_r58_r59_compiled_boundary_decision_packet/summary.json`
- `results/H55_post_h54_useful_kernel_reentry_packet/summary.json`
- `results/H56_post_r60_r61_useful_kernel_decision_packet/summary.json`
- `results/P39_post_h54_successor_worktree_hygiene_sync/summary.json`
- `results/R60_origin_compiled_useful_kernel_carryover_gate/summary.json`
- `results/R61_origin_compiled_useful_kernel_value_gate/summary.json`
- `results/H43_post_r44_useful_case_refreeze/summary.json`
