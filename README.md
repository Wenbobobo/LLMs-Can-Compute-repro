# llms-can-compute-repro

Careful reproduction of a narrowed execution-substrate reading of Percepta's
field note _Can LLMs Be Computers?_

This repository tracks a paper-grade endpoint:

1. deterministic computation can be encoded as an append-only execution trace;
2. exact latest-write retrieval over that trace can be implemented with
   structured 2D hard-max retrieval;
3. on the current validated scope, those primitives support a small exact
   executor; the earlier tiny typed-bytecode `D0` compiled endpoint is now a
   preserved historical boundary rather than the active mainline.

This repository does **not** claim that general LLMs are computers, that
arbitrary C has been reproduced, or that demo-first presentation is evidence.

## Current Mainline Note

As of `2026-03-23`, the canonical current stage is no longer the old
same-endpoint `D0` recovery line. The active routing/refreeze packet remains
`H32_post_r38_compiled_boundary_refreeze`, and the current docs-only control
packet is `H34_post_r39_later_explicit_scope_decision_packet`, preserving:

- `H27` as the negative closeout of the old same-endpoint recovery wave;
- `H28` as the Origin-core pivot packet;
- `H29` as the positive Origin-core refreeze packet on the current A/B/C chain;
- `R36` as a narrow precision-boundary sharpening pass;
- `R37` as the tiny compiled-boundary confirmation on the current
  append-only / exact-retrieval / small-VM substrate;
- `H30` as the preserved prior tiny compiled-boundary refreeze packet;
- `H31` as the explicit one-more-extension authorization packet;
- `R38` as the one-richer control/call-family compiled boundary gate on the
  same opcode surface;
- `P18` as the operational clean-worktree packaging lane for this packet;
- `H33` as the prior docs-only next-question packet that keeps `H32` active while
  naming only `R39_origin_compiler_control_surface_dependency_audit` as the
  one justified same-substrate follow-up question; and
- `R39` as the completed same-substrate dependency audit showing that one
  declared helper-body permutation with target renumbering can preserve exact
  final state and workload while still changing the trace on both audited rows;
- `H34` as the docs-only later explicit scope-decision packet that keeps `H32`
  active while selecting `freeze_compiled_boundary_as_complete_for_now`.

For current work, trust
`docs/publication_record/current_stage_driver.md`,
`tmp/active_wave_plan.md`,
`docs/plans/2026-03-23-post-h33-r39-origin-core-substrate-question-design.md`,
`results/H33...`, `results/R39...`, and the `results/H32...` / `results/R38...` /
`results/H31...` / `results/H30...` summaries ahead of the historical packet
inventory below.

## Current Boundary

