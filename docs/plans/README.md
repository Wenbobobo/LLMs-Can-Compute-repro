# Plans Index

This directory stores planning-only design documents, unattended master plans,
and packet-specific handoff notes. These files are routing aids, not
claim-bearing evidence. When a plan and a landed result differ, trust the
current stage driver, the milestone/result artifacts, and the machine-readable
`results/` summaries first.

## Current Start Points

- `2026-03-24-post-h49-origin-core-next-wave-design.md` — the current saved
  post-`H49` next-wave design that fixes the route:
  `F26 -> P36 -> R51 -> R52 -> H50`, while keeping `F27` saved only.
- `2026-03-24-post-h47-p35-f23-mainline-extension-master-plan.md` — the
  current saved post-`H47` master plan that fixes the next wave order:
  `P35` research-record rollup, `F23` numeric-scaling bundle, one narrow
  `R49` runtime gate, and later explicit `H48` stop/go interpretation.
- `2026-03-24-post-h47-p35-research-record-rollup-design.md` — the current
  low-priority operational/docs design surface that records artifact policy,
  root-dirty quarantine, push state, merge posture, and preserved negative
  results after landed `H47`.
- `2026-03-24-post-h47-f23-numeric-scaling-bundle-design.md` — the current
  planning surface for the only admissible post-`H47` runtime question,
  fixing `R49` as the only next runtime candidate while keeping `H47/H43`
  intact.
- `2026-03-24-post-r49-h48-numeric-scaling-decision-design.md` — the
  preserved prior docs-only decision surface that reads completed `R49`,
  records landed `H48`, and authorizes exactly `F25` as the next planning-only
  bundle.
- `2026-03-24-post-h48-f25-restricted-tinyc-lowering-design.md` — the current
  planning surface for the only admissible post-`H48` runtime question,
  fixing `R50` as the only next runtime candidate and `H49` as the only
  follow-up packet while preserving the `R47` useful-case contract first.
- `2026-03-24-post-r50-h49-tinyc-lowering-decision-design.md` — the current
  docs-only decision surface that reads completed `R50`, records `H49` as the
  active interpretation packet, freezes `R50` as narrow exact tiny-`C`
  support only, and restores `no_active_downstream_runtime_lane`.
- `2026-03-24-post-f25-r50-restricted-tinyc-lowering-design.md` — the current
  execution design surface for the landed `R50` restricted tiny-`C` lowering
  gate, preserving `H48/H43`, executing only the admitted single-function
  static `i32` surface, and handing interpretation to `H49`.
- `2026-03-24-post-h47-r49-useful-case-numeric-scaling-design.md` — the
  current execution design surface for the landed `R49` numeric-scaling gate,
  preserving `H47/H43`, executing the fixed three-kernel ladder through the
  saved `F23` buckets, and handing interpretation to `H48`.
- `2026-03-24-post-h43-mainline-reentry-master-plan.md` — the current
  post-`H43` saved master plan that fixes the exact-first reentry wave order:
  `Wave 0` save/fork/reindex, `F21` exact-first planning bundle, `H44`
  docs-only route reauthorization packet, `R46` exact surface-generalization
  gate, conditional `R47`, conditional `R48`, and later low-priority rollup.
- `2026-03-24-post-r48-h47-useful-case-bridge-refreeze-design.md` — the
  preserved prior execution design surface for the landed docs-only `H47`
  refreeze packet that freezes positive comparator-only `R48` narrowly before
  the later completed `H48` decision packet.
- `2026-03-24-post-r47-h46-frontend-bridge-decision-design.md` — the
  preserved prior execution design surface for the landed docs-only `H46`
  interpretation packet that reads completed `R47`, authorizes exactly `R48`,
  and turns `F22` into the current comparator-planning bundle.
- `2026-03-24-post-h46-r48-dual-mode-useful-case-model-design.md` — the
  preserved prior execution design surface for the landed comparator-only
  `R48` useful-case model gate that evaluates both admitted modes on the
  preserved `R47` contract and hands interpretation to `H47`.
