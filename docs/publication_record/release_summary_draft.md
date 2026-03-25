# Release Summary Draft

## Narrow target

This repository reproduces a narrow execution-substrate claim rather than a
broad “LLMs are computers” thesis. On the current validated scope, the project
supports three linked statements: deterministic computation can be encoded as an
append-only execution trace; exact latest-write retrieval over that trace can
be implemented with structured 2D hard-max retrieval; and those primitives are
enough for a small exact executor on the active Origin-core bundle. The earlier
tiny typed-bytecode `D0` endpoint is now a preserved historical boundary rather
than the active mainline.

## Current gate chain

The current execution-facing chain is now
`H27_refreeze_after_r32_r33_same_endpoint_decision` ->
`H28_post_h27_origin_core_reanchor_packet` ->
`R34_origin_retrieval_primitive_contract_gate` ->
`R35_origin_append_only_stack_vm_execution_gate` ->
`H29_refreeze_after_r34_r35_origin_core_gate` ->
`R36_origin_long_horizon_precision_scaling_gate` ->
`R37_origin_compiler_boundary_gate` ->
`H30_post_r36_r37_scope_decision_packet` ->
`H31_post_h30_later_explicit_boundary_decision_packet` ->
`R38_origin_compiler_control_surface_extension_gate` ->
`H32_post_r38_compiled_boundary_refreeze` ->
`H33_post_h32_conditional_next_question_packet` ->
`R39_origin_compiler_control_surface_dependency_audit` ->
`H34_post_r39_later_explicit_scope_decision_packet` ->
`H35_post_p23_bounded_scalar_family_runtime_decision_packet` ->
`R40_origin_bounded_scalar_locals_and_flags_gate` ->
`H36_post_r40_bounded_scalar_family_refreeze` ->
`P25_post_h36_clean_promotion_prep` ->
`F15_post_h36_origin_goal_reanchor_bundle` ->
`H37_post_h36_runtime_relevance_decision_packet` ->
`F16_post_h37_r41_candidate_isolation_bundle` ->
`H38_post_f16_runtime_relevance_reopen_decision_packet` ->
`P26_post_h37_promotion_and_artifact_hygiene_audit` ->
`F17_post_h38_same_substrate_exit_criteria_bundle` ->
`F18_post_h38_origin_core_long_arc_bundle` ->
`F19_post_f18_restricted_wasm_useful_case_roadmap` ->
`H40_post_h38_semantic_boundary_activation_packet` ->
`R42_origin_append_only_memory_retrieval_contract_gate` ->
`F20_post_r42_dual_mode_model_mainline_bundle` ->
`H41_post_r42_aggressive_long_arc_decision_packet` ->
`P27_post_h41_clean_promotion_and_explicit_merge_packet` ->
`R43_origin_bounded_memory_small_vm_execution_gate` ->
`R45_origin_dual_mode_model_mainline_gate` ->
`H42_post_r43_route_selection_packet` ->
`R44_origin_restricted_wasm_useful_case_execution_gate` ->
`H43_post_r44_useful_case_refreeze` ->
`H50_post_r51_r52_scope_decision_packet` ->
`F28_post_h50_origin_mechanism_reentry_bundle` ->
`H51_post_h50_origin_mechanism_reentry_packet` ->
`R55_origin_2d_hardmax_retrieval_equivalence_gate` ->
`R56_origin_append_only_trace_vm_semantics_gate` ->
`R57_origin_accelerated_trace_vm_comparator_gate` ->
`H52_post_r55_r56_r57_origin_mechanism_decision_packet` ->
`F29_post_h52_restricted_compiled_boundary_bundle` ->
`H53_post_h52_compiled_boundary_reentry_packet` ->
`R58_origin_restricted_stack_bytecode_lowering_contract_gate` ->
`R59_origin_compiled_trace_vm_execution_gate` ->
`H54_post_r58_r59_compiled_boundary_decision_packet` ->
`F30_post_h54_useful_kernel_bridge_bundle` ->
`H55_post_h54_useful_kernel_reentry_packet` ->
`R60_origin_compiled_useful_kernel_carryover_gate` ->
`R61_origin_compiled_useful_kernel_value_gate` ->
`H56_post_r60_r61_useful_kernel_decision_packet` ->
`F31_post_h56_final_discriminating_value_boundary_bundle` ->
`H57_post_h56_last_discriminator_authorization_packet` ->
`R62_origin_native_useful_kernel_value_discriminator_gate` ->
`H58_post_r62_origin_value_boundary_closeout_packet`.
Earlier paper/release controls such as `P3`, `R1`, `R2`, `M7`, and `P4`
remain relevant guardrails, but they are no longer the current
science-routing story by themselves.