| Track | Current state |
| --- | --- |
| `M0-M3` | repo scaffold, claim discipline, geometry core, and append-only trace executor are in place |
| `M4-M5` | exact retrieval/executor branches, staged-pointer caveats, and softmax negative controls remain recorded without widening |
| `M6-M7` | the tiny typed-bytecode boundary is implemented and validated; widening remains blocked |
| `P1-P10` | paper bundle, public-safe packaging, bundle-lock audits, and archive handoff remain active |
| `H4-H5` | bounded return packet completed and preserved as historical scientific baseline |
| `H6-H7` | bounded exactness/mechanism packet completed and preserved as the deeper baseline underneath the current stage |
| `H8-H9` | completed bounded `D0` long-horizon packet: `H8` replaced the driver, `R6` completed the long-horizon scaling gate, `R7` preserved the full `8`-family exact-admitted surface but profiled only the top `4` heaviest representatives, and `H9` refroze the packet |
| `H10-H12` | completed bounded `D0` retrieval-pressure packet: `H10` reconciles `R7` to artifact-backed wording, `H11` replaces the driver, `R8` stresses higher retrieval pressure on the same endpoint, `R9` keeps real-trace precision companion-only, `R10` attributes same-endpoint costs, and `H12` refreezes the packet |
| `H13-V1` | completed governance/runtime handoff preserved as a control baseline: `H13` kept the completed checkpoint explicit, `V1` classified the slow full-suite `pytest -q` gate as `healthy_but_slow`, and outward-sync audits were tightened without widening scope |
| `H14-H15` | completed bounded core-first reopen/refreeze packet: `H14` locked the reopened lane to exact 2D retrieval plus append-only/latest-write execution, `R11/R12` landed on bounded evidence, `R13` stayed inactive, `R14` stayed unjustified, and `H15` refroze the repo on the same endpoint |
| `H16-H17` | completed bounded same-scope reopen/refreeze packet: `H16` kept the same `D0` endpoint active after `H15`, `R15` and `R16` closed the remaining-family retrieval-pressure and admitted precision surfaces, `R17` landed as the full-surface runtime stop result, `R18a` failed its narrow decomp-first gate, `R18b` then closed the runtime repair packet with exact `8/8` confirmation, and `H17` refroze the repo on the same endpoint |
| `H18-H19` | completed bounded same-endpoint mainline reopen/refreeze packet: `H18` kept the `D0` scope lock explicit, `R19` confirmed admitted-plus-heldout same-endpoint runtime generalization, `R20` supported the mechanism on a fixed `16`-row probe set, `R21` did not expose a failure inside the bounded `48`-branch executor grid, and `H19` refroze the packet as the current machine-readable state |
| `H20-H21` | completed post-`H19` reentry/refreeze packet: `H20` isolated dirty-tree hygiene from the next science lanes, `R22` extended the bounded executor-boundary scan to `102/102` executed candidates without localizing a failure, `R23` reran the full positive `D0` systems universe and kept `pointer_like_exact` exact on `25/25` rows but still failed to overturn the mixed systems gate, and `H21` refroze the packet as the preserved pre-reopen same-endpoint control |
| `H22-H23` | completed bounded post-`H21` dual-track reopen/refreeze packet preserved as the prior same-endpoint frozen scientific state: `H22` locked one boundary-first reopen contract, `R26` executed `22/22` first-wave candidates without localizing a failure, `R28` audited the mechanism contract as supported with partial control isolation, `R27` extended to `12/12` second-wave candidates without localizing a failure, and `H23` refroze the packet with `P14` as the downstream docs-only lane |
| `H24-H25` | completed post-`H23` reauthorization/refreeze packet preserved as the prior same-endpoint decision layer: `H24` separated reauthorization work from hygiene, `R30` authorized one future family-local boundary sharp zoom through `R32`, `R31` routed any later same-endpoint systems recovery discussion through `R33` non-retrieval overhead localization first, and `H25` refroze that decision packet without widening scope |
| `H26-H29` | completed same-endpoint closeout plus Origin-core pivot/refreeze packet: `R32/R33/H27` closed the old same-endpoint route negatively, `H28` reanchored the project around append-only traces plus exact retrieval plus a small exact stack/VM, `R34/R35` validated that narrow chain, and `H29` froze it positively |
| `R36` | completed narrow precision-boundary follow-up on the active Origin-core bundle: inflated-horizon float32 `single_head` fails on selected high-address/deep-stack rows while bounded decomposition schemes recover those exact rows without authorizing broader scope lift |

## Current Gate Outcome

- The current active stage is `H32_post_r38_compiled_boundary_refreeze`, not
  the preserved prior `H30` packet or the earlier `H25` same-endpoint
  decision packet.
- The current docs-only control packet is
  `H34_post_r39_later_explicit_scope_decision_packet`, which selects
  `freeze_compiled_boundary_as_complete_for_now` and names no active
  downstream runtime lane.
- The current active scientific target is the narrower Origin-core line:
  append-only traces, exact `2D` hard-max retrieval, and a small exact stack/VM
  executor.
- `R34` supports the narrow retrieval primitive contract on `47/47`
  observations, `R35` supports exact rollout on `12/12` current bundle rows,
  `R36` sharpens a suite-bounded precision boundary, `R37` shows that one tiny
  admitted bytecode subset can lower onto the active substrate exactly, `H31`
  names the only allowed later-explicit extension, `R38` validates one richer
  compiled control/call family on the same substrate, and `H32` refreezes that
  result without broadening scope.
- `R39` then executes one declared helper-body permutation with target
  renumbering and returns
  `control_surface_dependence_not_detected_on_declared_permutation` on both the
  admitted row and the recorded boundary probe, while still not authorizing
  arbitrary control-surface freedom or broader compiler claims.
- `H34` then interprets that result as complete-for-now narrow support rather
  than authorizing another same-substrate runtime move by momentum.
- The old same-endpoint `D0` story is preserved historically: `H27` closes it
  negatively, `H30` preserved the first tiny compiled-boundary positive packet,
  and `H31` then keeps further extension behind an explicit named decision
  rather than momentum.
- The current compiled-boundary claim remains narrow: the admitted
  post-`H30` extension row is `subroutine_braid_program(6, base_address=80)`,
  while `subroutine_braid_long_program(12, base_address=160)` is recorded as a
  same-family boundary probe rather than an admitted widening.