- `2026-03-24-post-r46-h45-surface-decision-design.md` — the preserved prior
  execution design surface for the landed docs-only `H45` interpretation
  packet that reads completed `R46`, authorizes exactly `R47`, keeps `F22`
  blocked at that stage, and keeps `R48` deferred behind later explicit
  `H46`.
- `2026-03-24-post-h45-r47-restricted-frontend-translation-design.md` — the
  preserved prior execution design surface for the landed `R47` restricted
  frontend bridge that lowers one structured `i32` / static-memory frontend
  onto the existing useful-case kernels exactly and hands interpretation to
  `H46`.
- `2026-03-24-post-h44-r46-useful-case-surface-generalization-design.md` —
  the preserved prior execution design surface for the landed post-`H44`
  exact held-out useful-case surface-generalization gate and the `H45`
  follow-on interpretation requirement.
- `2026-03-24-post-r42-aggressive-long-arc-master-plan.md` — the current
  post-`R42` saved master plan that fixes the aggressive long-arc wave order:
  `Wave 0` save/push/fork, `F20/H41` control override, `P27` explicit merge
  hygiene, `R43` exact bounded-memory mainline, `R45` dual-mode model
  mainline, later `H42`, and conditional `R44`.
- `2026-03-24-post-r42-f20-h41-control-override-design.md` — the current
  control-override design surface that lands the planning-only `F20` model
  bundle plus the docs-only `H41` aggressive long-arc decision packet above
  completed `R42`.
- `2026-03-24-post-h41-p27-explicit-merge-wave-design.md` — the current
  operational merge-wave design surface that lands `P27`, keeps `main`
  untouched, and precedes the later completed exact `R43` lane.
- `2026-03-24-post-r43-r45-dual-mode-execution-design.md` — the current
  narrow dual-mode execution design surface that maps `R45` onto analytic and
  fitted stack latest-write scorers on the landed `R43` family set.
- `2026-03-24-post-r43-h42-route-selection-design.md` — the current
  route-selection design surface that turns saved `H42` into the completed
  packet authorizing `R44` as the next exact useful-case gate.
- `2026-03-24-post-r44-h43-refreeze-design.md` — the current post-`R44`
  refreeze design surface that turns landed `R44` into the completed current
  narrow useful-case gate and returns the stack to no active downstream
  runtime lane.
- `2026-03-24-post-h43-p31-blog-guardrails-refresh-design.md` — the current
  low-priority blocked-blog/helper guardrail refresh design surface that keeps
  `H43` current while refreshing downstream blog plus manuscript-helper
  guardrails that still freeze the paper-grade endpoint at preserved
  `H32/H34`.
- `2026-03-24-post-h43-p32-historical-wording-refresh-design.md` — the
  completed auxiliary historical/regeneration wording refresh design surface
  that keeps `P31` current while refreshing preserved `H0/P3`
  machine-readable wording that still treats `D0` as the whole current paper
  endpoint.
- `2026-03-24-post-h43-p33-dormant-playbook-wording-refresh-design.md` — the
  completed auxiliary dormant-playbook wording refresh design surface that
  keeps `P31` current while refreshing dormant `E1` playbooks and helper
  historical wording that still speak as though preserved same-endpoint
  `R2/D0` scope were the live paper endpoint.
- `2026-03-24-post-h43-p34-live-surface-wording-guardrail-design.md` — the
  completed auxiliary live-surface wording guardrail design surface that keeps
  `P31` current while adding machine-checkable drift checks on current helper
  and control surfaces.
- `2026-03-24-post-h43-p30-manuscript-surface-refresh-design.md` — the
  completed prior low-priority manuscript-surface refresh design surface that
  moved stale paper-facing prose baselines to the landed `H43` state without
  changing the scientific stage.
- `2026-03-24-post-h43-p29-release-audit-refresh-design.md` — the completed
  prior low-priority release/public audit refresh design surface that updates
  stale downstream audits and the last contradictory release-facing ledgers
  downstream of landed `H43`.
