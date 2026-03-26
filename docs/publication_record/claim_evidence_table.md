# Claim Evidence Table

## Current evidence

Lock note: narrow positive mechanism result survives; broad headline reproduction did not land.

- `C2e` — `results/M4_factorized_event_decoder/summary.json`
  Direct factorized event-value decoder: nontrivial teacher-forced accuracy,
  weak free-running rollout.
- `C2f` — `results/M4_staged_pointer_decoder/summary.json`
  Staged pointer decoder with structural, `opcode_shape`, and `opcode_legal`
  rollout on the harder held-out slice including `alternating_memory_loop`.
- `C2g` — `results/M5_pointer_baseline/training_run.json`
  Pointer-space softmax baseline: structural and `opcode_shape` remain the
  valid comparison regimes; `opcode_legal` stays diagnostic only.
- `C2h` — `results/M4_mask_dependence_executor_gap/summary.json`
  Expanded staged-mask batch: held-out `opcode_shape` collapses on the broader
  suite, while `opcode_legal` remains exact; cleaned failures split between
  `push_expr_0` trace mismatches and `step_budget` nontermination, so no
  fourth regime is justified.
- `C2h` — `results/M4_failure_provenance/summary.json`
  Provenance follow-up: the earlier held-out `opcode_shape` `step_budget` rows
  are downstream nontermination after first semantic divergence, not a third
  root-cause family beside `push_expr_0`.
- `C3c` — `results/M4_precision_scaling_real_traces/summary.json`
  Real offset traces reproduce the single-head precision failure mode.
- `C3d` — `results/M4_precision_scaling_real_traces/horizon_base_sweep.json`
  Horizon/base sweep over loop, ping-pong, and alternating offset streams.
- `C3e` — `results/M4_precision_generalization/screening.json`
  Broader real-trace suite: new high-address memory families fail at `1x`,
  while stack depth remains easier at `64` and begins to fail by `256`.
- `C3e` — `results/M4_precision_generalization/boundary_sweep.json`
  Boundary sweep: decomposition remains strong on the new memory families,
  while the deeper exported stack stream tightens the stable-base story.
- `C3e` — `results/M4_precision_organic_traces/claim_impact.json`
  Dedicated organic-trace bundle: same broadened evidence is now indexed under
  one explicit claim-impact artifact for paper/README use.
- `C3e` — `results/R1_precision_mechanism_closure/summary.json`
  Unified precision closure: single-head failures are common on the tracked
  suite, decomposition stays useful on current validated rows, and broader
  robustness claims remain blocked.
- `C3d/C3e` — `results/E1a_precision_patch/summary.json`
  Patch-level precision bundle: the denser `1/2/4/8/16/32/64` horizon grid
  stays on the same 25-stream / 7-family tracked suite, with `12/25`
  single-head failure streams, `7/25` already failing at `1x`, and `194`
  fully passing decomposition configs.
- `C3d/C3e` — `results/E1a_precision_patch/first_failure_rows.csv`
  Stream-level companion rows for the bounded patch: first-failure
  multipliers, full-horizon survivors, and control-vs-active scheme outcomes
  now live in one compact machine-readable table.
- `C3d/C3e` — `results/E1a_precision_patch/family_boundary_rows.csv`
  Family-level companion rows for the bounded patch: earliest failures,
  fail-at-`1x` counts, and decomposition coverage are summarized per family.
- `C3d/C3e` — `results/E1a_precision_patch/negative_control_rows.json`
  Weaker coarse-bucket control rows: the diagnostic control fails broadly on
  the same tracked suite, so it sharpens the mechanism story but is not a
  positive alternative.
- `D0` — `results/M6_typed_bytecode_harness/verifier_rows.json`
  Current tiny-bytecode verifier batch: twenty-two valid programs pass, and
  seven negative controls fail deterministically with first-error reports.
- `D0` — `results/M6_typed_bytecode_harness/short_exact_trace.json`
  Current exact-trace harness batch: sixteen short/medium programs, including
  the control-flow-first `call` / `ret` rows, match the lowered `exec_trace`
  path exactly.
- `D0` — `results/M6_typed_bytecode_harness/long_exact_final_state.json`
  Current long-row harness batch: six longer programs also match exactly
  through final state.
- `D0` — `results/M6_memory_surface_followup/summary.json`
  Diagnostic memory-surface follow-up: the same call/ret bytecode slice now
  has six annotated rows and two deterministic negative controls, with
  reference-vs-lowered surface views still matching exactly.
