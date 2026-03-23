# Milestones Index

This directory stores milestone-local staging areas, result digests, and
planning bundles. Read the current driver first, not the directory name alone.

## Reading Order

1. `../publication_record/current_stage_driver.md`
2. `../../tmp/active_wave_plan.md`
3. the relevant milestone `README.md` / `status.md`
4. the matching `results/<lane>/summary.json`

## Current Top Of Stack

- `H34_post_r39_later_explicit_scope_decision_packet/` — current docs-only
  control packet that keeps `H32` active while selecting
  `freeze_compiled_boundary_as_complete_for_now`.
- `H32_post_r38_compiled_boundary_refreeze/` — current active routing/refreeze
  packet.
- `H33_post_h32_conditional_next_question_packet/` — preserved prior docs-only
  control packet that selected the one justified next question.
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

## Current Downstream Lanes

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

## Completed Current-Wave Closeout

- `P17_h30_commit_hygiene_and_clean_worktree_promotion/` — completed docs-only
  closeout and clean-worktree packet-promotion lane before the later explicit
  packet.
- `P18_post_h32_clean_worktree_promotion/` — completed clean-branch closeout
  and promotion lane for the landed `H31/R38/H32` packet.
- `P19_post_h32_publication_surface_alignment/` — completed docs-only
  publication/control alignment after the saved post-`H32` planning surface.
- `P20_post_h34_manuscript_narrative_resync/` — completed docs-only manuscript
  and helper-doc resync so the paper-facing bundle now terminates on
  `R37 -> H30 -> H31 -> R38 -> H32 -> H33 -> R39 -> H34`.
- `P21_post_h34_planning_surface_sync/` — completed docs-only planning-surface
  sync that recorded `F7/F8` as the first admissible follow-on surfaces while
  keeping runtime inactive.
- `P22_post_f10_planning_surface_sync/` — completed docs-only planning-surface
  sync that records `F10` as the current planning-only bridge surface while
  keeping `F9` blocked, `F11` new-substrate, and runtime inactive.

## Current Planning-Only Follow-ons

- `F7_post_h34_reopen_trigger_specification_bundle/` — planning-only bundle
  that turns future same-substrate reopen admissibility into one mechanical
  contradiction-packet specification.
- `F8_post_h34_beyond_origin_bridge_roadmap/` — planning-only bundle that maps
  the broader Origin-facing scientific vision into saved future milestone
  families without authorizing them now.
- `F10_post_h34_executor_value_comparator_matrix/` — planning-only bridge
  bundle that makes richer executor-visible value and comparator obligations
  explicit without authorizing runtime widening.
- `F9_post_h34_restricted_wasm_semantic_boundary_roadmap/` — inactive roadmap
  storage for a later restricted-Wasm semantic-boundary family that remains
  blocked even after `F10`.
- `F11_post_h34_hybrid_planner_executor_bridge_roadmap/` — inactive roadmap
  storage for a later planner-plus-executor interface family that still
  requires a new substrate.

## Conditional Future Lanes

- `../plans/2026-03-23-post-r39-later-explicit-scope-decision-design.md` —
  preserved design surface that led to the landed `H34` scope-decision
  packet.
- `../plans/2026-03-23-post-h33-r39-origin-core-substrate-question-design.md`
  — preserved design surface that led to the completed `R39`
  same-substrate audit.
- `../plans/2026-03-23-post-h32-conditional-next-packet-design.md` — saved
  post-`H32` planning surface that led to the landed docs-only `H33` packet.
- `R39_origin_compiler_control_surface_dependency_audit/` — completed
  same-substrate dependency audit, not an automatic routing change.
- `H34_post_r39_later_explicit_scope_decision_packet/` — completed docs-only
  interpretation packet, not a routing change.
- `../plans/2026-03-22-post-h30-h31-r38-extension-plan.md` — saved plan for
  the landed explicit-extension wave after `H30`.
- no further same-substrate or compiler-boundary extension is active by
  default.
- any later runtime, broader compiled, or frontier lane now requires a new
  contradiction-driven explicit packet.

## Blocked Or Planning-Only Lanes

- `R29_d0_same_endpoint_systems_recovery_execution_gate/` — blocked future
  same-endpoint systems lane.
- `F2_future_frontier_recheck_activation_matrix/` — planning-only frontier
  activation surface.
- `F3_post_h23_scope_lift_decision_bundle/` — blocked scope-lift gate.
- `F4_post_h23_origin_claim_delta_matrix/` — preserved origin-facing delta
  surface.
- `F5_post_h34_contradiction_scout_matrix/` — planning-only post-`H34`
  contradiction scout that currently concludes no reopen candidate survives.
- `F6_post_p20_future_option_matrix/` — planning-only post-`P20/F5` option
  matrix that keeps docs/planning work admissible while leaving runtime
  inactive by default.
- `F7_post_h34_reopen_trigger_specification_bundle/` — planning-only
  contradiction/reopen specification surface under `H34`.
- `F8_post_h34_beyond_origin_bridge_roadmap/` — planning-only beyond-Origin
  roadmap surface under `H34`.
- `F10_post_h34_executor_value_comparator_matrix/` — current planning-only
  bridge surface under `H34`.
- `F9_post_h34_restricted_wasm_semantic_boundary_roadmap/` — blocked roadmap
  storage downstream of `F10`.
- `F11_post_h34_hybrid_planner_executor_bridge_roadmap/` — new-substrate
  roadmap storage downstream of `F10`.

## Current Rule

Do not activate a blocked or historical milestone from momentum. On the current
stack:

- `H32` is active routing.
- `H34` is the current docs-only control packet.
- `H33` is the preserved prior docs-only question-selection packet.
- `H31` and `H30` are preserved upstream decision packets, not the next
  objective.
- `H29` and `H28` are preserved upstream refreeze/pivot evidence.
- `R34`, `R35`, `R36`, `R37`, and `R38` stay frozen as upstream support.
- `R39` is complete as a downstream audit, not an active routing change.
- `F7` and `F8` are preserved planning-only follow-on surfaces, not runtime
  packets.
- `F10` is the current planning-only bridge surface, not a runtime packet.
- `F9` remains blocked roadmap storage and `F11` remains new-substrate roadmap
  storage.
- no active downstream runtime lane exists after `H34`.
- one richer compiled control family still does not authorize broader compiler
  or demo scope lift.
- `R29`, `F3`, and wider frontier/demo claims remain blocked without a new
  plan packet.