- `2026-03-24-post-h43-p28-publication-surface-sync-design.md` — the
  completed prior low-priority publication/control sync design surface that
  aligned paper-facing ledgers to landed `H43/R44/R45/R43/P27` state without
  changing the scientific stage.
- `2026-03-23-post-h38-f18-f19-long-arc-design.md` — the current post-`H38`
  planning surface that lands `F18/F19` and fixes the saved
  `R42/R43/R44` semantic-boundary gate family.
- `2026-03-23-post-h38-h40-r42-activation-design.md` — the preserved prior
  execution surface that landed the later explicit semantic-boundary
  activation packet plus the completed first retrieval-contract gate,
  `H40 -> R42`.
- `2026-03-23-post-h37-f16-h38-p26-candidate-isolation-design.md` — the
  current control design surface for the landed `F16 -> H38 -> P26 -> F17`
  wave after `H37`.
- `2026-03-23-post-h36-p25-f15-h37-control-design.md` — the current control
  design surface for the preserved prior `P25 -> F15 -> H37` wave after
  `H36`.
- `2026-03-23-post-h36-r41-runtime-relevance-threat-design.md` — the saved
  future design surface for the deferred `R41` runtime-relevance threat lane.
- `2026-03-23-post-p23-h35-r40-bounded-scalar-runtime-design.md` — the
  preserved design surface for the landed bounded-scalar runtime reopen and
  refreeze wave after `P23`.
- `2026-03-23-post-f10-family-first-preactivation-design.md` — the preserved
  design surface for the family-first preactivation wave that landed
  `F12/F13/F14/P23`.
- `2026-03-23-post-r39-later-explicit-scope-decision-design.md` — the
  preserved design surface for the landed post-`R39` docs-only scope decision
  packet, `H34_post_r39_later_explicit_scope_decision_packet`.
- `2026-03-23-post-h33-r39-origin-core-substrate-question-design.md` — the
  preserved design surface that led to the completed post-`H33`
  same-substrate audit, `R39_origin_compiler_control_surface_dependency_audit`.
- `2026-03-23-post-h32-conditional-next-packet-design.md` — the preserved
  post-`H32` planning surface that led to the landed docs-only `H33`
  question-selection packet.
- `2026-03-22-post-h30-h31-r38-extension-plan.md` — the preserved post-`H30`
  execution surface that landed the explicit later decision packet, one richer
  same-substrate extension gate, `H32` refreeze, and `P18` clean closeout.
- `2026-03-22-post-h30-explicit-next-wave-design.md` — the preserved pre-`H31`
  planning surface that required a later explicit packet before any further
  compiled-boundary extension.
- `2026-03-22-post-r36-explicit-next-wave-design.md` — the saved post-`R36`
  explicit-next-wave handoff that led to the landed `R37 -> H30` packet.
- `2026-03-22-post-unattended-r32-mainline-design.md` — preserved historical
  same-endpoint handoff for the earlier `P16 -> R32 -> H26 -> R33/H27` route.
- `2026-03-21-h18-unattended-mainline-master-plan.md` — broad unattended
  master plan for the earlier mainline reproduction program.
- `2026-03-22-post-h23-reauthorization-design.md` — the design that landed the
  preserved prior `H24/R30/R31/H25` reauthorization/refreeze packet.
- `2026-03-22-post-h25-r32-r33-near-term-design.md` — preserved historical
  handoff for `R32` first and deferred `R33` second on the old
  same-endpoint route.

## Use With

- `../publication_record/current_stage_driver.md` — canonical current stage,
  routing order, and standing gates.
- `../../tmp/active_wave_plan.md` — short current-wave handoff and closeout
  notes.
- `../milestones/F26_post_h49_origin_claim_delta_and_next_question_bundle/` —
  current post-`H49` planning-only claim-delta bundle fixing `R51`, `R52`,
  and `H50` while preserving `H49/H43/H36`.