- The preserved design surface that led to the completed `R39` audit is
  `docs/plans/2026-03-23-post-h33-r39-origin-core-substrate-question-design.md`;
  the preserved design surface that led to the landed `H34` interpretation is
  `docs/plans/2026-03-23-post-r39-later-explicit-scope-decision-design.md`;
  `R39` itself is not a routing change, and there is now no active downstream
  runtime lane.

- The current active stage still starts from the locked submission-candidate
  bundle and restrained release-candidate checkpoint created by `P8/P9`.
- The precision story remains bounded rather than broad: float32 single-head
  fails on `12/25` tracked real/organic streams, `7/25` already at `1x`, while
  at least one decomposition stays exact on `25/25` tracked streams in the
  validated suite.
- The systems gate remains mixed: geometry is strongly positive, but the
  lowered path is still about `1.82x` slower than the best current
  reference/oracle path on positive `D0` suites.
- `R6` keeps the completed long-horizon packet positive on the same endpoint:
  `24/24` fixed-multiplier rows stay admitted, `8/8` longer-row decode-parity
  checks match exactly, and the narrow multiplier-`8` precision companion
  finds `4/8` boundary-bearing streams while the weaker control fails on `2/4`
  of those boundary-bearing rows.
- `R7` preserved the full `8`-family exact-admitted `R6` index but only
  profiled the top `4` heaviest family representatives on the same endpoint;
  all `4/4` profiled rows stayed exact, accelerated Hull decode reached only
  about `0.973x` of linear on median, and it still ran about `1980.3x` slower
  per step than the lowered path.
- `R8` stresses higher retrieval pressure on the same endpoint and is now
  closed on a bounded harder-family gate: `4/4` exact rows remain admitted,
  the bounded top-`2` decode-parity probe matches on `2/2` rows, and
  retrieval pressure grows to about `1.249x` max events and `1.560x` max
  total candidate depth versus the admitted `R6` `8x` source rows.
- `R9` keeps real-trace precision companion-only and is now closed on the
  admitted `R8` memory streams: all `4/4` screened streams stay
  `effective_here`, one `single_head` `tie_collapse` appears at `1x` on the
  helper-checkpoint-braid-long stream, the default decomposition grid still
  passes there, and the weaker negative control does not fail.
- `R10` attributes same-endpoint costs and is now closed on representative
  admitted rows: median exact-versus-lowered runtime is still about
  `2429.1x`, median retrieval share is about `99.8%`, harness share is
  effectively negligible, and retrieval dominates on `4/4` profiled rows.
- `H8/R6/R7/H9` now sits as the completed direct same-endpoint baseline, while
  `H6/R3/R4/(inactive R5)/H7` remains the older exactness/mechanism baseline
  underneath it.
- `H10/H11/R8/R9/R10/H12` is now the latest completed same-endpoint follow-up
  packet rather than the active science lane. It keeps the same endpoint
  fixed, closes `R8/R9/R10` on bounded evidence, and leaves `H12` as the
  completed refreeze lane for the current scientific checkpoint.
- `H13/V1` remains preserved as the completed governance/runtime handoff:
  `pytest --collect-only -q` succeeds on the current suite, the bounded top-`6`
  timing follow-up classifies full `pytest -q` as healthy but multi-minute,
  and outward-sync control remains machine-audited.
- On the preserved prior same-endpoint route, the last post-`P9` active packet
  was `H25_refreeze_after_r30_r31_decision_packet`. That `H25/H23` stack is no
  longer the current mainline after `H27 -> H28 -> H29 -> R36 -> R37 -> H30`;
  it remains historical control context only.
- `H15_refreeze_and_decision_sync` is now the preserved prior refreeze and
  decision record. It still records `R13` as inactive and `R14` as
  unjustified on the fixed `D0` endpoint.
- `H14_core_first_reopen_and_scope_lock` is now the completed reopened packet
  underneath the active `H16` packet. That packet kept work bounded to exact
  `2D` geometry plus append-only/latest-write execution, ran `R11` before
  `R12`, left `R13` inactive, and left `R14` downstream rather than
  authorizing compiled widening by wording alone.
- `R11` has now closed on a bounded current-code re-audit: the geometry parity
  slice stays exact on `5/5` audited cases, preserved cache-versus-bruteforce
  speedup ranges from about `42.8x` to `249.2x`, and same-endpoint lowered-path
  speedup wording remains blocked.
