# llms-can-compute-repro

Careful reproduction of a narrow execution-substrate reading of Percepta's
_Can LLMs Be Computers?_ field note.

The repository still does not target a general "LLMs are computers" claim. The
current closed question is narrower: the current compiled-boundary route can
carry one minimal preserved useful-kernel pair exactly, but that route still
does not retain bounded value over simpler baselines once compiler/lowering
overhead is counted.

## Current Stage

As of `2026-03-25`, the current active packet is
`H56_post_r60_r61_useful_kernel_decision_packet`.

Current anchors:

- active docs-only packet:
  `H56_post_r60_r61_useful_kernel_decision_packet`
- preserved prior docs-only closeout:
  `H54_post_r58_r59_compiled_boundary_decision_packet`
- preserved prior useful-kernel reentry packet:
  `H55_post_h54_useful_kernel_reentry_packet`
- current planning bundle:
  `F30_post_h54_useful_kernel_bridge_bundle`
- current low-priority operational/docs wave:
  `P39_post_h54_successor_worktree_hygiene_sync`
- completed useful-kernel carryover gate:
  `R60_origin_compiled_useful_kernel_carryover_gate`
- completed value gate:
  `R61_origin_compiled_useful_kernel_value_gate`
- current downstream scientific lane:
  `no_active_downstream_runtime_lane`
- preserved paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- preserved routing/refreeze packet:
  `H36_post_r40_bounded_scalar_family_refreeze`

`F30_post_h54_useful_kernel_bridge_bundle` fixed one narrow stop/go wave above
`H54`. `H55` authorized only the minimal useful-kernel pair
`sum_i32_buffer` and `count_nonzero_i32_buffer` through `R60`. `R60` then
landed exact carryover on `5/5` preserved variants with exact source/spec,
source/lowered, canonical/compiled, and linear/accelerated internal execution
parity. `R61` kept all declared comparators exact on those same `5/5` rows,
but the accelerated internal route was slower than linear, transparent source,
transparent lowered execution, and a plain external reference runtime once
compiler/lowering overhead was counted. `H56` therefore selects
`freeze_minimal_useful_kernel_bridge_supported_without_bounded_value`.

## Current Order

- completed mainline:
  `F30 -> H55 -> R60 -> R61 -> H56`
- sidecar:
  `P39`

## Execution Posture

There are no remaining runtime or docs-only execution tasks on this closed
wave. This branch is now a preserved closeout surface. The next meaningful
step is a new explicit planning packet in a successor worktree, not more
compiled useful-kernel execution on this branch.

## Current Scope

The closed wave is limited to:

1. landed planning-only `F30` routing for one compiled useful-kernel stop/go
   wave;
2. landed docs-only `H55` authorization through `R60` only;
3. landed exact `R60` useful-kernel carryover evidence on the fixed
   `sum/count` suite;
4. landed `R61` value-negative comparator evidence on the exact `R60` rows;
   and
5. landed docs-only `H56` closeout.

Still blocked:

- `F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle`
- `R53_origin_transformed_executor_entry_gate`
- `R54_origin_trainable_executor_comparator_gate`
- `histogram16_u8` carryover on this first compiled useful-kernel wave
- arbitrary `C`
- broad Wasm claims
- merge back to dirty root `main`

Raw row dumps and artifacts above roughly `10 MiB` stay out of git by default
on the active wave.

## Read First

- `docs/publication_record/current_stage_driver.md`
- `tmp/active_wave_plan.md`
- `docs/plans/2026-03-25-post-h54-useful-kernel-stopgo-design.md`
- `results/F30_post_h54_useful_kernel_bridge_bundle/summary.json`
- `results/H54_post_r58_r59_compiled_boundary_decision_packet/summary.json`
- `results/H55_post_h54_useful_kernel_reentry_packet/summary.json`
- `results/R60_origin_compiled_useful_kernel_carryover_gate/summary.json`
- `results/R61_origin_compiled_useful_kernel_value_gate/summary.json`
- `results/H56_post_r60_r61_useful_kernel_decision_packet/summary.json`
- `results/P39_post_h54_successor_worktree_hygiene_sync/summary.json`
- `results/H43_post_r44_useful_case_refreeze/summary.json`

Older milestone and plan inventories remain in the repository as historical
records. When historical prose conflicts with current routing, trust the files
above.
