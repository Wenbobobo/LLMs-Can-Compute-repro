# Active Wave Plan

## Current Wave

Current scientific/control stack:

- current active docs-only decision packet:
  `H51_post_h50_origin_mechanism_reentry_packet`;
- preserved prior docs-only closeout:
  `H50_post_r51_r52_scope_decision_packet`;
- preserved prior paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`;
- preserved active routing/refreeze packet:
  `H36_post_r40_bounded_scalar_family_refreeze`;
- current planning bundle:
  `F28_post_h50_origin_mechanism_reentry_bundle`;
- current low-priority operational/docs wave:
  `P37_post_h50_narrow_executor_closeout_sync`;
- current downstream scientific lane:
  `R55_origin_2d_hardmax_retrieval_equivalence_gate`;
- fixed later mechanism sequence:
  `R56_origin_append_only_trace_vm_semantics_gate` ->
  `R57_origin_accelerated_trace_vm_comparator_gate` ->
  `H52_post_r55_r56_r57_origin_mechanism_decision_packet`;
- blocked future storage:
  `F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle`,
  `R53_origin_transformed_executor_entry_gate`, and
  `R54_origin_trainable_executor_comparator_gate`.

Immediate active wave:

`F28_post_h50_origin_mechanism_reentry_bundle` is now the current planning
bundle. It preserves negative `H50`, rewrites the active claim surface around
the narrower mechanism chain, fixes `H51` as the only follow-up packet, fixes
`R55` as the only next runtime candidate, and keeps `R56/R57/H52` as the only
later exact sequence.

`H51_post_h50_origin_mechanism_reentry_packet` is now the current active
docs-only decision packet. It selects
`authorize_origin_mechanism_reentry_through_r55_first`, keeps `H50` visible
as the preserved prior broader-route closeout, preserves `H43` as the
paper-grade endpoint, and does not reactivate `F27`.

`P37_post_h50_narrow_executor_closeout_sync` is now the current low-priority
operational/docs wave. It records the clean control worktree, descendant
execution worktrees, out-of-git policy for row dumps and artifacts above
roughly `10 MiB`, and explicit no-merge posture for this wave.

## Immediate Objectives

1. Preserve `H50` as a landed broader-route bounded-value falsifier.
2. Preserve `H43` as the paper-grade endpoint.
3. Preserve `H36` as the routing/refreeze packet underneath the current stack.
4. Keep `R55` as the only next runtime candidate.
5. Keep `R56` and `R57` conditional on positive exact earlier gates only.
6. Keep `H52` as the only saved closeout packet for this mechanism lane.
7. Keep `F27`, `R53`, and `R54` blocked.
8. Keep dirty root `main` out of scope for scientific execution.
9. Keep raw row dumps and artifacts above roughly `10 MiB` out of git by
   default.
10. Prefer exact equivalence and clear falsifiers over broader demos.

## Current Order

Immediate forward order:

`F28_post_h50_origin_mechanism_reentry_bundle` ->
`H51_post_h50_origin_mechanism_reentry_packet` ->
`R55_origin_2d_hardmax_retrieval_equivalence_gate` ->
`R56_origin_append_only_trace_vm_semantics_gate` ->
`R57_origin_accelerated_trace_vm_comparator_gate` ->
`H52_post_r55_r56_r57_origin_mechanism_decision_packet`

Low-priority sidecar:

`P37_post_h50_narrow_executor_closeout_sync`

## Current Rule

- `H51` is the current active docs-only packet.
- `H50` is preserved prior closeout and remains scientifically binding.
- `F28` is the current planning bundle.
- `P37` is the current low-priority operational/docs wave.
- `R55` is the only next runtime candidate.
- `R56` and `R57` remain future gates only.
- `H52` remains the only saved closeout packet for this lane.
- `F27`, `R53`, and `R54` remain blocked.
- no merge back to `main` occurs during this wave.

## Control References

- `docs/publication_record/current_stage_driver.md`
- `docs/plans/2026-03-25-post-h50-origin-mechanism-reentry-master-plan.md`
- `docs/milestones/F28_post_h50_origin_mechanism_reentry_bundle/`
- `docs/milestones/H51_post_h50_origin_mechanism_reentry_packet/`
- `docs/milestones/P37_post_h50_narrow_executor_closeout_sync/`
- `docs/milestones/R55_origin_2d_hardmax_retrieval_equivalence_gate/`
- `docs/milestones/R56_origin_append_only_trace_vm_semantics_gate/`
- `docs/milestones/R57_origin_accelerated_trace_vm_comparator_gate/`
- `docs/milestones/H52_post_r55_r56_r57_origin_mechanism_decision_packet/`
- `results/H50_post_r51_r52_scope_decision_packet/summary.json`
- `results/F28_post_h50_origin_mechanism_reentry_bundle/summary.json`
- `results/H51_post_h50_origin_mechanism_reentry_packet/summary.json`
- `results/P37_post_h50_narrow_executor_closeout_sync/summary.json`