- `R12` has now closed on a bounded reopened executor export: current
  `exact_linear`, `exact_accelerated`, and bounded `trainable_stack` modes all
  remain exact on the exported suites, the longest heldout countdown still
  reaches `104` steps, and the next harder-slice inventory is explicit across
  `24` staged `R6` rows plus `4` staged `R8` rows.
- `R15` has now closed the bounded remaining-family retrieval-pressure gate:
  all `4/4` remaining-family harder rows stay admitted, the bounded top-`2`
  decode-parity probe matches on `2/2` rows, and remaining-family retrieval
  pressure rises to about `1.248x` max event growth plus about `1.557x` max
  total candidate-depth growth versus the admitted `R6` `8x` source rows.
- `R15` complements rather than replaces `R8`: together they now cover all
  `8` current `R6` families with bounded same-endpoint retrieval-pressure
  evidence.
- `R16` has now closed the bounded real-trace precision saturation follow-up
  on that admitted `R8/R15` memory surface: all `8/8` screened streams remain
  `effective_here`, only the preserved helper-checkpoint-braid-long stream
  enters boundary follow-up, the default decomposition grid still passes there,
  and the weaker base-`256` control does not fail.
- `R17` has now closed the bounded full-surface same-endpoint runtime bridge:
  all `8/8` admitted runtime rows stay exact, median
  accelerated-versus-linear speedup is only about `1.0019x`, median
  accelerated-versus-lowered ratio is still about `1257.5x`, focused
  attribution on the preserved boundary-bearing `R8` row plus the heaviest
  admitted `R15` row remains retrieval-dominated, and `R18` is therefore
  conditionally activated only around
  `helper_checkpoint_braid_long/retrieval_total`.
- `R18a` first measured the narrow decomp-first counterfactual on that named
  target and failed its `2.0x` gate, but `R18b` then closed the comparator-only
  repair packet: pointer-like exact retrieval stayed exact on the focused
  target plus matched control, the target reached about `1308.5x` versus the
  recorded `R17` accelerated baseline, and the admitted `8/8` confirmation
  sweep stayed exact with about `1252.7x` median speedup versus the recorded
  `R17` accelerated baseline.
- `H17` is now preserved as the prior same-scope refreeze and frontier-review
  decision record for the completed `H16/R15/R16/R17/R18` packet.
- `H18` has now exported that planning guard as
  `results/H18_post_h17_mainline_reopen_guard/summary.json`, keeping the
  `D0` scope lock explicit while moving the unattended handoff into `R19`.
- `R19` has now closed the first admitted-plus-heldout same-endpoint runtime
  gate: `pointer_like_exact` stayed exact on admitted `8/8` plus heldout
  `16/16` rows, no heldout family failed, and median pointer-like speedup
  reached about `396.9x` versus current accelerated on admitted rows plus
  about `457.0x` on heldout rows.
- `R20` has now closed the bounded same-endpoint mechanism ablation lane:
  `pointer_like_exact` stayed exact on the fixed `16/16` `R19`-derived sample
  set, median pointer-like speedup versus imported current accelerated reached
  about `392.6x`, and both negative controls failed on `16/16` rows.
- `R21` has now closed the bounded exact-executor boundary map on the same
  endpoint: `pointer_like_exact` stayed exact on `96/96` executed candidates
  across the fixed `48`-branch grid, and no branch failures were observed
  inside that bounded scan.
- `H19` has now recorded the preserved post-`H18` frozen same-endpoint control
  state:
  `decision_state = same_endpoint_refreeze_complete`,
  `runtime_generalization_verdict = same_endpoint_generalization_confirmed`,
  `mechanism_verdict = mechanism_supported`,
  `boundary_verdict = no_boundary_break_detected`,
  `future_frontier_review_state = planning_only_conditionally_reviewable`, and
  `historical_next_priority_lane = p13_public_surface_sync_and_repo_hygiene`.
- `H20` has now exported the post-`H19` reentry and hygiene split guard,
  keeping the dirty-tree isolation problem explicit before `R22` and `R23`
  landed.
- `R22` has now closed the harder same-endpoint boundary follow-up:
  all `102/102` executed candidates stayed exact, no boundary failure was
  localized, and the next lane remained `R23`.
- `R23` has now closed the same-endpoint systems overturn follow-up on the full
  positive `D0` suite: `pointer_like_exact` stayed exact on `25/25` rows and
  improved sharply versus imported accelerated, but still remained about
  `4.16x` slower than the best current reference path, so the lane verdict is
  `systems_still_mixed`.
- `H21` now remains the preserved pre-reopen same-endpoint control:
  `decision_state = post_r22_r23_refreeze_complete`,
  `boundary_verdict = extended_grid_no_break_still_not_localized`,
  `systems_verdict = systems_still_mixed`, and
  `future_frontier_review_state = planning_only_conditionally_reviewable`.
