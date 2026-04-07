# Commit Split Manifest

## Summary

`P16` should prefer the narrowest self-contained split that preserves
`H25 active / H23 frozen` semantics. Use one commit only if the full subset is
small and coherent. Otherwise split into the two packets below.

## Packet 1: `post-h23-core-packet`

Include this packet if the repository does not already contain the post-`H23`
core control/docs/results as committed history.

Recommended paths:

- `STATUS.md`
- `docs/publication_record/README.md`
- `docs/publication_record/current_stage_driver.md`
- `docs/publication_record/release_preflight_checklist.md`
- `docs/plans/2026-03-22-post-h23-reauthorization-design.md`
- `docs/plans/2026-03-22-post-h25-r32-r33-near-term-design.md`
- `docs/plans/README.md`
- `docs/milestones/README.md`
- `docs/milestones/H24_post_h23_reauthorization_and_hygiene_split/`
- `docs/milestones/H25_refreeze_after_r30_r31_decision_packet/`
- `docs/milestones/R30_d0_boundary_reauthorization_packet/`
- `docs/milestones/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/`
- `docs/milestones/R32_d0_family_local_boundary_sharp_zoom/`
- `docs/milestones/R33_d0_non_retrieval_overhead_localization_audit/`
- `results/H23_refreeze_after_r26_r27_r28/`
- `results/H25_refreeze_after_r30_r31_decision_packet/`
- `results/R30_d0_boundary_reauthorization_packet/`
- `results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/`
- `scripts/export_h23_refreeze_after_r26_r27_r28.py`
- `scripts/export_h25_refreeze_after_r30_r31_decision_packet.py`
- `scripts/export_r30_d0_boundary_reauthorization_packet.py`
- `scripts/export_r31_d0_same_endpoint_systems_recovery_reauthorization_packet.py`
- `tests/test_export_h23_refreeze_after_r26_r27_r28.py`
- `tests/test_export_h25_refreeze_after_r30_r31_decision_packet.py`
- `tests/test_export_r30_d0_boundary_reauthorization_packet.py`
- `tests/test_export_r31_d0_same_endpoint_systems_recovery_reauthorization_packet.py`

Exclude from this packet:

- `results/release_worktree_hygiene_snapshot/*`
- `results/release_preflight_checklist_audit/*`
- `results/P5_public_surface_sync/*`
- `P15/P16` handoff-only closeout docs unless needed for self-containment

## Packet 2: `h25-closeout-audits`

Use this narrower packet for the actual closeout wording, preflight logic, and
state-dependent outputs.

Recommended paths:

- `README.md`
- `tmp/active_wave_plan.md`
- `docs/publication_record/release_summary_draft.md`
- `docs/milestones/P15_internal_claim_and_handoff_sync_after_h25/`
- `docs/milestones/P16_h25_commit_hygiene_and_clean_worktree_promotion/`
- `scripts/export_p5_public_surface_sync.py`
- `scripts/export_release_preflight_checklist_audit.py`
- `tests/test_export_p5_public_surface_sync.py`
- `tests/test_export_release_preflight_checklist_audit.py`
- `results/P5_public_surface_sync/`
- `results/release_preflight_checklist_audit/`
- `results/release_worktree_hygiene_snapshot/`

Optional internal-only additions if they are already part of the same review:

- `docs/milestones/F2_future_frontier_recheck_activation_matrix/`
- `docs/milestones/F3_post_h23_scope_lift_decision_bundle/`
- `docs/milestones/F4_post_h23_origin_claim_delta_matrix/`
- `docs/plans/2026-03-22-post-unattended-r32-mainline-design.md`
- `docs/milestones/H26_refreeze_after_r32_boundary_sharp_zoom/`
- `docs/milestones/H27_refreeze_after_r32_r33_same_endpoint_decision/`

Exclude from this packet:

- new runtime outputs from `R32` or later lanes;
- unrelated manuscript/blog drift outside the closeout wording set;
- broad historical untracked folders not needed for the closeout review.

## Decision Rule

- If packet 2 is coherent without packet 1, keep packet 2 narrow.
- If packet 2 depends on uncommitted `H24/R30/R31/H25` semantics, land packet 1
  first.
- If both packets remain too large, reduce scope again rather than mixing new
  runtime work into the closeout.
