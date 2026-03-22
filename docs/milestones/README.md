# Milestones Index

This directory stores milestone-local staging areas, result digests, and
planning bundles. Read the current driver first, not the directory name alone.

## Reading Order

1. `../publication_record/current_stage_driver.md`
2. `../../tmp/active_wave_plan.md`
3. the relevant milestone `README.md` / `status.md`
4. the matching `results/<lane>/summary.json`

## Current Top Of Stack

- `H30_post_r36_r37_scope_decision_packet/` — current active routing/refreeze
  packet.
- `H29_refreeze_after_r34_r35_origin_core_gate/` — preserved upstream
  Origin-core refreeze packet.
- `H28_post_h27_origin_core_reanchor_packet/` — prior pivot packet that set the
  current Origin-core direction.
- `H27_refreeze_after_r32_r33_same_endpoint_decision/` — preserved closeout of
  the old same-endpoint recovery wave.

## Current Downstream Lanes

- `R34_origin_retrieval_primitive_contract_gate/` — frozen primitive evidence
  under `H29/H30`.
- `R35_origin_append_only_stack_vm_execution_gate/` — frozen exact execution
  evidence under `H29/H30`.
- `R36_origin_long_horizon_precision_scaling_gate/` — completed narrow
  precision-boundary lane.
- `R37_origin_compiler_boundary_gate/` — completed tiny compiled-boundary
  lane.

## Completed Current-Wave Closeout

- `P17_h30_commit_hygiene_and_clean_worktree_promotion/` — completed docs-only
  closeout and clean-worktree packet-promotion lane before any later explicit
  packet.

## Conditional Future Lanes

- `../plans/2026-03-22-post-h30-explicit-next-wave-design.md` — saved planning
  surface for the later explicit packet after `H30`.
- later explicit packet — required before any scope lift after `H30`.
- no compiler-boundary extension is active by default.

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

- `H30` is active routing.
- `H29` and `H28` are preserved upstream refreeze/pivot evidence, not the next
  objective.
- `R34`, `R35`, `R36`, and `R37` stay frozen as upstream support.
- one tiny positive compiled boundary does not authorize broader compiler or
  demo scope lift.
- `R29`, `F3`, and wider frontier/demo claims remain blocked without a later
  explicit packet.