- `H22` then reopened the mainline only as one bounded dual-track packet on
  the same `D0` endpoint.
- `R26` closed the declared `22`-candidate first-wave boundary scan with
  `22/22` exact candidates and no localized failure.
- `R28` closed the parallel mechanism-contract audit with
  `mechanism_contract_supported_with_partial_control_isolation` and a
  `pointer_like_exact_non_retrieval_dominant` bottleneck verdict.
- `R27` then closed the declared second-wave boundary extension with
  `12/12` exact candidates and no localized failure.
- On the preserved prior same-endpoint route, `H23` recorded the frozen state:
  `decision_state = post_r26_r27_r28_refreeze_complete`,
  `boundary_verdict = bounded_grid_still_not_localized`,
  `mechanism_contract_verdict = mechanism_contract_supported_with_partial_control_isolation`,
  `systems_verdict = systems_still_mixed`, and
  `next_priority_lane = p14_public_surface_sync_after_h23`.
- `H24` then split post-`H23` reauthorization work from hygiene and kept
  `R29`/`F3` blocked while the decision packet was assembled.
- `R30` then authorized one future family-local boundary sharp zoom through
  `R32_d0_family_local_boundary_sharp_zoom` rather than another historical
  full-grid expansion.
- `R31` then concluded that any later same-endpoint systems recovery story must
  first pass through `R33_d0_non_retrieval_overhead_localization_audit`; direct
  `R29` activation remains blocked.
- On the preserved prior same-endpoint route, `H25` recorded the active
  operational decision packet:
  `decision_state = post_h23_reauthorization_packet_complete`,
  `current_frozen_stage = h23_refreeze_after_r26_r27_r28`,
  `next_priority_lane = r32_d0_family_local_boundary_sharp_zoom`, and
  `deferred_audit_lane = r33_d0_non_retrieval_overhead_localization_audit`.
- that `H25` machine state still does not authorize a frontier run: any later
  broader review remains blocked behind true boundary localization, a
  materially positive same-endpoint systems story, and an explicit later
  scope-lift reauthorization.
- V1 remains a standing operational reference under the preserved `H13`
  handoff rather than an active science lane.
- The compiled endpoint remains tiny typed bytecode `D0`; no active lane
  authorizes frontend widening, arbitrary compiled-language claims, or a
  broader “LLMs are computers” thesis.
- `E1c` stays conditional only and contradiction-only throughout the packet.

## Start Here