- `D0` — `results/M6_stress_reference_followup/summary.json`
  Stress/reference follow-up: one branch-selected helper checkpoint braid
  family now adds two medium exact-trace positives, one long exact-final-state
  positive, and two matched negatives under a standalone Python spec
  interpreter, while all three positive rows preserve companion
  memory-surface agreement.
- `D0` — `results/R3_d0_exact_execution_stress_gate/summary.json`
  Harder-suite exact-execution gate: seven additional bounded `D0` rows stay
  exact under bytecode, lowered `exec_trace`, and standalone spec agreement;
  linear versus accelerated Hull decode parity stays exact on all admitted
  lowered rows; four longer memory streams enter the immediate precision
  companion screen; and `E1c` remains inactive.
- `D0` — `results/R4_mechanistic_retrieval_closure/summary.json`
  Mechanistic retrieval closure: all `32` current positive `D0` programs are
  explainable using latest-write, stack, control, and deterministic
  local-transition primitives; `4290` source-event observations keep exact
  linear-versus-Hull parity; `R5` is not justified; and `E1c` remains
  inactive.
- `D0` — `results/H8_driver_replacement_guard/summary.json`
  Driver replacement guard: the repo control docs now treat `H8/R6/R7/H9` as
  the active packet while preserving `H6/R3/R4/(inactive R5)/H7` as the
  completed baseline on the same endpoint.
- `D0` — `results/R6_d0_long_horizon_scaling_gate/summary.json`
  Long-horizon scaling gate: current scalable `D0` families are pushed to fixed
  longer horizons without widening semantics; all `24` rows remain admitted,
  `8/8` longer-row decode-parity checks stay exact, growth reaches about
  `7.81x` over baseline seeds, and the narrow multiplier-`8` precision
  companion finds `4/8` boundary-bearing streams with the weaker control
  failing on `2/4` of them.
- `D0` — `results/R7_d0_same_endpoint_runtime_bridge/summary.json`
  Same-endpoint runtime bridge: the full `8`-family exact-admitted surface is
  preserved, but only the top `4` heaviest representatives are profiled and
  remain exact; accelerated Hull decode reaches only about `0.973x` of linear
  on median, remains about `1980.3x` slower per step than the lowered path,
  and therefore stops at
  `stop_decode_gain_not_material`.
- `D0` — `results/H10_r7_reconciliation_guard/summary.json`
  Reconciliation guard: the public and paper-facing ledgers now restate the
  completed `R7` stop result as a bounded top-`4` profile on the preserved
  `8`-family admitted surface.
- `D0` — `results/H11_post_h9_mainline_rollover_guard/summary.json`
  Mainline rollover guard: the repo control docs now treat
  `H10/H11/R8/R9/R10/H12` as the active packet while preserving
  `H8/R6/R7/H9` as the completed direct baseline.
- `D0` — `results/R8_d0_retrieval_pressure_gate/summary.json`
  Retrieval-pressure gate: the same fixed endpoint survives one bounded
  heavier-family pressure raise with `4/4` admitted exact rows, `2/2` bounded
  decode-parity probe matches, and no routed contradiction candidates.
- `D0` — `results/R9_d0_real_trace_precision_boundary_companion/summary.json`
  Precision companion: the admitted `R8` memory streams stay bounded and
  companion-only, with all `4/4` screened streams still `effective_here` and
  no weak negative-control failure.
- `D0` — `results/R10_d0_same_endpoint_cost_attribution/summary.json`
  Cost-attribution companion: representative admitted `R6/R8` rows keep the
  systems question narrow and show current exact runtime still dominated by
  retrieval cost rather than by harness or transition overhead.
- `D0` — `results/R11_geometry_fastpath_reaudit/summary.json`
  Geometry fast-path re-audit: the current exact `2D` parity slice stays exact
  on `5/5` audited cases and the preserved standalone cache-vs-bruteforce gain
  remains strong, but same-endpoint speedup wording stays blocked.
- `D0` — `results/R12_append_only_executor_long_horizon/summary.json`
  Append-only executor re-audit: current exported executor modes remain exact,
  heldout countdown still reaches `104` steps, the preserved harder `R3`
  baseline stays contradiction-free, and the next harder-slice inventory is
  explicit across staged `R6/R8` rows.
- `D0` — `results/H15_refreeze_and_decision_sync/summary.json`
  Refreeze-and-decision sync: the repo is now explicitly refrozen after the
  bounded reopen wave, with `R13` inactive, `R14` unjustified, and no new
  active science lane authorized without a later explicit plan.
