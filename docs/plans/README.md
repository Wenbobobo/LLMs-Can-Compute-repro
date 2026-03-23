# Plans Index

This directory stores planning-only design documents, unattended master plans,
and packet-specific handoff notes. These files are routing aids, not
claim-bearing evidence. When a plan and a landed result differ, trust the
current stage driver, the milestone/result artifacts, and the machine-readable
`results/` summaries first.

## Current Start Points

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
- `../milestones/H38_post_f16_runtime_relevance_reopen_decision_packet/` —
  current active docs-only decision packet.
- `../milestones/H36_post_r40_bounded_scalar_family_refreeze/` — preserved
  active routing/refreeze packet for the bounded-scalar same-substrate wave.
- `../milestones/P26_post_h37_promotion_and_artifact_hygiene_audit/` —
  completed operational promotion/artifact audit lane.
- `../milestones/F16_post_h37_r41_candidate_isolation_bundle/` — current
  candidate-isolation bundle for the saved `R41` catalog.
- `../milestones/F17_post_h38_same_substrate_exit_criteria_bundle/` —
  current planning-only route-selection bundle after `H38`.
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

- `2026-03-23-*` — current post-`H34`, post-`P23`, and post-`H36` design set
  for the Origin-core line.
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
saved plan and the landed `H38/H36/P26/F16/F17/H37/P25/F15/H35/P24/R40` stack
differ, trust the landed packet.
