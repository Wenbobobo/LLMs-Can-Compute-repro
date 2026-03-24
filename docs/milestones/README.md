# Milestones Index

This directory stores milestone-local staging areas, result digests, and
planning bundles. Read the current driver first, not the directory name alone.

## Reading Order

1. `../publication_record/current_stage_driver.md`
2. `../../tmp/active_wave_plan.md`
3. the relevant milestone `README.md` / `status.md`
4. the matching `results/<lane>/summary.json`

## Current Top Of Stack

- `H44_post_h43_route_reauthorization_packet/` — current active docs-only
  route reauthorization packet that preserves `H43/H42/H36/F20/P27/R43/R44/R45`,
  incorporates `F21`, and authorizes exactly `R46`.
- `H43_post_r44_useful_case_refreeze/` — preserved prior useful-case refreeze
  packet and current paper-grade endpoint that preserves
  `H42/H36/F20/P27/R43/R44/R45`, records claim `D` as
  `supported_here_narrowly`, and restores `no_active_downstream_runtime_lane`.
- `H42_post_r43_route_selection_packet/` — preserved prior docs-only
  route-selection packet that preserves `H41/H36/F20/P27/R43/R45` and
  authorizes exact `R44`.
- `H41_post_r42_aggressive_long_arc_decision_packet/` — preserved prior
  docs-only decision packet that preserved completed `R42`, authorized exact
  `R43`, and admitted coequal model `R45` under an explicit evidence boundary.
- `H36_post_r40_bounded_scalar_family_refreeze/` — preserved active
  routing/refreeze packet freezing the bounded-scalar family narrowly on the
  current substrate.
- `R42_origin_append_only_memory_retrieval_contract_gate/` — completed current
  retrieval-contract gate validating exact latest-write-by-address and
  stack-slot retrieval on fixed semantic-boundary tasks.
- `R43_origin_bounded_memory_small_vm_execution_gate/` — completed current
  bounded-memory small-VM exact gate validating five fixed families end-to-end.
- `R44_origin_restricted_wasm_useful_case_execution_gate/` — completed current
  restricted-Wasm / tiny-`C` useful-case gate validating the fixed
  three-kernel ladder exactly on the same append-only substrate.
- `R45_origin_dual_mode_model_mainline_gate/` — completed current coequal
  model gate evaluating both admitted model modes on the landed `R43`
  contract family.
- `R46_origin_useful_case_surface_generalization_gate/` — completed current
  post-`H44` exact runtime gate validating held-out in-surface generalization
  on `8/8` variants across the fixed `3/3` useful-case kernels.
- `P27_post_h41_clean_promotion_and_explicit_merge_packet/` — completed
  operational explicit merge packet for the clean post-`H41` stack.
- `P31_post_h43_blog_guardrails_refresh/` — current low-priority
  operational blocked-blog/helper guardrail refresh packet updating stale
  downstream blog plus manuscript-helper controls without changing scientific
  stage.
- `P32_post_h43_historical_wording_refresh/` — completed auxiliary
  historical/regeneration wording refresh packet updating preserved `H0/P3`
  machine-readable wording without changing scientific stage or displacing
  `P31`.
- `P33_post_h43_dormant_playbook_wording_refresh/` — completed auxiliary
  dormant-playbook wording refresh packet updating dormant `E1` playbooks and
  helper historical wording without changing scientific stage or displacing
  `P31`.
- `P34_post_h43_live_surface_wording_guardrail/` — completed auxiliary
  live-surface wording guardrail packet adding machine-checkable drift guards
  on current helper/control surfaces without changing scientific stage or
  displacing `P31`.
- `P30_post_h43_manuscript_surface_refresh/` — completed prior low-priority
  operational manuscript-surface refresh packet updating stale paper-facing
  prose baselines and derivative helper docs without changing scientific
  stage.
- `P29_post_h43_release_audit_refresh/` — completed earlier prior low-priority
  operational release/public audit refresh packet updating stale downstream
  audits and the last contradictory release-facing ledgers without changing
  scientific stage.
- `P28_post_h43_publication_surface_sync/` — completed prior low-priority
  operational publication/control sync packet aligning paper-facing ledgers to
  the landed `H43` state without changing scientific stage.
- `F20_post_r42_dual_mode_model_mainline_bundle/` — current planning-only
  coequal-mainline model bundle fixing the exact-versus-model evidence
  boundary and dual implementation posture.
- `F21_post_h43_exact_useful_case_expansion_bundle/` — current planning-only
  exact-first post-`H43` bundle fixing `R46` as the first admissible next
  runtime candidate while keeping `R47/R48` conditional.
- `P26_post_h37_promotion_and_artifact_hygiene_audit/` — completed
  preserved prior operational promotion/artifact audit lane from the earlier
  clean branch.
