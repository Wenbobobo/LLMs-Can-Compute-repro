# Current Stage Driver

## Active Driver

The current active stage is:

- `H52_post_r55_r56_r57_origin_mechanism_decision_packet`

The preserved prior docs-only closeout is:

- `H50_post_r51_r52_scope_decision_packet`

The preserved prior mechanism-reentry packet is:

- `H51_post_h50_origin_mechanism_reentry_packet`

The current planning bundle is:

- `F28_post_h50_origin_mechanism_reentry_bundle`

The current low-priority operational/docs wave is:

- `P37_post_h50_narrow_executor_closeout_sync`

The preserved paper-grade endpoint is:

- `H43_post_r44_useful_case_refreeze`

The preserved active routing/refreeze packet is:

- `H36_post_r40_bounded_scalar_family_refreeze`

The completed exact mechanism gates under the closed mechanism lane are:

- `R55_origin_2d_hardmax_retrieval_equivalence_gate`
- `R56_origin_append_only_trace_vm_semantics_gate`

The completed comparator gate under the closed mechanism lane is:

- `R57_origin_accelerated_trace_vm_comparator_gate`

The current downstream scientific lane is:

- `no_active_downstream_runtime_lane`

The blocked future executor-entry bundle remains:

- `F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle`

The blocked future transformed gate remains:

- `R53_origin_transformed_executor_entry_gate`

The blocked future trainable gate remains:

- `R54_origin_trainable_executor_comparator_gate`

## Current Machine-State Meaning

- `H50` remains a landed negative closeout on the broader post-`H49`
  internal-route value question. It is not overturned by the narrower
  mechanism lane.
- `F28` remains the preserved planning bundle that fixed
  `R55 -> R56 -> R57 -> H52` as the only admissible mechanism-first sequence.
- `H51` remains the preserved prior mechanism-reentry packet that authorized
  reentry through `R55` only.
- `R55` is completed exact mechanism evidence with
  `retrieval_equivalence_supported_exactly` on `5/5` fixed tasks and
  `45/45` exact maximizer-row identity observations.
- `R56` is completed exact trace-VM semantics evidence with
  `trace_vm_semantics_supported_exactly` on `5/5` fixed rows and `288`
  exported transition rows.
- `R57` is completed comparator evidence with
  `accelerated_trace_vm_lacks_bounded_value`: all three comparator routes stay
  exact on `5/5` rows, but accelerated beats linear on `0/5` rows and beats
  the transparent external interpreter on `0/5` rows.
- `H52` is now the current active docs-only packet and selects
  `freeze_origin_mechanism_supported_without_fastpath_value`.
- `no_active_downstream_runtime_lane` is restored as the current downstream
  scientific lane.
- `H43` remains the current paper-grade endpoint and `H36` remains the
  routing/refreeze packet underneath the current stack.
- Completed exact substrate support underneath the mechanism reentry remains
  `R42`, `R43`, `R44`, `R46`, `R47`, `R49`, `R50`, and `R51`, while `R52`
  remains the broader-route value falsifier, `R55/R56` remain the narrow exact
  mechanism evidence, and `R45` remains coequal non-substitutive model
  evidence.
- Dirty root `main` remains quarantined and `merge_executed = false` remains
  explicit through `P27` and `P37`.
- General LLM-computer claims, arbitrary `C`, broad Wasm, transformed entry,
  and trainable entry remain blocked.

## Current Forward Order

- completed mainline: `F28 -> H51 -> R55 -> R56 -> R57 -> H52`
- sidecar: `P37`
- blocked by default: `F27`, `R53`, and `R54`

## Standing Gates

- `H52_post_r55_r56_r57_origin_mechanism_decision_packet` is the current
  active docs-only decision packet.
- `H50_post_r51_r52_scope_decision_packet` is the preserved prior broader-route
  closeout packet and remains scientifically binding on the post-`H49`
  bounded-value question.
- `H51_post_h50_origin_mechanism_reentry_packet` is the preserved prior
  mechanism-reentry packet for the now-closed lane.
- `F28_post_h50_origin_mechanism_reentry_bundle` is the current preserved
  planning-only bundle fixing the mechanism-first order.
- `P37_post_h50_narrow_executor_closeout_sync` is the current low-priority
  operational/docs wave.
- `R55_origin_2d_hardmax_retrieval_equivalence_gate` is the completed current
  exact retrieval gate.
- `R56_origin_append_only_trace_vm_semantics_gate` is the completed current
  exact trace-VM semantics gate.
- `R57_origin_accelerated_trace_vm_comparator_gate` is the completed current
  comparator gate.
- `no_active_downstream_runtime_lane` is the current downstream lane state.
- `F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle`,
  `R53_origin_transformed_executor_entry_gate`, and
  `R54_origin_trainable_executor_comparator_gate` remain blocked and inactive.
- `R41_origin_runtime_relevance_threat_stress_audit` remains deferred.
- `R42_origin_append_only_memory_retrieval_contract_gate`,
  `R43_origin_bounded_memory_small_vm_execution_gate`,
  `R44_origin_restricted_wasm_useful_case_execution_gate`,
  `R45_origin_dual_mode_model_mainline_gate`,
  `R46_origin_useful_case_surface_generalization_gate`,
  `R47_origin_restricted_frontend_translation_gate`,
  `R48_origin_dual_mode_useful_case_model_gate`,
  `R49_origin_useful_case_numeric_scaling_gate`,
  `R50_origin_restricted_tinyc_lowering_gate`,
  `R51_origin_memory_control_surface_sufficiency_gate`, and
  `R52_origin_internal_vs_external_executor_value_gate` remain completed
  upstream evidence or comparator gates underneath the closed mechanism lane.

## Control References

- `results/H50_post_r51_r52_scope_decision_packet/summary.json`
- `results/F28_post_h50_origin_mechanism_reentry_bundle/summary.json`
- `results/H51_post_h50_origin_mechanism_reentry_packet/summary.json`
- `results/H52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json`
- `results/P37_post_h50_narrow_executor_closeout_sync/summary.json`
- `results/R55_origin_2d_hardmax_retrieval_equivalence_gate/summary.json`
- `results/R56_origin_append_only_trace_vm_semantics_gate/summary.json`
- `results/R57_origin_accelerated_trace_vm_comparator_gate/summary.json`
- `results/H43_post_r44_useful_case_refreeze/summary.json`
- `results/R51_origin_memory_control_surface_sufficiency_gate/summary.json`
- `results/R52_origin_internal_vs_external_executor_value_gate/summary.json`
- `docs/plans/2026-03-25-post-h50-origin-mechanism-reentry-master-plan.md`
- `docs/milestones/F28_post_h50_origin_mechanism_reentry_bundle/`
- `docs/milestones/H51_post_h50_origin_mechanism_reentry_packet/`
- `docs/milestones/H52_post_r55_r56_r57_origin_mechanism_decision_packet/`
- `docs/milestones/P37_post_h50_narrow_executor_closeout_sync/`
- `docs/milestones/R55_origin_2d_hardmax_retrieval_equivalence_gate/`
- `docs/milestones/R56_origin_append_only_trace_vm_semantics_gate/`
- `docs/milestones/R57_origin_accelerated_trace_vm_comparator_gate/`
- `tmp/active_wave_plan.md`

## Historical Reference

The earlier `H27 -> H50` stack remains preserved as landed evidence and
control history. The `F28/H51` pair does not erase `H50`; it opened one
explicit narrower mechanism-only reentry route above the preserved
`H43/H36` Origin-core stack, and `H52` now closes that route without
reopening a downstream runtime lane.
