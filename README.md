# llms-can-compute-repro

Careful reproduction of a narrow execution-substrate reading of Percepta's
_Can LLMs Be Computers?_ field note.

The repository still does not target a general "LLMs are computers" claim. The
current closed question is narrower: even when `sum_i32_buffer` and
`count_nonzero_i32_buffer` are executed as native append-only trace programs,
the accelerated internal executor still does not retain bounded value over
linear or plain external references.

## Current Stage

As of `2026-03-25`, the current active packet is
`H58_post_r62_origin_value_boundary_closeout_packet`.

Current anchors:

- active docs-only packet:
  `H58_post_r62_origin_value_boundary_closeout_packet`
- preserved prior docs-only closeout:
  `H56_post_r60_r61_useful_kernel_decision_packet`
- preserved prior authorization packet:
  `H57_post_h56_last_discriminator_authorization_packet`
- current planning bundle:
  `F31_post_h56_final_discriminating_value_boundary_bundle`
- current low-priority operational/docs wave:
  `P40_post_h56_successor_worktree_and_artifact_hygiene_sync`
- completed native value discriminator gate:
  `R62_origin_native_useful_kernel_value_discriminator_gate`
- current downstream scientific lane:
  `no_active_downstream_runtime_lane`
- preserved paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- preserved routing/refreeze packet:
  `H36_post_r40_bounded_scalar_family_refreeze`

`F31` fixed one final successor wave above `H56`. `H57` authorized exactly one
native useful-kernel value discriminator through `R62`. `R62` then landed
exact native execution on `4/4` declared rows across `2/2` kernels, but the
accelerated route was faster than linear on `0/2` longest kernel rows and did
not approach the external scalar comparator on either kernel. `H58` therefore
selects `stop_as_mechanism_supported_but_no_bounded_executor_value`.

## Current Order

- completed mainline:
  `F31 -> H57 -> R62 -> H58`
- sidecar:
  `P40`

## Execution Posture

There are no remaining runtime or docs-only execution tasks on this closed
wave. This branch is now a preserved closeout surface. The next meaningful
step is either a new explicit planning packet with a genuinely different cost
structure or a consolidation/closeout pass, not more executor-value probing by
momentum.

## Current Scope

The closed wave is limited to:

1. landed planning-only `F31` routing for one final discriminator wave;
2. landed docs-only `H57` authorization through `R62` only;
3. landed exact `R62` native useful-kernel comparator evidence on the fixed
   `sum/count` suite; and
4. landed docs-only `H58` closeout.

Still blocked:

- `F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle`
- `R53_origin_transformed_executor_entry_gate`
- `R54_origin_trainable_executor_comparator_gate`
- arbitrary `C`
- broad Wasm claims
- merge back to dirty root `main`

Raw row dumps and artifacts above roughly `10 MiB` stay out of git by default
on the active wave.

## Read First

- `docs/publication_record/current_stage_driver.md`
- `tmp/active_wave_plan.md`
- `docs/plans/2026-03-25-post-h56-last-discriminator-design.md`
- `results/F31_post_h56_final_discriminating_value_boundary_bundle/summary.json`
- `results/H57_post_h56_last_discriminator_authorization_packet/summary.json`
- `results/R62_origin_native_useful_kernel_value_discriminator_gate/summary.json`
- `results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json`
- `results/P40_post_h56_successor_worktree_and_artifact_hygiene_sync/summary.json`
- `results/H56_post_r60_r61_useful_kernel_decision_packet/summary.json`
- `results/H43_post_r44_useful_case_refreeze/summary.json`

Older milestone and plan inventories remain in the repository as historical
records. When historical prose conflicts with current routing, trust the files
above.