- `F18_post_h38_origin_core_long_arc_bundle/` — current planning-only
  long-arc bundle fixing the post-`H38` claim ladder, preferred route, and
  worktree/merge policy.
- `F19_post_f18_restricted_wasm_useful_case_roadmap/` — current planning-only
  semantic-boundary roadmap that turns the preserved `F9` family into a
  decision-complete restricted-Wasm / useful-case surface.
- `H45_post_r46_surface_decision_packet/` — saved next docs-only decision
  packet that interprets landed `R46` before any frontend/model widening.
- `R47_origin_restricted_frontend_translation_gate/` — conditional future
  exact frontend bridge lane, downstream of positive `R46`.
- `R48_origin_dual_mode_useful_case_model_gate/` — conditional future
  comparator-only model lane on the preserved useful-case contract.
- `H40_post_h38_semantic_boundary_activation_packet/` — preserved prior
  semantic-boundary activation packet above `H38`.
- `F16_post_h37_r41_candidate_isolation_bundle/` — current candidate-
  isolation bundle for the saved `R41` catalog.
- `F17_post_h38_same_substrate_exit_criteria_bundle/` — current planning-only
  route-selection bundle after `H38`.
- `H38_post_f16_runtime_relevance_reopen_decision_packet/` — preserved prior
  docs-only keep-freeze decision packet above `H36`.
- `H37_post_h36_runtime_relevance_decision_packet/` — preserved prior docs-
  only runtime-relevance decision packet.
- `P25_post_h36_clean_promotion_prep/` — preserved prior clean
  promotion-prep lane from the real source-of-truth branch.
- `F15_post_h36_origin_goal_reanchor_bundle/` — current canonical
  origin-facing derivative bundle after the bounded-scalar wave.
- `H35_post_p23_bounded_scalar_family_runtime_decision_packet/` — preserved
  prior docs-only control packet that authorized exactly one bounded-scalar
  runtime gate.
- `P24_post_h36_bounded_scalar_runtime_sync/` — preserved prior docs-only
  control-surface sync after the landed `H35/R40/H36` wave.
- `H34_post_r39_later_explicit_scope_decision_packet/` — preserved earlier
  docs-only control packet that froze the compiled-boundary line
  complete-for-now before the bounded-scalar reopen.
- `H32_post_r38_compiled_boundary_refreeze/` — preserved earlier active
  compiled-boundary refreeze packet.
- `H33_post_h32_conditional_next_question_packet/` — preserved earlier
  docs-only control packet that selected the one justified next question.
- `H31_post_h30_later_explicit_boundary_decision_packet/` — preserved explicit
  authorization packet between `H30` and `R38`.
- `H30_post_r36_r37_scope_decision_packet/` — preserved prior compiled-boundary
  refreeze packet.
- `H29_refreeze_after_r34_r35_origin_core_gate/` — preserved upstream
  Origin-core refreeze packet.
- `H28_post_h27_origin_core_reanchor_packet/` — prior pivot packet that set the
  current Origin-core direction.
- `H27_refreeze_after_r32_r33_same_endpoint_decision/` — preserved closeout of
  the old same-endpoint recovery wave.

## Current Downstream Evidence Lanes

- `R34_origin_retrieval_primitive_contract_gate/` — frozen primitive evidence
  under `H29/H32`.
- `R35_origin_append_only_stack_vm_execution_gate/` — frozen exact execution
  evidence under `H29/H32`.
- `R36_origin_long_horizon_precision_scaling_gate/` — completed narrow
  precision-boundary lane.
- `R37_origin_compiler_boundary_gate/` — completed tiny compiled-boundary
  lane.
- `R38_origin_compiler_control_surface_extension_gate/` — completed richer
  compiled control-surface lane on the same opcode surface.
- `R39_origin_compiler_control_surface_dependency_audit/` — completed
  same-substrate dependency audit on one declared helper-body permutation with
  target renumbering; it preserves narrow scope and does not change routing by
  itself.
- `R40_origin_bounded_scalar_locals_and_flags_gate/` — completed bounded-
  scalar same-substrate runtime gate validating explicit frame locals plus
  typed `FLAG` slots on the same opcode surface.
- `R42_origin_append_only_memory_retrieval_contract_gate/` — completed
  semantic-boundary retrieval-contract gate validating exact value and
  maximizer-row identity on six fixed task families.
- `R43_origin_bounded_memory_small_vm_execution_gate/` — completed exact
  bounded-memory small-VM gate validating five fixed families without widening
  the admitted substrate.
- `R45_origin_dual_mode_model_mainline_gate/` — completed coequal model gate
  validating two admitted model modes on the same bounded-memory contract.

## Completed Current-Wave Closeout