- `D0` — `results/H17_refreeze_and_conditional_frontier_recheck/summary.json`
  Same-scope refreeze: the completed `H16/R15/R16/R17/R18` packet is frozen as
  the preserved prior reopen/refreeze baseline, with frontier review still
  conditional-only.
- `D0` — `results/H19_refreeze_and_next_scope_decision/summary.json`
  Same-endpoint mainline refreeze: the completed `H18/R19/R20/R21` packet is
  frozen machine-readably, with runtime generalization and mechanism support
  carried forward but no boundary break localized.
- `D0` — `results/R22_d0_true_boundary_localization_gate/summary.json`
  Harder boundary follow-up: the extended `102`-candidate executor grid stays
  exact throughout, so the bounded no-break story is strengthened but true
  boundary localization remains open.
- `D0` — `results/R23_d0_same_endpoint_systems_overturn_gate/summary.json`
  Same-endpoint systems recheck: `pointer_like_exact` stays exact on the full
  positive `D0` suite and is much faster than imported accelerated, but it is
  still slower than both the best current reference path and the lowered path,
  so the systems verdict remains mixed.
- `D0` — `results/H21_refreeze_after_r22_r23/summary.json`
  Post-`R22/R23` refreeze: the preserved pre-reopen control keeps scope
  locked, records `systems_still_mixed`, leaves frontier activation
  conditions unsatisfied, and preserves the same-endpoint control packet.
- `D0` — `results/H22_post_h21_boundary_reopen_and_dual_track_lock/summary.json`
  Bounded reopen-control packet: the post-`H21` follow-up is locked to one
  dual-track `D0` wave before any new execution runs.
- `D0` — `results/R26_d0_boundary_localization_execution_gate/summary.json`
  First-wave boundary scan: the declared `22`-candidate post-`H21` grid stays
  exact throughout and still does not localize a true executor boundary.
- `D0` — `results/R28_d0_trace_retrieval_contract_audit/summary.json`
  Mechanism-contract audit: append-only trace, latest-write, stack, and
  control-retrieval support remain positive on the current endpoint, but the
  control isolation story is still only partial and the bottleneck remains
  non-retrieval dominated.
- `D0` — `results/R27_d0_boundary_localization_extension_gate/summary.json`
  Conditional extension: the declared second-wave boundary packet stays exact
  on `12/12` rows and still does not localize a true executor boundary.
- `D0` — `results/H23_refreeze_after_r26_r27_r28/summary.json`
  Current refreeze: the current machine-readable state keeps scope locked,
  records `bounded_grid_still_not_localized`, carries
  `mechanism_contract_supported_with_partial_control_isolation`, preserves
  `systems_still_mixed`, and routes the next downstream docs lane to `P14`.
- `D0` — `results/R30_d0_boundary_reauthorization_packet/summary.json`
  Boundary reauthorization packet: the post-`H23` decision step authorizes one
  future family-local sharp zoom through `R32` rather than reopening the
  historical full-grid boundary search.
- `D0` — `results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json`
  Systems reauthorization packet: the post-`H23` systems decision step keeps
  `R29` blocked and routes any later same-endpoint systems story through the
  narrower `R33` non-retrieval audit first.
- `D0` — `results/H25_refreeze_after_r30_r31_decision_packet/summary.json`
  Active operational decision packet: `H25` preserves `H23` as the current
  frozen scientific state while recording `R32` as the primary next lane,
  `R33` as the deferred systems-audit lane, and `R29/F3` as still blocked.
- `D0` — `results/M7_frontend_candidate_decision/decision_summary.json`
  Frontend decision bundle: the preserved first compiled step stays on tiny
  typed bytecode, frontend widening is not authorized, and any revisit now
  requires a fresh scope + systems case.
- `R2` — `results/E1b_systems_patch/summary.json`
  Patch-level systems bundle: the mixed gate is restated with same-scope
  component attribution, `25` component rows, `5` suite bridges, `4` history
  bridges, and lowered execution still about `1.824x` slower than the best
  current reference path, while frontend widening remains blocked.
- `R2` — `results/E1b_systems_patch/component_cost_rows.csv`
  Program-level attribution companion: the current runtime gap is decomposed
  across verification, bytecode, lowered, and spec paths on the existing
  positive `D0` suites.
- `R2` — `results/E1b_systems_patch/suite_bridge_rows.csv`
  Suite-level bridge companion: the current mixed gate is broken out by suite
  rather than left as one median-only statement.
