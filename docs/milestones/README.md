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

- `H52_post_r55_r56_r57_origin_mechanism_decision_packet/`
  current active docs-only packet
- `H51_post_h50_origin_mechanism_reentry_packet/`
  preserved prior mechanism-reentry packet
- `H50_post_r51_r52_scope_decision_packet/`
  preserved prior broader-route closeout
- `F28_post_h50_origin_mechanism_reentry_bundle/`
  current planning-only mechanism reentry bundle
- `P37_post_h50_narrow_executor_closeout_sync/`
  current low-priority operational/docs wave
- `R55_origin_2d_hardmax_retrieval_equivalence_gate/`
  completed exact retrieval-equivalence gate
- `R56_origin_append_only_trace_vm_semantics_gate/`
  completed exact trace-VM semantics gate
- `R57_origin_accelerated_trace_vm_comparator_gate/`
  completed comparator gate

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

- preserve negative `H50`
- keep `H52` as the current closeout
- keep the downstream scientific lane at `no_active_downstream_runtime_lane`
- do not reopen transformed or trainable entry by momentum
- keep dirty root `main` out of scientific execution

## Historical Note

Older milestone directories remain important evidence, but they are not the
current routing surface. When an old milestone says "current", read that as
"current at the time of that packet", not as the live repo state.