- `P17_h30_commit_hygiene_and_clean_worktree_promotion/` — completed docs-only
  closeout and clean-worktree packet-promotion lane before the later explicit
  packet.
- `P18_post_h32_clean_worktree_promotion/` — completed clean-branch closeout
  and promotion lane for the landed `H31/R38/H32` packet.
- `P19_post_h32_publication_surface_alignment/` — completed docs-only
  publication/control alignment after the saved post-`H32` planning surface.
- `P20_post_h34_manuscript_narrative_resync/` — completed docs-only manuscript
  and helper-doc resync so the paper-facing bundle terminates on
  `R37 -> H30 -> H31 -> R38 -> H32 -> H33 -> R39 -> H34`.
- `P21_post_h34_planning_surface_sync/` — completed docs-only planning-surface
  sync that recorded `F7/F8` as the first admissible follow-on surfaces while
  keeping runtime inactive.
- `P22_post_f10_planning_surface_sync/` — completed prior docs-only
  planning-surface sync for the `F10` bridge wave.
- `P23_post_f13_planning_surface_sync/` — completed docs-only planning-surface
  sync that recorded `F12/F13/F14` while keeping `F9` blocked, `F11`
  new-substrate, and runtime inactive.
- `P24_post_h36_bounded_scalar_runtime_sync/` — completed docs-only sync that
  recorded `H36` as active and no active downstream runtime lane after `R40`.
- `P25_post_h36_clean_promotion_prep/` — completed operational prep that fixes
  the clean promotion branch, source-of-truth inventory, and no-merge rule.
- `P26_post_h37_promotion_and_artifact_hygiene_audit/` — completed
  operational audit that records packet split, branch posture, and large-
  artifact policy above `H38`.
- `P27_post_h41_clean_promotion_and_explicit_merge_packet/` — completed
  operational merge packet that stages explicit merge posture without merging
  `main`.
- `P31_post_h43_blog_guardrails_refresh/` — current low-priority operational
  blocked-blog/helper guardrail refresh packet that keeps `H43` current while
  refreshing stale downstream blog plus manuscript-helper controls.
- `P32_post_h43_historical_wording_refresh/` — completed auxiliary
  historical/regeneration wording refresh packet that keeps `P31` current
  while refreshing preserved `H0/P3` regeneration-facing wording.
- `P33_post_h43_dormant_playbook_wording_refresh/` — completed auxiliary
  dormant-playbook wording refresh packet that keeps `P31` current while
  refreshing dormant `E1` playbook and helper historical wording.
- `P34_post_h43_live_surface_wording_guardrail/` — completed auxiliary
  live-surface wording guardrail packet that keeps `P31` current while
  machine-checking current helper/control surfaces.
- `P30_post_h43_manuscript_surface_refresh/` — completed prior operational
  manuscript-surface refresh packet that keeps `H43` current while refreshing
  stale paper-facing prose baselines and derivative helper docs.
- `P29_post_h43_release_audit_refresh/` — completed earlier prior operational
  release/public audit refresh packet that keeps `H43` current while
  refreshing stale downstream audits and release ledgers.
- `P28_post_h43_publication_surface_sync/` — completed operational
  publication/control sync packet that keeps `H43` current while aligning
  paper-facing ledgers downstream of landed evidence.

## Current Planning And Deferred Follow-Ons

- `F15_post_h36_origin_goal_reanchor_bundle/` — current canonical
  origin-facing derivative bundle anchored to the landed bounded-scalar state.
- `F16_post_h37_r41_candidate_isolation_bundle/` — current planning-only
  candidate-isolation bundle for the saved `R41` catalog.
- `F17_post_h38_same_substrate_exit_criteria_bundle/` — current planning-only
  route-selection bundle after the `H38` keep-freeze decision.
- `F18_post_h38_origin_core_long_arc_bundle/` — current planning-only
  long-arc bundle fixing the post-`H38` claim ladder, preferred route, and
  worktree/merge policy.
- `F19_post_f18_restricted_wasm_useful_case_roadmap/` — current planning-only
  semantic-boundary roadmap that turns the preserved `F9` family into a
  decision-complete restricted-Wasm / useful-case surface.
- `F14_post_f13_conditional_reopen_readiness_bundle/` — preserved planning-only
  bundle that stores one future contradiction-driven packet blueprint and one
  future runtime-audit blueprint without authorizing either one.
- `../plans/2026-03-23-post-h36-r41-runtime-relevance-threat-design.md` —
  saved future design surface for the deferred
  `R41_origin_runtime_relevance_threat_stress_audit` lane.
- `R41_origin_runtime_relevance_threat_stress_audit/` — deferred future
  same-substrate runtime-audit lane fixed to the two landed `R40` rows, the
  two surviving `F14` threat families, and explicit stop rules.