- `R2` — `results/E1b_systems_patch/history_bridge_rows.csv`
  History bridge companion: asymptotic geometry wins are tied back to current
  `D0` step counts without treating beyond-scope histories as end-to-end
  runtime evidence.

## Current bounded mainline state

- `H61` is now the current active docs-only packet; it preserves `H60` and
  `H59` as prior decision packets, preserves `H58` as the prior value-negative
  closeout, preserves `F32` as the closeout certification bundle, preserves
  `H43` as the paper-grade endpoint, selects
  `archive_first_consolidation_becomes_default_posture`, keeps `F27/R53/R54`
  blocked, and leaves the downstream lane at `planning_only_or_project_stop`.
- `F36` is the current qualification-only bundle; it preserves the one
  admissible future family
  `compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route`,
  fixes strict baseline and stop-rule discipline, and keeps runtime closed.
- `P46` is the current publication/docs wave; it keeps the narrow positive
  mechanism result explicit, keeps the broad headline negative explicit, makes
  narrow mechanistic reproduction plus executor-value partial falsification the
  outward shorthand, and keeps the compiled-online route qualification-only.
  archive-first consolidation is now the default live posture.
- `P45` is the current repo-hygiene sidecar; it records the clean successor
  line, keeps dirty root `main` quarantined, and records
  `clean_descendant_only_never_dirty_root_main`.
- `F35` is the current far-future storage bundle; it records
  `high_cost_model_route_far_future_only` and
  `programs_into_weights_route_far_future_only`.
- `H60` is the preserved prior active packet; it records
  `remain_planning_only_and_prepare_stop_or_archive`.
- `F34` is the preserved prior reopen screen; it names only the one compiled-
  online family and keeps same-lane executor-value microvariants inadmissible.
- `P44` is the preserved prior publication/docs wave; it keeps the narrow
  positive mechanism result explicit, keeps the broad headline negative
  explicit, and keeps the compiled-online route conditional only at that stage.
- `P43` is the preserved prior repo-hygiene sidecar; it records the preferred
  repo-local worktree graph and the original descendant-only merge posture.
- `P42` is the preserved prior advisory/docs wave; it records the
  self-contained GPTPro dossier and keeps it advisory rather than
  claim-bearing.
- `P41` is the preserved prior publication/archive sync sidecar; it records
  that archive/release surfaces are aligned to `H59`, confirms zero tracked
  artifacts at or above roughly `10 MiB`, and confirms that raw-row ignore
  rules remain active.
- `F32` is the preserved prior closeout certification bundle; it certifies
  that `H58` is a real stop boundary and not a staging point.
- `H58` is the preserved prior docs-only closeout packet for the final
  post-`H56` discriminator wave; it preserves `H56` as the prior compiled
  useful-kernel closeout, preserves `H57` as the prior authorization packet,
  preserves `H43` as the paper-grade endpoint, selects
  `stop_as_mechanism_supported_but_no_bounded_executor_value`, keeps
  `F27/R53/R54` blocked, and restores `no_active_downstream_runtime_lane`.
- `F31` is the completed preserved planning bundle that fixed
  `H57 -> R62 -> H58` as the only admissible post-`H56` sequence and kept
  `P40` as the operational sidecar for that closed wave.
- `H57` is the preserved prior docs-only authorization packet for the last
  native useful-kernel discriminator lane; it preserved `H56`, preserved
  `H43`, and authorized exactly `R62 -> H58` without reopening transformed or
  trainable entry.
- `R62` is the completed native useful-kernel value discriminator gate; it
  keeps all declared native comparators exact on `4/4` rows across `2/2`
  kernels but records `native_useful_kernel_route_lacks_bounded_value`
  because accelerated wins are `0/2` on the longest kernel rows and
  external-scalar same-order behavior is `0/2`.
- `P40` is the preserved prior low-priority operational/docs wave for the
  closed final-discriminator packet; it recorded the clean successor worktree,
  kept `merge_executed = false` explicit, and confirmed zero tracked artifacts
  at or above roughly `10 MiB`.
- `H56` is the preserved prior docs-only interpretation packet for the closed
  compiled useful-kernel bridge lane after landed `R60/R61`; it preserves
  `H54` as the prior compiled-boundary closeout, preserves `H55` as the prior
  useful-kernel reentry packet, preserves `H43` as the paper-grade endpoint,
  selects
  `freeze_minimal_useful_kernel_bridge_supported_without_bounded_value`,
  keeps `F27/R53/R54` blocked, and restores
  `no_active_downstream_runtime_lane`.
