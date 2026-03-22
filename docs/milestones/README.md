# Milestones Index

This directory stores milestone-local staging areas, result digests, and
planning bundles. Read the current driver first, not the directory name alone.

## Reading Order

1. `../publication_record/current_stage_driver.md`
2. `../../tmp/active_wave_plan.md`
3. the relevant milestone `README.md` / `status.md`
4. the matching `results/<lane>/summary.json`

## Current Top Of Stack

- `H32_post_r38_compiled_boundary_refreeze/` — current active routing/refreeze
  packet.
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

## Completed Current-Wave Closeout

- `P17_h30_commit_hygiene_and_clean_worktree_promotion/` — completed docs-only
  closeout and clean-worktree packet-promotion lane before the later explicit
  packet.
- `P18_post_h32_clean_worktree_promotion/` — completed clean-branch closeout
  and promotion lane for the landed `H31/R38/H32` packet.

## Conditional Future Lanes

- `../plans/2026-03-23-post-h32-conditional-next-packet-design.md` — saved
  post-`H32` planning surface for the next docs-only question-selection packet.
- `H33_post_h32_conditional_next_question_packet/` — planning-only scaffold for
  the conditional next packet after `H32`.
- `../plans/2026-03-22-post-h30-h31-r38-extension-plan.md` — saved plan for
  the landed explicit-extension wave after `H30`.
- no further compiler-boundary extension is active by default.
- any broader compiled or frontier lane now requires a new plan packet.

## Blocked Or Planning-Only Lanes

- `R29_d0_same_endpoint_systems_recovery_execution_gate/` — blocked future
  same-endpoint systems lane.
- `F2_future_frontier_recheck_activation_matrix/` — planning-only frontier
  activation surface.
- `F3_post_h23_scope_lift_decision_bundle/` — blocked scope-lift gate.
- `F4_post_h23_origin_claim_delta_matrix/` — preserved origin-facing delta
  surface.

## Current Rule

Do not activate a blocked or historical milestone from momentum. On the current
stack:

- `H32` is active routing.
- `H31` and `H30` are preserved upstream decision packets, not the next
  objective.
- `H29` and `H28` are preserved upstream refreeze/pivot evidence.
- `R34`, `R35`, `R36`, `R37`, and `R38` stay frozen as upstream support.
- one richer compiled control family still does not authorize broader compiler
  or demo scope lift.
- `R29`, `F3`, and wider frontier/demo claims remain blocked without a new
  plan packet.