## Current endpoint and non-goals

The current live control state is the post-`R62` closeout selected by `H58`:
the append-only executor stack remains mechanistically supported on narrow
admitted surfaces, but bounded executor value remains negative even after the
runtime is collapsed down to native useful-kernel trace programs. `H58`
preserves `H56` as the prior compiled useful-kernel closeout, preserves
`H54` as the prior compiled-boundary closeout, preserves `H52` as the prior
mechanism closeout, and does not promote the current route into a broader
fast-path or systems-value claim. `H43` remains the paper-grade endpoint for
the useful-case semantic-boundary story; `H58` does not widen that endpoint,
it only closes the final admitted executor-value discriminator lane above it.
The earlier tiny typed-bytecode `D0` endpoint remains a preserved first
compiled boundary and should not be read as the current bridge to arbitrary
`C`, general LLM computation, or broader demo-first claims. Those broader
readings remain explicitly unsupported on both the paper-grade and the current
control scope.

## Current paper-facing follow-up

The current frozen scope has a locked submission-candidate bundle. `P8` closed
the manuscript, appendix, and ledger lock on the same frozen endpoint. `H2`
remains the standing bundle-lock and release-hygiene gate. `P9` keeps outward
wording downstream of the locked bundle. The completed `H8/R6/R7/H9` packet
now sits as the direct same-endpoint baseline: `R6` keeps `24/24`
fixed-multiplier rows admitted, while `R7` preserves the full `8`-family
exact-admitted surface but profiles only the top `4` heaviest representatives,
stopping at `stop_decode_gain_not_material` with `0.973x` median
accelerated-vs-linear speedup and a `1980.3x` accelerated-vs-lowered ratio.
The older `H6/R3/R4/(inactive R5)/H7` packet remains the deeper
exactness/mechanism baseline on the same endpoint. `H10/H11/R8/R9/R10/H12` is
now the latest completed same-endpoint follow-up packet rather than the active
science lane. `H10` reconciles the prior packet. `H11` replaces the driver.
`R8` opens a higher retrieval-pressure gate. `R9` keeps real-trace precision
companion-only. `R10` attributes same-endpoint costs. `H12` completes the
refreeze on the same endpoint. Within that packet, `R8` now closes with `4/4`
admitted exact rows plus a bounded `2/2` decode-parity probe match, `R9` now
closes with `4/4` screened streams still `effective_here`, and `R10` now
closes with retrieval dominating representative admitted rows while median
exact-versus-lowered ratio stays around `2429.1x`. `H13/V1` is now the
preserved governance/runtime handoff rather than the active science lane. `V1`
records that `pytest --collect-only -q` succeeds on the current suite, and the
bounded top-`6` per-file timing follow-up classifies full `pytest -q` as
healthy but multi-minute rather than discovery-broken. The preserved prior
same-endpoint scientific state inside the earlier post-`P9` chain is
`H23_refreeze_after_r26_r27_r28`, which refreezes the
bounded post-`H21` packet
`H22_post_h21_boundary_reopen_and_dual_track_lock` ->
`R26_d0_boundary_localization_execution_gate` +
`R28_d0_trace_retrieval_contract_audit` ->
conditional `R27_d0_boundary_localization_extension_gate` ->
`H23_refreeze_after_r26_r27_r28` on top of the preserved
`H20_post_h19_mainline_reentry_and_hygiene_split` ->
`R22_d0_true_boundary_localization_gate` ->
`R23_d0_same_endpoint_systems_overturn_gate` ->
`H21_refreeze_after_r22_r23` packet and the earlier preserved
`H18_post_h17_mainline_reopen_and_scope_lock` ->
`R19_d0_pointer_like_surface_generalization_gate` ->
`R20_d0_runtime_mechanism_ablation_matrix` ->
`R21_d0_exact_executor_boundary_break_map` ->
`H19_refreeze_and_next_scope_decision` packet. `H23` keeps the claim
partition explicit: same-endpoint runtime generalization and bounded mechanism
support remain supported on current evidence, `R22`, `R26`, and `R27` still do
not localize a true executor failure, `R28` supports the mechanism contract
only with partial control isolation and a non-retrieval-dominant bottleneck,
`R23` still leaves the systems verdict mixed, broader endpoint widening
remains unsupported, and future frontier review remains planning-only. `H21`
is now the preserved immediate pre-reopen control for the completed
`H20/R22/R23` packet. `H19` is now the preserved earlier same-endpoint
refreeze decision for the completed `H18/R19/R20/R21` packet. `H17` remains
the preserved prior same-scope refreeze decision for the completed
`H16/R15/R16/R17/R18` packet. `H15_refreeze_and_decision_sync` remains the
completed predecessor refreeze stage, `H14` remains the completed prior
reopened packet rather than the active stage, and `E1c` remains conditional
only and contradiction-only on current evidence.

