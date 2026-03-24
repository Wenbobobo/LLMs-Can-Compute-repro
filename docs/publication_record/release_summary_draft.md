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
`H43_post_r44_useful_case_refreeze`.
Earlier paper/release controls such as `P3`, `R1`, `R2`, `M7`, and `P4`
remain relevant guardrails, but they are no longer the current
science-routing story by themselves.

## Current endpoint and non-goals

The active endpoint on current evidence is the narrower Origin-core
semantic-boundary line now carried through exact bounded-memory execution
(`R43`), coequal `R45` model support, and the restricted useful-case climb
frozen by `H43`. The earlier tiny typed-bytecode `D0` endpoint remains a
preserved first compiled boundary and should not be read as the current bridge
to arbitrary C, general LLM computation, or broader demo-first claims. Those
broader readings remain explicitly unsupported on the current paper scope. A
later internal follow-on under `H44`, `R46`, kept the held-out in-surface
useful-case matrix exact on `8/8` variants, but `H45` still must interpret
that result before any broader surface lift.

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
`H43_post_r44_useful_case_refreeze`, which preserves
`H42_post_r43_route_selection_packet` and
`H41_post_r42_aggressive_long_arc_decision_packet` as the prior docs-only
decision packets, preserves
`H36_post_r40_bounded_scalar_family_refreeze` as the active routing/refreeze
packet, records `R42_origin_append_only_memory_retrieval_contract_gate`,
`R43_origin_bounded_memory_small_vm_execution_gate`,
`R44_origin_restricted_wasm_useful_case_execution_gate`, and
`R45_origin_dual_mode_model_mainline_gate` as the completed current
semantic-boundary gate stack, records
`F20_post_r42_dual_mode_model_mainline_bundle` as the coequal-mainline model
bundle, records `P27_post_h41_clean_promotion_and_explicit_merge_packet` as
the completed explicit merge packet with `merge_executed = false`, records
`P26_post_h37_promotion_and_artifact_hygiene_audit` as the preserved prior
operational audit lane, records
`F16_post_h37_r41_candidate_isolation_bundle`,
`F17_post_h38_same_substrate_exit_criteria_bundle`,
`F18_post_h38_origin_core_long_arc_bundle`,
`F19_post_f18_restricted_wasm_useful_case_roadmap`, and
`F15_post_h36_origin_goal_reanchor_bundle` as the current planning/control
bundle set, and keeps `H40_post_h38_semantic_boundary_activation_packet`,
`H38_post_f16_runtime_relevance_reopen_decision_packet`,
`H37_post_h36_runtime_relevance_decision_packet`, and
`P25_post_h36_clean_promotion_prep` as the prior decision/audit support wave.
Under that state, `H27` remains the negative closeout of the old
same-endpoint route, `H28` remains the Origin-core pivot packet, `H29`
remains the positive narrow refreeze, `R36` remains the completed
precision-boundary follow-up, `R37` remains one tiny compiled-boundary
confirmation, `H31` remains the explicit later-decision packet, `R38` remains
one richer same-substrate control/call family, `H33` preserves the one-
question docs-only selection step, `R39` preserves one narrow same-substrate
dependency audit, `H34` preserves the freeze-complete-for-now compiled line,
`H35` authorizes exactly one bounded-scalar same-substrate runtime gate, and
`R40` validates bounded scalar locals and typed `FLAG` slots on one admitted
row plus one same-family boundary row. `H37` first keeps that `H36` freeze,
`F16` then reduces the saved `R41` catalog to fixed candidate statuses and
concludes `no_candidate_ready`, `H38` keeps the same freeze again because
there is still no `execution_ready` candidate on the landed `R40` row pair,
`P26` records an `audit_only` promotion posture, `F17/F18/F19` select and
constrain the semantic-boundary route, `H40` authorizes exactly `R42`, `R42`
validates the first append-only retrieval contract, `F20/H41/P27` make the
later exact-versus-model and explicit-merge posture canonical, `R43` lands the
bounded-memory exact gate, `R45` lands the coequal model gate, `H42`
authorizes exact `R44`, `R44` lands the fixed useful-case ladder, and `H43`
refreezes that result as bounded useful-case support only. The later
paper-facing and planning-only closeout lanes now also align to that reading:
`P20` remains the preserved earlier manuscript bundle resync that terminated on
the landed `H34` state at that stage, `P30` now refreshes the
manuscript-facing bundle to the landed `H43` state, `F5` concludes
`no_reopen_candidate_survives`, `F6` records docs/planning maintenance as the
admissible default rather than a new runtime wave, `F7` makes future
same-substrate reopen criteria mechanical, `F8` stores beyond-Origin milestone
families without activating them, `F10` makes richer executor-visible
value/comparator obligations explicit without authorizing runtime widening,
`F12` remains the preserved earlier origin-facing claim delta reanchor, `F13`
fixes `bounded scalar locals and flags` as the bounded same-substrate
family-first preactivation surface, `F14` stores a conditional
reopen-readiness blueprint, `F15` reanchors the origin-facing claim delta to
the current control state, `P28` aligns publication-facing ledgers to landed
`H43`, `P29` aligns release/public audit surfaces to landed `H43`, `F9`
remains blocked, `F11` remains new-substrate, `P21` and `P22` remain
preserved prior planning syncs, `P23/P24/P25` preserve the earlier driver and
handoff surfaces, `P26/P27` preserve the audit-plus-explicit-merge operational
posture, `R41` remains deferred behind a later explicit contradiction packet,
and no active downstream runtime lane exists after `H43`.

## Reproducibility pointers

- `README.md`
- `STATUS.md`
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/manuscript_bundle_draft.md`
- `results/P1_paper_readiness/summary.json`
