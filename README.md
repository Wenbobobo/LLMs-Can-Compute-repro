# llms-can-compute-repro

Careful reproduction of a narrow execution-substrate reading of Percepta's
_Can LLMs Be Computers?_ field note.

The repository does not target a general "LLMs are computers" claim. The
current closed question is narrower: append-only traces plus exact structured
retrieval support one bounded internal executor mechanism exactly, but the
accelerated fast path does not show bounded value over simpler transparent
baselines on the fixed five-row suite.

## Current Stage

As of `2026-03-25`, the current active packet is
`H52_post_r55_r56_r57_origin_mechanism_decision_packet`.

Current anchors:

- active docs-only packet:
  `H52_post_r55_r56_r57_origin_mechanism_decision_packet`
- preserved prior broader-route closeout:
  `H50_post_r51_r52_scope_decision_packet`
- preserved prior mechanism-reentry packet:
  `H51_post_h50_origin_mechanism_reentry_packet`
- current planning bundle:
  `F28_post_h50_origin_mechanism_reentry_bundle`
- current low-priority operational/docs wave:
  `P37_post_h50_narrow_executor_closeout_sync`
- completed exact retrieval-equivalence gate:
  `R55_origin_2d_hardmax_retrieval_equivalence_gate`
- completed exact trace-VM semantics gate:
  `R56_origin_append_only_trace_vm_semantics_gate`
- completed comparator gate:
  `R57_origin_accelerated_trace_vm_comparator_gate`
- current downstream scientific lane:
  `no_active_downstream_runtime_lane`
- preserved paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- preserved routing/refreeze packet:
  `H36_post_r40_bounded_scalar_family_refreeze`

`H50` remains scientifically binding on the broader post-`H49` bounded-value
question. `H52` closes the narrower mechanism-first lane as
`freeze_origin_mechanism_supported_without_fastpath_value`: landed `R55` and
`R56` remain exact mechanism evidence, while landed `R57` keeps all comparator
routes exact on `5/5` rows but shows `0/5` accelerated wins over both linear
and transparent external baselines. The repo therefore returns to no active
downstream runtime lane.

## Current Order

- completed mainline:
  `F28 -> H51 -> R55 -> R56 -> R57 -> H52`
- sidecar:
  `P37`

## Current Scope

The closed wave is limited to:

1. landed exact `R55` retrieval-equivalence evidence;
2. landed exact `R56` append-only trace-VM semantics evidence;
3. landed negative `R57` fast-path comparator evidence; and
4. landed docs-only `H52` mechanism closeout.

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
- `results/H51_post_h50_origin_mechanism_reentry_packet/summary.json`
- `results/R55_origin_2d_hardmax_retrieval_equivalence_gate/summary.json`
- `results/R56_origin_append_only_trace_vm_semantics_gate/summary.json`
- `results/R57_origin_accelerated_trace_vm_comparator_gate/summary.json`
- `results/H52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json`

Older milestone and plan inventories remain in the repository as historical
records. When historical prose conflicts with current routing, trust the files
above.