The downstream `P14` public-surface sync implied by `H23` is docs-only and is
already complete. The current active post-`P9` stage is now
`H58_post_r62_origin_value_boundary_closeout_packet`, which preserves
`H56_post_r60_r61_useful_kernel_decision_packet` as the prior compiled
useful-kernel closeout, preserves
`H57_post_h56_last_discriminator_authorization_packet` as the prior
last-discriminator authorization packet, preserves
`H54_post_r58_r59_compiled_boundary_decision_packet` as the prior
compiled-boundary closeout, preserves
`H52_post_r55_r56_r57_origin_mechanism_decision_packet` as the prior
mechanism closeout, preserves `H50_post_r51_r52_scope_decision_packet` as the
broader-route value closeout, preserves `H43_post_r44_useful_case_refreeze`
as the paper-grade endpoint, preserves
`H36_post_r40_bounded_scalar_family_refreeze` as the routing/refreeze packet,
records `R42_origin_append_only_memory_retrieval_contract_gate`,
`R43_origin_bounded_memory_small_vm_execution_gate`,
`R44_origin_restricted_wasm_useful_case_execution_gate`, and
`R45_origin_dual_mode_model_mainline_gate` as the completed semantic-boundary
gate stack underneath the paper endpoint, records `R51/R52` as the broader
post-`H49` exactness-versus-value closeout pair, records `R55/R56/R57` as the
preserved prior mechanism evidence stack, records `R58/R59` as exact narrow
compiled-boundary evidence only, records `R60/R61` as exact-but-value-negative
compiled useful-kernel bridge evidence, records `R62` as the final native
value-negative discriminator, records
`F31_post_h56_final_discriminating_value_boundary_bundle` as the current
planning bundle above preserved `F30/F29/F28/F20`, records
`P40_post_h56_successor_worktree_and_artifact_hygiene_sync` as the current
operational/docs sidecar above preserved `P38/P27/P26/P25`, and keeps
`merge_executed = false` explicit while returning the downstream lane to
`no_active_downstream_runtime_lane`.

The later paper-facing and planning-only closeout lanes align to that reading:
`P28/P29/P30` keep publication, release, and manuscript ledgers downstream of
the preserved `H43` paper-grade endpoint; `F5` concludes
`no_reopen_candidate_survives`; `F6` records docs/planning maintenance as the
admissible default rather than a new runtime wave; `F7` makes future
same-substrate reopen criteria mechanical; `F8` stores beyond-Origin
milestone families without activating them; `F10` makes richer
executor-visible value/comparator obligations explicit without authorizing
runtime widening; `F12/F13/F14/F15` preserve origin-facing claim-delta and
conditional-reopen planning; `F9` remains blocked; `F11` remains
new-substrate; `P21/P22/P23/P24/P25/P26/P27/P38/P40` preserve the earlier driver,
handoff, audit, and explicit-merge surfaces; `R41` remains deferred behind a
later explicit contradiction packet; and no active downstream runtime lane
exists after `H58`.

## Reproducibility pointers

- `README.md`
- `STATUS.md`
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/manuscript_bundle_draft.md`
- `results/P1_paper_readiness/summary.json`