- `../milestones/P36_post_h49_cleanline_hygiene_and_artifact_policy/` —
  current low-priority operational/docs packet fixing cleanline execution
  posture, artifact policy, and no-merge discipline for the post-`H49` wave.
- `../milestones/P35_post_h47_research_record_rollup/` — preserved prior
  low-priority operational/docs rollup packet that records post-`H47` research state,
  hygiene policy, and preserved negative-result accounting without changing
  scientific stage.
- `../milestones/F21_post_h43_exact_useful_case_expansion_bundle/` — current
  exact-first planning bundle that keeps `H43` as the paper-grade endpoint and
  fixes `R46` as the first admissible next runtime candidate.
- `../milestones/H49_post_r50_tinyc_lowering_decision_packet/` — current
  active docs-only interpretation packet that reads completed `R50`,
  preserves `H43` as the paper-grade endpoint, freezes `R50` narrowly, and
  restores `no_active_downstream_runtime_lane`.
- `../milestones/H48_post_r49_numeric_scaling_decision_packet/` — preserved
  prior docs-only interpretation packet that reads completed `R49`,
  preserves `H43` as the paper-grade endpoint, and authorizes exactly `F25`.
- `../milestones/H47_post_r48_useful_case_bridge_refreeze/` — preserved prior
  docs-only interpretation packet that freezes landed comparator-only `R48`
  narrowly before the later completed `H48` decision.
- `../milestones/H46_post_r47_frontend_bridge_decision_packet/` — preserved
  prior docs-only interpretation packet that reads completed `R47`,
  authorizes the landed `R48` lane, and keeps `F22` current without widening
  the paper-grade endpoint.
- `../milestones/H45_post_r46_surface_decision_packet/` — preserved prior
  docs-only interpretation packet that reads completed `R46`, authorizes
  exactly `R47`, and keeps `F22/R48` explicit at that stage.
- `../milestones/H44_post_h43_route_reauthorization_packet/` — preserved prior
  docs-only route reauthorization packet that preserves `H43` and authorizes
  completed `R46`.
- `../milestones/R46_origin_useful_case_surface_generalization_gate/` —
  completed preserved prior post-`H44` exact runtime gate that keeps `8/8`
  held-out in-surface variants exact across the fixed `3/3` useful-case
  kernels.
- `../milestones/F22_post_r46_useful_case_model_bridge_bundle/` — current
  comparator-planning bundle downstream of exact frontend evidence and active
  `H47`.
- `../milestones/F23_post_h47_numeric_scaling_bundle/` — current post-`H47`
  planning-only numeric-scaling bundle fixing `R49` as the only next runtime
  candidate while keeping `F24` dormant.
- `../milestones/F25_post_h48_restricted_tinyc_lowering_bundle/` — completed
  current post-`H48` planning-only bundle selected by completed `H48` that
  fixed `R50` and `H49`.
- `../milestones/R50_origin_restricted_tinyc_lowering_gate/` — completed
  current restricted tiny-`C` lowering gate downstream of completed `F25`,
  preserving `8/8` exact admitted variants across the fixed `3/3` useful-case
  kernels and fixing `H49` as the next required packet.
- `../milestones/H49_post_r50_tinyc_lowering_decision_packet/` — current
  active docs-only follow-up packet after completed `R50`.
- `../milestones/R49_origin_useful_case_numeric_scaling_gate/` — completed
  current numeric-scaling gate downstream of completed `F23` and before
  landed `H48`.
- `../milestones/R47_origin_restricted_frontend_translation_gate/` —
  completed current exact frontend bridge lane that now underwrites landed
  `R48`.
- `../milestones/R48_origin_dual_mode_useful_case_model_gate/` — completed
  current comparator-only useful-case model gate on the preserved `R47`
  contract.
- `../milestones/P32_post_h43_historical_wording_refresh/` — completed
  auxiliary historical/regeneration wording refresh packet that keeps `P31`
  current while refreshing preserved `H0/P3` regeneration-facing wording.
- `../milestones/P33_post_h43_dormant_playbook_wording_refresh/` —
  completed auxiliary dormant-playbook wording refresh packet that keeps
  `P31` current while refreshing dormant `E1` playbook and helper wording.