- `STATUS.md` — current repository state and immediate gates
- `docs/publication_record/current_stage_driver.md` — canonical current stage driver
- `docs/plans/README.md` — plans index for the current `post-H32` planning surface, the landed `H31/R38/H32/P18` wave, and the historical design stack
- `docs/milestones/README.md` — milestones index separating the current stack, deferred lanes, blocked/planning-only bundles, and preserved historical packets
- `docs/plans/2026-03-23-post-h33-r39-origin-core-substrate-question-design.md` — preserved design that led to the completed post-`H33` same-substrate audit, `R39`
- `docs/plans/2026-03-23-post-r39-later-explicit-scope-decision-design.md` — preserved design that led to the landed post-`R39` docs-only scope-decision packet, `H34`
- `docs/plans/2026-03-23-post-h32-conditional-next-packet-design.md` — preserved post-`H32` planning packet that led to the landed docs-only `H33` question-selection step
- `docs/plans/2026-03-22-post-h30-h31-r38-extension-plan.md` — preserved execution design packet that fixed the only admitted extension row, the only named boundary probe, the same-opcode-surface rule, and the landed `H32/P18` closeout path
- `results/H32_post_r38_compiled_boundary_refreeze/summary.json` — one-file summary for the current active Origin-core refreeze packet
- `results/H34_post_r39_later_explicit_scope_decision_packet/summary.json` — one-file summary for the current docs-only scope-decision packet freezing the compiled-boundary line complete-for-now
- `results/R39_origin_compiler_control_surface_dependency_audit/summary.json` — one-file summary for the completed same-substrate dependency audit on one declared helper-body permutation
- `results/R38_origin_compiler_control_surface_extension_gate/summary.json` — one-file summary for the completed one-richer compiled control/call-family gate
- `results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json` — one-file summary for the explicit later-extension authorization packet
- `results/H30_post_r36_r37_scope_decision_packet/summary.json` — one-file summary for the preserved prior tiny compiled-boundary refreeze packet
- `results/R37_origin_compiler_boundary_gate/summary.json` — one-file summary for the completed tiny compiled-boundary gate
- `results/R36_origin_long_horizon_precision_scaling_gate/summary.json` — one-file summary for the completed narrow precision-boundary follow-up
- `docs/plans/2026-03-22-post-h23-reauthorization-design.md` — preserved historical design that landed `H24/R30/R31/H25`
- `docs/plans/2026-03-22-post-h25-r32-r33-near-term-design.md` — preserved historical design for the completed `R32 -> H26 -> R33 -> H27` wave
- `tmp/active_wave_plan.md` — short handoff file for the current active wave
- `docs/milestones/H34_post_r39_later_explicit_scope_decision_packet/README.md` — landed docs-only post-`R39` scope-decision packet that keeps `H32` active and selects freeze-complete-for-now
- `docs/milestones/H33_post_h32_conditional_next_question_packet/README.md` — landed docs-only conditional next-question packet that keeps `H32` active and authorizes only `R39`
- `docs/milestones/R39_origin_compiler_control_surface_dependency_audit/README.md` — completed same-substrate dependency audit authorized by `H33`
- `docs/milestones/R39_origin_compiler_control_surface_dependency_audit/execution_manifest.md` — execution manifest for the completed `R39` audit
- `docs/milestones/P18_post_h32_clean_worktree_promotion/worktree_runbook.md` — operational clean-worktree packaging runbook for the completed `H32` closeout wave
- `docs/milestones/P15_internal_claim_and_handoff_sync_after_h25/handoff_notes.md` — preserved internal handoff for the historical `H25` state, downstream lane order, and blocked follow-up paths
- `docs/milestones/R32_d0_family_local_boundary_sharp_zoom/execution_manifest.md` — planning-only first-pass `R32` sharp-zoom manifest fixing the candidate core, ceiling-relative ladder, stop rules, and required outputs
- `docs/milestones/R33_d0_non_retrieval_overhead_localization_audit/component_localization_manifest.md` — planning-only first-pass `R33` attribution manifest fixing the comparator set, stratified audit packet, escalation rule, component targets, and required outputs
- `docs/milestones/F2_future_frontier_recheck_activation_matrix/activation_matrix.md` — planning-only frontier activation matrix tied to the current `H27 -> H32` control chain rather than momentum
- `docs/milestones/F3_post_h23_scope_lift_decision_bundle/decision_gate.md` — planning-only scope-lift gate clarifying that `R32` and deferred `R33` must still precede any later reauthorization discussion
- `docs/milestones/F4_post_h23_origin_claim_delta_matrix/claim_delta_matrix.md` — origin-facing claim delta matrix anchored to frozen `H23` evidence while remaining downstream of `H25`
- `results/H25_refreeze_after_r30_r31_decision_packet/summary.json` — one-file entrypoint for the preserved historical post-`H23` decision packet, primary next lane, deferred audit lane, and preserved blockers
- `results/H23_refreeze_after_r26_r27_r28/summary.json` — one-file entrypoint for the preserved historical post-`H22/R26/R28/R27` same-endpoint state, claim partition, and next-priority lane
- `results/R30_d0_boundary_reauthorization_packet/summary.json` — machine-readable post-`H23` boundary reauthorization packet authorizing the future `R32` family-local sharp zoom
- `results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json` — machine-readable post-`H23` systems reauthorization packet routing later same-endpoint systems work through future `R33`
- `results/H22_post_h21_boundary_reopen_and_dual_track_lock/summary.json` — machine-readable reopen-control packet for the bounded dual-track follow-up
- `results/R26_d0_boundary_localization_execution_gate/summary.json` — machine-readable first-wave boundary scan showing `22/22` exact candidates and no localized failure
- `results/R27_d0_boundary_localization_extension_gate/summary.json` — machine-readable conditional second-wave extension showing `12/12` exact candidates and no localized failure
- `results/R28_d0_trace_retrieval_contract_audit/summary.json` — machine-readable mechanism-contract audit showing support with partial control isolation
- `results/H21_refreeze_after_r22_r23/summary.json` — preserved pre-reopen same-endpoint control state after the landed `R22/R23` follow-up
- `results/H20_post_h19_mainline_reentry_and_hygiene_split/summary.json` — machine-readable reentry guard between `H19` and the preserved `R22/R23/H21` packet
- `results/H19_refreeze_and_next_scope_decision/summary.json` — preserved pre-`R22/R23` frozen same-endpoint control state
- `results/H18_post_h17_mainline_reopen_guard/summary.json` — machine-readable planning guard for the post-`H17` same-scope reopen handoff
- `results/R19_d0_pointer_like_surface_generalization_gate/summary.json` — machine-readable exactness/runtime verdict for the landed `R19` same-endpoint gate
- `results/R19_d0_pointer_like_surface_generalization_gate/manifest_rows.json` — explicit admitted/heldout program matrix for the landed `R19` gate
- `results/R19_d0_pointer_like_surface_generalization_gate/runtime_rows.json` — row-level runtime and exactness matrix for admitted plus heldout `R19` rows
- `results/R20_d0_runtime_mechanism_ablation_matrix/summary.json` — machine-readable mechanism verdict for the landed `R20` bounded ablation lane
- `results/R20_d0_runtime_mechanism_ablation_matrix/runtime_matrix_rows.json` — merged imported-baseline plus measured-control runtime matrix for the landed `R20` sample set
- `results/R21_d0_exact_executor_boundary_break_map/summary.json` — machine-readable bounded boundary-map verdict for the landed `R21` executor scan
- `results/R21_d0_exact_executor_boundary_break_map/branch_summary.json` — per-branch exactness summary for the landed `R21` bounded grid
- `results/H17_refreeze_and_conditional_frontier_recheck/summary.json` — preserved prior same-scope refreeze state for the completed `H16/R15/R16/R17/R18` packet
- `results/H16_post_h15_same_scope_reopen_guard/summary.json` — preserved entrypoint for the completed `H16` active stage and synchronized control surface
- `results/R15_d0_remaining_family_retrieval_pressure_gate/summary.json` — landed remaining-family retrieval-pressure gate on the same fixed `D0` endpoint
- `results/R16_d0_real_trace_precision_boundary_saturation/summary.json` — landed admitted-surface precision saturation follow-up across the merged `R8/R15` same-scope memory surface
- `results/R17_d0_full_surface_runtime_bridge/summary.json` — landed full-surface same-endpoint runtime bridge on the admitted `R8/R15` surface
- `results/R18_d0_same_endpoint_runtime_repair_counterfactual/summary.json` — landed comparator-only `R18` runtime repair packet, with `R18b` closing the focused gate and exact `8/8` confirmation sweep
- `results/H15_refreeze_and_decision_sync/summary.json` — preserved prior `H15` refreeze decision with explicit `R13/R14` status
- `results/H14_core_first_reopen_guard/summary.json` — preserved guard for the completed `H14` core-first reopen packet, preserved `H13/V1` handoff, and standing controls
- `results/H13_post_h12_governance_stage_health/summary.json` — preserved governance/runtime handoff reference for the completed `H13/V1` control stack
- `results/V1_full_suite_validation_runtime_audit/summary.json` — bounded runtime-classification audit for the full-suite validation gate
- `results/V1_full_suite_validation_runtime_timing_followup/summary.json` — bounded top-`6` per-file timing classification for the full-suite validation gate
- `results/release_worktree_hygiene_snapshot/summary.json` — machine-readable snapshot of whether the current worktree blocks a release-facing commit
- `results/release_preflight_checklist_audit/summary.json` — machine-readable outward release-preflight audit over release-facing docs, frozen paper-facing ledgers, and standing summaries
- `results/H10_r7_reconciliation_guard/summary.json` — reconciliation guard for the corrected `R7` top-`4` profile wording
- `results/H11_post_h9_mainline_rollover_guard/summary.json` — driver-alignment guard for the current retrieval-pressure packet under the reopened stage
- `results/R8_d0_retrieval_pressure_gate/summary.json` — completed bounded heavier-family retrieval-pressure gate on the same fixed `D0` endpoint
- `results/R9_d0_real_trace_precision_boundary_companion/summary.json` — completed bounded real-trace precision companion on admitted `R8` memory streams
- `results/R10_d0_same_endpoint_cost_attribution/summary.json` — completed representative-row same-endpoint cost attribution on admitted `R6/R8` rows
- `results/R7_d0_same_endpoint_runtime_bridge/summary.json` — completed same-endpoint runtime bridge on the preserved `8`-family admitted surface with bounded top-`4` profiling
- `results/R6_d0_long_horizon_scaling_gate/summary.json` — completed fixed-multiplier long-horizon exactness gate on current scalable `D0` families
- `results/R3_d0_exact_execution_stress_gate/summary.json` — preserved harder-suite exactness baseline on the current `D0` endpoint
- `results/R4_mechanistic_retrieval_closure/summary.json` — preserved mechanistic-closure baseline on the current positive `D0` suites
- `docs/publication_record/submission_packet_index.md` — venue-agnostic submission/archive handoff
- `docs/publication_record/claim_ladder.md` — claim boundary summary
- `docs/publication_record/claim_evidence_table.md` — artifact-to-claim map
- `docs/publication_record/manuscript_bundle_draft.md` — current manuscript section draft
- `docs/milestones/H25_refreeze_after_r30_r31_decision_packet/` — preserved historical decision-packet staging area
- `docs/milestones/H23_refreeze_after_r26_r27_r28/` — preserved historical frozen scientific-stage staging area
- `docs/milestones/H24_post_h23_reauthorization_and_hygiene_split/` — completed post-`H23` split stage for the preserved historical decision packet
- `docs/milestones/R30_d0_boundary_reauthorization_packet/` — completed post-`H23` boundary reauthorization packet
- `docs/milestones/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/` — completed post-`H23` systems reauthorization packet
- `docs/milestones/R32_d0_family_local_boundary_sharp_zoom/` — authorized future boundary sharp-zoom lane
- `docs/milestones/R33_d0_non_retrieval_overhead_localization_audit/` — deferred future systems-audit lane
- `docs/milestones/H21_refreeze_after_r22_r23/` — preserved pre-reopen frozen-stage staging area
- `docs/milestones/P14_public_surface_sync_after_h23/` — current downstream outward-sync staging area
- `docs/milestones/R29_d0_same_endpoint_systems_recovery_execution_gate/` — blocked future same-endpoint systems recovery lane
- `docs/milestones/F3_post_h23_scope_lift_decision_bundle/` — blocked future scope-lift decision bundle
- `docs/milestones/H17_refreeze_and_conditional_frontier_recheck/` — preserved prior same-scope refreeze staging area
- `docs/milestones/H16_post_h15_same_scope_reopen_and_scope_lock/` — completed reopen/refreeze staging area
- `docs/milestones/H15_refreeze_and_decision_sync/` — preserved prior refreeze staging area
- `docs/milestones/H14_core_first_reopen_and_scope_lock/` — preserved reopen-packet staging area

