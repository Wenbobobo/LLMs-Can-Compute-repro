# Milestones Index

This directory stores milestone-local docs, result digests, and planning
bundles. Read current control surfaces first; many older milestone files are
historical and may use then-current wording.

## Reading Order

1. `../publication_record/current_stage_driver.md`
2. `../../tmp/active_wave_plan.md`
3. the active milestone `README.md` / `status.md`
4. the matching `results/<lane>/summary.json`

## Current Top Of Stack

- `H56_post_r60_r61_useful_kernel_decision_packet/`
  current active docs-only packet
- `H55_post_h54_useful_kernel_reentry_packet/`
  preserved prior useful-kernel reentry packet
- `H54_post_r58_r59_compiled_boundary_decision_packet/`
  preserved prior compiled-boundary closeout
- `F30_post_h54_useful_kernel_bridge_bundle/`
  current planning-only useful-kernel stop/go bundle
- `P39_post_h54_successor_worktree_hygiene_sync/`
  current low-priority operational/docs wave
- `R60_origin_compiled_useful_kernel_carryover_gate/`
  completed exact compiled useful-kernel carryover gate
- `R61_origin_compiled_useful_kernel_value_gate/`
  completed value gate

## Preserved Recent Upstream Wave

- `F29_post_h52_restricted_compiled_boundary_bundle/`
  preserved prior compiled-boundary planning bundle
- `H53_post_h52_compiled_boundary_reentry_packet/`
  preserved prior compiled-boundary reentry packet
- `R58_origin_restricted_stack_bytecode_lowering_contract_gate/`
  preserved prior exact compiled-boundary lowering gate
- `R59_origin_compiled_trace_vm_execution_gate/`
  preserved prior exact compiled-boundary execution gate
- `H52_post_r55_r56_r57_origin_mechanism_decision_packet/`
  preserved prior mechanism closeout

## Preserved Anchors

- `H43_post_r44_useful_case_refreeze/`
  current paper-grade endpoint
- `H36_post_r40_bounded_scalar_family_refreeze/`
  preserved routing/refreeze packet under the current stack
- `F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle/`
  blocked future planning storage only
- `R53_origin_transformed_executor_entry_gate/`
  blocked future transformed gate
- `R54_origin_trainable_executor_comparator_gate/`
  blocked future trainable comparator gate

## Current Rule

- preserve negative `H54` on bounded fast-path/system value
- keep `H56` as the current closeout
- keep the downstream scientific lane at `no_active_downstream_runtime_lane`
- do not reopen transformed or trainable entry by momentum
- keep dirty root `main` out of scientific execution

## Historical Note

Older milestone directories remain important evidence, but they are not the
current routing surface. When an old milestone says "current", read that as
"current at the time of that packet", not as the live repo state.