- `../milestones/P34_post_h43_live_surface_wording_guardrail/` — completed
  auxiliary live-surface wording guardrail packet that keeps `P31` current
  while machine-checking current helper/control surfaces.
- `../milestones/H43_post_r44_useful_case_refreeze/` — preserved prior
  useful-case refreeze packet and current paper-grade endpoint that records
  `R44` as completed narrow useful-case evidence and restores
  `no_active_downstream_runtime_lane`.
- `../milestones/P30_post_h43_manuscript_surface_refresh/` — completed prior
  low-priority operational manuscript-surface refresh packet that aligned
  stale paper-facing prose baselines and derivative helper docs to landed
  `H43`.
- `../milestones/P29_post_h43_release_audit_refresh/` — completed prior
  low-priority operational release/public audit refresh packet that aligned
  stale downstream audits and release-facing ledgers to landed `H43`.
- `../milestones/P28_post_h43_publication_surface_sync/` — completed
  low-priority operational publication/control sync packet that aligned
  paper-facing ledgers to the landed `H43` state.
- `../milestones/H42_post_r43_route_selection_packet/` — preserved prior
  docs-only route-selection packet that authorized `R44` explicitly.
- `../milestones/H41_post_r42_aggressive_long_arc_decision_packet/` —
  preserved prior docs-only aggressive-long-arc decision packet.
- `../milestones/H36_post_r40_bounded_scalar_family_refreeze/` — preserved
  active routing/refreeze packet for the bounded-scalar same-substrate wave.
- `../milestones/R42_origin_append_only_memory_retrieval_contract_gate/` —
  completed current retrieval-contract gate on the semantic-boundary route.
- `../milestones/F20_post_r42_dual_mode_model_mainline_bundle/` — current
  planning-only coequal-mainline model bundle above completed `R42`.
- `../milestones/P26_post_h37_promotion_and_artifact_hygiene_audit/` —
  completed operational promotion/artifact audit lane.
- `../milestones/P27_post_h41_clean_promotion_and_explicit_merge_packet/` —
  completed operational explicit merge packet for the post-`R42` override.
- `../milestones/P31_post_h43_blog_guardrails_refresh/` — completed prior
  low-priority operational blocked-blog/helper guardrail refresh packet
  downstream of `H43`.
- `../milestones/P32_post_h43_historical_wording_refresh/` — completed
  auxiliary historical/regeneration wording refresh packet downstream of
  `H43`.
- `../milestones/P33_post_h43_dormant_playbook_wording_refresh/` — completed
  auxiliary dormant-playbook wording refresh packet downstream of `H43`.
- `../milestones/P34_post_h43_live_surface_wording_guardrail/` — completed
  auxiliary live-surface wording guardrail packet downstream of `H43`.
- `../milestones/P30_post_h43_manuscript_surface_refresh/` — completed prior
  low-priority operational manuscript-surface refresh packet downstream of
  `H43`.
- `../milestones/P29_post_h43_release_audit_refresh/` — completed earlier prior
  low-priority operational release/public audit refresh packet downstream of
  `H43`.
- `../milestones/P28_post_h43_publication_surface_sync/` — completed
  operational publication/control sync packet downstream of `H43`.
- `../milestones/F16_post_h37_r41_candidate_isolation_bundle/` — current
  candidate-isolation bundle for the saved `R41` catalog.
- `../milestones/F17_post_h38_same_substrate_exit_criteria_bundle/` —
  current planning-only route-selection bundle after `H38`.
- `../milestones/F18_post_h38_origin_core_long_arc_bundle/` — current
  planning-only long-arc bundle above the `H38` keep-freeze state.
- `../milestones/F19_post_f18_restricted_wasm_useful_case_roadmap/` —
  current planning-only semantic-boundary roadmap for the preserved `F9`
  family.
- `../milestones/H40_post_h38_semantic_boundary_activation_packet/` —
  preserved prior semantic-boundary activation packet.