## Quickstart

The intended workflow uses Python `3.12` and `uv`.

```bash
uv sync --group dev
uv run pytest -q
```

Common export commands:

```bash
uv run python scripts/export_h18_post_h17_mainline_reopen_guard.py
uv run python scripts/export_h19_refreeze_and_next_scope_decision.py
uv run python scripts/export_h16_post_h15_same_scope_reopen_guard.py
uv run python scripts/export_r15_d0_remaining_family_retrieval_pressure_gate.py
uv run python scripts/export_r16_d0_real_trace_precision_boundary_saturation.py
uv run python scripts/export_r17_d0_full_surface_runtime_bridge.py
uv run python scripts/export_r18_d0_same_endpoint_runtime_repair_counterfactual.py
uv run python scripts/export_r21_d0_exact_executor_boundary_break_map.py
uv run python scripts/export_h17_refreeze_and_conditional_frontier_recheck.py
uv run python scripts/export_h14_core_first_reopen_guard.py
uv run python scripts/export_h15_refreeze_and_decision_sync.py
uv run python scripts/export_h10_r7_reconciliation_guard.py
uv run python scripts/export_h11_post_h9_mainline_rollover_guard.py
uv run python scripts/export_h8_driver_replacement_guard.py
uv run python scripts/export_h6_mainline_rollover_guard.py
uv run python scripts/export_v1_full_suite_validation_runtime_audit.py
uv run python scripts/export_v1_full_suite_validation_runtime_timing_followup.py
uv run python scripts/export_h13_post_h12_governance_stage_health.py
uv run python scripts/export_release_worktree_hygiene_snapshot.py
uv run python scripts/export_release_preflight_checklist_audit.py
uv run python scripts/export_p5_public_surface_sync.py
uv run python scripts/export_h2_bundle_lock_audit.py
uv run python scripts/export_p10_submission_archive_ready.py
```

## Repository Layout

- `docs/` — milestone logs, plans, claim ledgers, publication notes
- `src/` — geometry, trace execution, model branches, typed-bytecode harness
- `scripts/` — export and rendering entrypoints
- `tests/` — regression and artifact tests
- `results/` — tracked benchmark summaries and milestone outputs

## Public Material Policy

`docs/Origin/` and `docs/origin/` contain local-only source material and stay
out of version control. The public repository stores derived notes, code,
benchmark outputs, claim ledgers, and explicit accounting of what was and was
not reproduced.