- `F30` is the completed preserved planning bundle that fixed
  `H55 -> R60 -> R61 -> H56` as the only admissible useful-kernel bridge
  sequence above preserved `H54/H52/H43/H36`.
- `H55` is the preserved prior docs-only interpretation packet for the
  minimal useful-kernel carryover lane; it preserved `H54`, preserved `H52`,
  preserved `H43`, and authorized exactly `R60 -> R61 -> H56`.
- `R60` is the completed preserved prior compiled useful-kernel carryover
  gate; it keeps `5/5` declared variants exact across `2/2` preserved kernels
  with zero compiler-leakage breaks.
- `R61` is the completed preserved prior useful-kernel comparator gate; it
  keeps all comparators exact on the declared `R60` rows but records
  `compiled_useful_kernel_route_lacks_bounded_value` because accelerated wins
  are `0/5`.
- `H54` is the preserved prior docs-only interpretation packet for the closed
  compiled-boundary lane after landed `R58/R59`; it preserves `H52` as the
  prior mechanism closeout, preserves `H53` as the prior compiled-boundary
  reentry packet, preserves `H43` as the paper-grade endpoint, selects
  `freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value`,
  and restores `no_active_downstream_runtime_lane`.
- `H53` is the preserved prior docs-only interpretation packet for the
  narrowed compiled-boundary reentry lane; it preserved negative `H52`,
  preserved `H43`, and authorized exactly `R58 -> R59 -> H54`.
- `H52` is the preserved prior docs-only interpretation packet for the closed
  mechanism reentry lane after landed `R55/R56/R57`; it preserves `H50` as
  the broader-route bounded-value closeout, preserves `H51` as the prior
  mechanism-reentry packet, preserves `H43` as the paper-grade endpoint,
  selects `freeze_origin_mechanism_supported_without_fastpath_value`, and
  restores `no_active_downstream_runtime_lane`.
- `H50` is the preserved prior docs-only interpretation packet for the bounded
  mainline after completed `R51/R52`; it preserves `H49` as the prior
  decision packet, preserves `H48` as the earlier decision packet, preserves
  `H43` as the paper-grade endpoint, selects
  `stop_as_exact_without_system_value`, keeps `F27` blocked and
  non-selected, and restores `no_active_downstream_runtime_lane`.
- `H43` is the preserved prior useful-case refreeze packet and current
  paper-grade endpoint; it records claim `D` as `supported_here_narrowly` and
  restores `no_active_downstream_runtime_lane`.
- `H42` and `H41` are the preserved prior docs-only decision packets that
  respectively authorized exact `R44` and authorized exact `R43` plus coequal
  `R45`.
- `H36` is the preserved active routing/refreeze packet; it freezes the
  bounded-scalar family narrowly and remains the routing packet underneath the
  later semantic-boundary and useful-case stacks.
- `R42`, `R43`, `R44`, and `R45` remain the preserved semantic-boundary and
  useful-case evidence stack underneath `H43`; exact evidence remains
  decisive and model evidence remains explicitly non-substitutive.
- `R46`, `R47`, `R48`, `R49`, `R50`, `R51`, and `R52` remain the preserved
  post-`H43` useful-case extension stack; those packets stay historically
  informative but do not override the later `H50/H52/H54/H56/H58` stop chain.
- `F28`, `F29`, `F20`, `F18`, `F19`, `F17`, `F16`, and `F15` remain
  preserved planning/control bundles; none changes the scientific lane by
  itself.
- `P27` remains the preserved explicit merge packet with
  `merge_executed = false`; `P26` remains the preserved prior operational
  promotion/artifact audit lane.
- `H40`, `H38`, `H37`, `H35`, `H34`, `H33`, `H32`, `H31`, `H30`, `H29`, and
  `H28` remain preserved routing/control history underneath the current stack.
- `R41` remains deferred until a later explicit contradiction packet.
- `H27` remains the preserved negative closeout of the old same-endpoint
  recovery route.
- `H25`, `H23`, `H21`, `H19`, `H17`, and `H15` remain preserved historical
  same-endpoint control packets, not the current mainline state.
- `H8/R6/R7/H9` remain the completed direct same-endpoint baseline, and
  `H6/R3/R4/(inactive R5)/H7` remain the deeper exactness/mechanism baseline
  underneath that historical route.
- `E1c` remains inactive unless the active Origin-core packet exposes a
  concrete frozen-`D0` contradiction that wording alone cannot repair.
- `H3/P10/P11/F1` remain the documentation/archive baseline while
  `H4/E1a/E1b/H5` remain the completed bounded return baseline.