- `../milestones/H38_post_f16_runtime_relevance_reopen_decision_packet/` —
  preserved prior docs-only keep-freeze decision packet.
- `../milestones/H37_post_h36_runtime_relevance_decision_packet/` — preserved
  prior docs-only runtime-relevance decision packet.
- `../milestones/P25_post_h36_clean_promotion_prep/` — preserved prior
  operational promotion-prep lane.
- `../milestones/F15_post_h36_origin_goal_reanchor_bundle/` — current
  canonical derivative bundle.
- `../milestones/H35_post_p23_bounded_scalar_family_runtime_decision_packet/`
  — preserved prior docs-only control packet that authorized `R40`.
- `../milestones/P24_post_h36_bounded_scalar_runtime_sync/` — preserved prior
  docs-only sync packet for the landed bounded-scalar runtime wave.
- `../milestones/R40_origin_bounded_scalar_locals_and_flags_gate/` —
  completed bounded-scalar runtime gate on the current substrate.
- `../milestones/R41_origin_runtime_relevance_threat_stress_audit/` —
  deferred future runtime-audit lane fixed to the landed `R40` row pair and
  the two surviving threat families.
- `../milestones/R43_origin_bounded_memory_small_vm_execution_gate/` —
  completed current exact bounded-memory small-VM gate downstream of `H41`.
- `../milestones/R45_origin_dual_mode_model_mainline_gate/` — completed
  coequal model lane downstream of `H41/F20`.
- `../milestones/R44_origin_restricted_wasm_useful_case_execution_gate/` —
  completed current restricted-Wasm / tiny-`C` useful-case gate downstream of
  completed `H42`.
- `../milestones/H34_post_r39_later_explicit_scope_decision_packet/` —
  preserved prior docs-only scope-decision packet above `H32`.
- `../milestones/H33_post_h32_conditional_next_question_packet/` — preserved
  docs-only packet above the preserved `H32` refreeze that selected the next
  question.
- `../milestones/R39_origin_compiler_control_surface_dependency_audit/` —
  completed same-substrate dependency audit downstream of `H33`.
- `../milestones/H32_post_r38_compiled_boundary_refreeze/` — preserved earlier
  routing/refreeze packet in the Origin-core line.

## Historical Plan Groups

- `2026-03-24-*` — current post-`R42` aggressive long-arc master-plan,
  post-`H43` mainline-reentry master-plan, control-override, explicit
  merge-wave, dual-mode execution, post-`R43` route-selection, post-`R44`
  useful-case refreeze, and post-`H43` operational sync/audit-refresh/
  manuscript/helper-doc/dormant-playbook/wording-guardrail design set.
- `2026-03-23-*` — current post-`H34`, post-`P23`, post-`H36`, post-`H38`,
  and post-`R42` design set for the Origin-core line.
- `2026-03-21-*` and `2026-03-22-*` — preserved post-`H19`, post-`H21`,
  post-`H23`, post-`H25`, and post-`H30` design stack.
- `2026-03-20-*` — `H10` through `H17`, `R8` through `R18`, and release/control
  audit design set.
- `2026-03-19-*` — `H1` through `H9`, `R3` through `R7`, `P5` through `P10`,
  and early unattended governance/master-plan set.
- `2026-03-17-*` and `2026-03-18-*` — earliest bootstrap, exact hard-max,
  trainable latest-write, and first compiled-boundary planning set.

## Reading Rule

For current work, start with the newest plan in the relevant lane, then confirm
its status against:

1. `../publication_record/current_stage_driver.md`
2. `../../tmp/active_wave_plan.md`
3. the corresponding milestone `README.md` / `status.md`
4. the corresponding `results/<lane>/summary.json`

Do not treat an older plan as authorization to reopen a blocked lane. When a
saved plan and the landed
`H45/H44/H43/H42/H41/F21/F20/R46/H40/R42/H36/P27/P26/F16/F17/F18/F19/H38/H37/P25/F15/H35/P24/R40` stack
differ, trust the landed packet.