- `F7_post_h34_reopen_trigger_specification_bundle/` — planning-only bundle
  that turns future same-substrate reopen admissibility into one mechanical
  contradiction-packet specification.
- `F8_post_h34_beyond_origin_bridge_roadmap/` — planning-only bundle that maps
  the broader Origin-facing scientific vision into saved future milestone
  families without authorizing them now.
- `F10_post_h34_executor_value_comparator_matrix/` — planning-only bridge
  bundle that makes richer executor-visible value and comparator obligations
  explicit without authorizing runtime widening.
- `F12_post_f10_origin_claim_delta_reanchor_bundle/` — preserved historical
  canonical derivative surface for the earlier `H34/F10/P22` control state.
- `F13_post_f12_bounded_scalar_value_family_spec/` — preserved planning-only
  bounded family-first preactivation bundle for `bounded scalar locals and flags`.
- `F9_post_h34_restricted_wasm_semantic_boundary_roadmap/` — inactive default-
  forward roadmap storage for a later restricted-Wasm semantic-boundary family.
- `F11_post_h34_hybrid_planner_executor_bridge_roadmap/` — inactive roadmap
  storage for a later planner-plus-executor interface family that still
  requires a new substrate.

## Blocked Or Historical Lanes

- `R29_d0_same_endpoint_systems_recovery_execution_gate/` — blocked future
  same-endpoint systems lane.
- `F2_future_frontier_recheck_activation_matrix/` — planning-only frontier
  activation surface.
- `F3_post_h23_scope_lift_decision_bundle/` — blocked scope-lift gate.
- `F4_post_h23_origin_claim_delta_matrix/` — preserved historical
  origin-facing delta surface superseded first by `F12` and now by `F15`.
- `F5_post_h34_contradiction_scout_matrix/` — planning-only contradiction
  scout concluding no reopen candidate survives on the current evidence.
- `F6_post_p20_future_option_matrix/` — planning-only option matrix keeping
  docs/planning work admissible while runtime remains inactive by default.

## Current Rule

Do not activate a blocked or historical milestone from momentum. On the current
stack:

- `H44` is the active docs-only decision packet.
- `H43` is the preserved prior useful-case refreeze packet and current
  paper-grade endpoint.
- `H42` is the preserved earlier docs-only route-selection packet.
- `H41` is the preserved earlier docs-only aggressive-long-arc packet.
- `H36` is the preserved active routing/refreeze packet.
- `R42` is the completed current retrieval-contract gate underneath `H41`.
- `F20` is the current coequal-mainline model bundle.
- `F21` is the current exact-first post-`H43` planning bundle.
- `P27` is the completed operational explicit merge packet and keeps
  `merge_executed = false`.
- `P26` is the preserved prior operational promotion/artifact audit lane, not
  merge authorization.
- `F16` is the current candidate-isolation bundle.
- `F17` is the current planning-only route-selection bundle.
- `F18` is the current planning-only long-arc bundle.
- `F19` is the current planning-only semantic-boundary roadmap.
- `H40` is the preserved prior semantic-boundary activation packet.
- `H38` is the preserved prior docs-only decision packet.
- `H37` is the preserved prior docs-only runtime-relevance decision packet.
- `P25` is the preserved prior operational promotion-prep lane.
- `F15` is the current canonical derivative claim-delta surface.
- `H35` is the preserved prior docs-only control packet.
- `P24` is the preserved prior docs-only sync packet.
- `H34` and `H33` are preserved earlier docs-only packets.
- `H31` and `H30` are preserved upstream decision packets, not the next
  objective.
- `H29` and `H28` are preserved upstream refreeze/pivot evidence.
- `R34`, `R35`, `R36`, `R37`, and `R38` stay frozen as upstream support.
- `R39` and `R40` are complete downstream audits/gates, not active routing
  changes by themselves.
- `R41` is a deferred future runtime-audit design, not active work.
- `R43` is the completed current exact semantic-boundary gate.
- `R45` is the completed current coequal model lane under the `F20` evidence
  rule.
- `R44` is the completed current restricted useful-case gate.
- `R46` is the completed current post-`H44` exact runtime gate.
- `H45` is the next required docs-only interpretation packet.
- `no_active_downstream_runtime_lane` remains the landed `H43` closeout.
- `F12`, `F13`, and `F14` are preserved historical or planning surfaces, not
  runtime packets.
- `F9` remains the default forward semantic-boundary roadmap and `F11`
  remains new-substrate roadmap storage.
- `R43` and `R45` are now both completed; model evidence still remains
  downstream of the landed exact `R43` contract set.
- `R29`, `F3`, and wider frontier/demo claims remain blocked without a new
  explicit packet.
