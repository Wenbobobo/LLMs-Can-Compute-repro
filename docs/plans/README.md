# Plans Index

This directory stores planning-only design documents, unattended master plans,
and packet-specific handoff notes. These files are routing aids, not
claim-bearing evidence. When a plan and a landed result differ, trust the
current stage driver, the milestone/result artifacts, and the machine-readable
`results/` summaries first.

## Current Start Points

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
- `../milestones/P31_post_h43_blog_guardrails_refresh/` — current
  low-priority operational blocked-blog/helper guardrail refresh packet that
  updates stale downstream blog plus manuscript-helper controls without
  changing scientific stage.
- `../milestones/P32_post_h43_historical_wording_refresh/` — completed
  auxiliary historical/regeneration wording refresh packet that keeps `P31`
  current while refreshing preserved `H0/P3` regeneration-facing wording.
- `../milestones/H43_post_r44_useful_case_refreeze/` — current active
  docs-only refreeze packet that records `R44` as completed narrow useful-case
  evidence and restores `no_active_downstream_runtime_lane`.
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
- `../milestones/P31_post_h43_blog_guardrails_refresh/` — current low-priority
  operational blocked-blog/helper guardrail refresh packet downstream of
  `H43`.
- `../milestones/P32_post_h43_historical_wording_refresh/` — completed
  auxiliary historical/regeneration wording refresh packet downstream of
  `H43`.
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
  control-override, explicit merge-wave, dual-mode execution, post-`R43`
  route-selection, post-`R44` useful-case refreeze, and post-`H43`
  operational sync/audit-refresh/manuscript/helper-doc design set.
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
`H43/H42/H41/F20/H40/R42/H36/P27/P26/F16/F17/F18/F19/H38/H37/P25/F15/H35/P24/R40` stack
differ, trust the landed packet.
