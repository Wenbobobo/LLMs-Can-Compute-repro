# llms-can-compute-repro

Careful reproduction of a narrow execution-substrate reading of Percepta's
_Can LLMs Be Computers?_ field note.

The repository does not target a general "LLMs are computers" claim. The
current question is narrower: whether append-only traces plus exact structured
retrieval can support one bounded internal executor under a transparent
reference contract.

## Current Stage

As of `2026-03-25`, the current active packet is
`H51_post_h50_origin_mechanism_reentry_packet`.

Current anchors:

- active docs-only packet:
  `H51_post_h50_origin_mechanism_reentry_packet`
- preserved prior broader-route closeout:
  `H50_post_r51_r52_scope_decision_packet`
- current planning bundle:
  `F28_post_h50_origin_mechanism_reentry_bundle`
- current low-priority operational/docs wave:
  `P37_post_h50_narrow_executor_closeout_sync`
- completed current exact mechanism gate:
  `R55_origin_2d_hardmax_retrieval_equivalence_gate`
- next required runtime candidate:
  `R56_origin_append_only_trace_vm_semantics_gate`
- preserved paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- preserved routing/refreeze packet:
  `H36_post_r40_bounded_scalar_family_refreeze`

`H50` remains scientifically binding on the broader post-`H49` bounded-value
question: positive `R51` plus negative `R52` still close that lane as
`stop_as_exact_without_system_value`. `H51` does not overturn that result. It
reopens only a narrower mechanism-first lane, and landed `R55` now keeps that
lane open only as far as `R56`.

## Current Order

- mainline:
  `F28 -> H51 -> R55 -> R56 -> R57 -> H52`
- sidecar:
  `P37`

`R55_origin_2d_hardmax_retrieval_equivalence_gate` has landed as completed
exact mechanism evidence with `5/5` exact tasks and `45/45` exact
maximizer-row checks. `R56_origin_append_only_trace_vm_semantics_gate` is now
the only next runtime candidate. `R57` and `H52` remain fixed later stages
and open only after positive earlier gates.

## Current Scope

The active wave is limited to:

1. landed exact `R55` retrieval-equivalence evidence;
2. exact append-only trace-VM semantics through `R56`; and
3. bounded comparator value for an accelerated trace-VM path through `R57`
   only after positive `R56`.

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
- `docs/plans/2026-03-25-post-h50-origin-mechanism-reentry-master-plan.md`
- `results/H50_post_r51_r52_scope_decision_packet/summary.json`
- `results/F28_post_h50_origin_mechanism_reentry_bundle/summary.json`
- `results/H51_post_h50_origin_mechanism_reentry_packet/summary.json`
- `results/P37_post_h50_narrow_executor_closeout_sync/summary.json`
- `results/R55_origin_2d_hardmax_retrieval_equivalence_gate/summary.json`

Older milestone and plan inventories remain in the repository as historical
records. When historical prose conflicts with current routing, trust the files
above.
