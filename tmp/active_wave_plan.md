# Active Wave Plan

## Current Wave

Current scientific/control stack:

- current active docs-only decision packet:
  `H52_post_r55_r56_r57_origin_mechanism_decision_packet`;
- preserved prior broader-route closeout:
  `H50_post_r51_r52_scope_decision_packet`;
- preserved prior mechanism-reentry packet:
  `H51_post_h50_origin_mechanism_reentry_packet`;
- preserved prior paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`;
- preserved active routing/refreeze packet:
  `H36_post_r40_bounded_scalar_family_refreeze`;
- current planning bundle:
  `F28_post_h50_origin_mechanism_reentry_bundle`;
- current low-priority operational/docs wave:
  `P37_post_h50_narrow_executor_closeout_sync`;
- completed exact retrieval-equivalence gate:
  `R55_origin_2d_hardmax_retrieval_equivalence_gate`;
- completed exact trace-VM semantics gate:
  `R56_origin_append_only_trace_vm_semantics_gate`;
- completed comparator gate:
  `R57_origin_accelerated_trace_vm_comparator_gate`;
- current downstream scientific lane:
  `no_active_downstream_runtime_lane`;
- blocked future storage:
  `F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle`,
  `R53_origin_transformed_executor_entry_gate`, and
  `R54_origin_trainable_executor_comparator_gate`.

Immediate active wave:

`F28_post_h50_origin_mechanism_reentry_bundle` remains the preserved planning
bundle that fixed `R55 -> R56 -> R57 -> H52` as the only admissible order.

`H51_post_h50_origin_mechanism_reentry_packet` remains the preserved prior
mechanism-reentry packet. It selected
`authorize_origin_mechanism_reentry_through_r55_first` and kept `H50`
visible rather than overturning it.

`P37_post_h50_narrow_executor_closeout_sync` remains the current low-priority
operational/docs wave. It keeps the clean control worktree, descendant
execution worktrees, out-of-git policy for row dumps and artifacts above
roughly `10 MiB`, and explicit no-merge posture for this wave.

`R55_origin_2d_hardmax_retrieval_equivalence_gate` is completed with
`retrieval_equivalence_supported_exactly` on `5/5` fixed tasks and `45/45`
exact maximizer-row identity observations.

`R56_origin_append_only_trace_vm_semantics_gate` is completed with
`trace_vm_semantics_supported_exactly` on `5/5` fixed rows and `288`
exported transition rows.

`R57_origin_accelerated_trace_vm_comparator_gate` is completed with
`accelerated_trace_vm_lacks_bounded_value`: all comparator routes remain exact
on `5/5` rows, but accelerated beats neither linear nor the transparent
external interpreter on any row.

`H52_post_r55_r56_r57_origin_mechanism_decision_packet` is now the current
active packet and selects
`freeze_origin_mechanism_supported_without_fastpath_value`.

## Immediate Objectives

1. Preserve `H50` as a landed broader-route bounded-value falsifier.
2. Preserve `H43` as the paper-grade endpoint.
3. Preserve `H36` as the routing/refreeze packet underneath the current stack.
4. Preserve `R55` as completed exact retrieval-equivalence evidence only.
5. Preserve `R56` as completed exact trace-VM semantics evidence only.
6. Preserve `R57` as completed negative fast-path comparator evidence.
7. Keep `H52` as the current docs-only closeout packet.
8. Keep the downstream scientific lane at `no_active_downstream_runtime_lane`.
9. Keep `F27`, `R53`, and `R54` blocked.
10. Keep dirty root `main` out of scope for scientific execution.
11. Keep raw row dumps and artifacts above roughly `10 MiB` out of git by
   default.

## Current Order

Completed forward order:

`F28_post_h50_origin_mechanism_reentry_bundle` ->
`H51_post_h50_origin_mechanism_reentry_packet` ->
`R55_origin_2d_hardmax_retrieval_equivalence_gate` ->
`R56_origin_append_only_trace_vm_semantics_gate` ->
`R57_origin_accelerated_trace_vm_comparator_gate` ->
`H52_post_r55_r56_r57_origin_mechanism_decision_packet`

Low-priority sidecar:

`P37_post_h50_narrow_executor_closeout_sync`

## Current Rule

- `H52` is the current active docs-only packet.
- `H50` is preserved prior closeout and remains scientifically binding.
- `H51` is preserved prior mechanism-reentry history.
- `F28` is the preserved planning bundle.
- `P37` is the current low-priority operational/docs wave.
- `R55` is the completed exact retrieval-equivalence gate.
- `R56` is the completed exact trace-VM semantics gate.
- `R57` is the completed comparator gate.
- `no_active_downstream_runtime_lane` is the current downstream lane state.
- `F27`, `R53`, and `R54` remain blocked.
- no merge back to `main` occurs during this wave.

## Control References

- `docs/publication_record/current_stage_driver.md`
- `docs/plans/2026-03-25-post-h50-origin-mechanism-reentry-master-plan.md`
- `docs/milestones/F28_post_h50_origin_mechanism_reentry_bundle/`
- `docs/milestones/H51_post_h50_origin_mechanism_reentry_packet/`
- `docs/milestones/H52_post_r55_r56_r57_origin_mechanism_decision_packet/`
- `docs/milestones/P37_post_h50_narrow_executor_closeout_sync/`
- `docs/milestones/R55_origin_2d_hardmax_retrieval_equivalence_gate/`
- `docs/milestones/R56_origin_append_only_trace_vm_semantics_gate/`
- `docs/milestones/R57_origin_accelerated_trace_vm_comparator_gate/`
- `results/H50_post_r51_r52_scope_decision_packet/summary.json`
- `results/F28_post_h50_origin_mechanism_reentry_bundle/summary.json`
- `results/H51_post_h50_origin_mechanism_reentry_packet/summary.json`
- `results/H52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json`
- `results/P37_post_h50_narrow_executor_closeout_sync/summary.json`
- `results/R55_origin_2d_hardmax_retrieval_equivalence_gate/summary.json`
- `results/R56_origin_append_only_trace_vm_semantics_gate/summary.json`
- `results/R57_origin_accelerated_trace_vm_comparator_gate/summary.json`
