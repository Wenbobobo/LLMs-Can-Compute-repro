# Commit And Hygiene Handoff

This document is preserved as the `H25`-era commit handoff for the old
same-endpoint route. Under `H30` it is not the current routing note; use it
only when isolating or committing the older `H24/R30/R31/H25/R32/R33/H27`
packet family.

## Stable Scientific / Routing State

- At the time of this handoff, `H30_post_r36_r37_scope_decision_packet` was
  the live routing packet. The repo now routes through
  `H32_post_r38_compiled_boundary_refreeze`.
- `H27_refreeze_after_r32_r33_same_endpoint_decision` is the preserved
  negative closeout of the old same-endpoint route.
- On that preserved prior route,
  `H25_refreeze_after_r30_r31_decision_packet` was the last active operational
  decision packet and `H23_refreeze_after_r26_r27_r28` remained the frozen
  same-endpoint scientific state.
- `R32_d0_family_local_boundary_sharp_zoom` and
  `R33_d0_non_retrieval_overhead_localization_audit` are preserved historical
  follow-up lanes on that old route, not the current next objective.
- `R29_d0_same_endpoint_systems_recovery_execution_gate` and
  `F3_post_h23_scope_lift_decision_bundle` remain blocked.
- `F2_future_frontier_recheck_activation_matrix` remains planning-only.
- `F4_post_h23_origin_claim_delta_matrix` appears adequate and does not need a
  claim-status rewrite for this closeout.

## Stable Outputs From This Closeout

- `results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json`
  now reports `blocked_count = 0` and keeps
  `systems_reauthorization_verdict = audit_non_retrieval_overhead_first`.
- `results/P5_public_surface_sync/summary.json` now reports
  `current_paper_phase = h25_refreeze_after_r30_r31_decision_packet_active_h23_frozen`
  and `blocked_count = 0`.
- `results/release_preflight_checklist_audit/summary.json` now reports
  `preflight_state = docs_and_audits_green` and `blocked_count = 0`, but its
  commit-readiness conclusion still depends on the current worktree.

## Reviewable Commit Subset

- Closeout wording and audit logic:
  `README.md`,
  `docs/publication_record/release_summary_draft.md`,
  `scripts/export_p5_public_surface_sync.py`,
  `tests/test_export_p5_public_surface_sync.py`,
  `scripts/export_release_preflight_checklist_audit.py`,
  `tests/test_export_release_preflight_checklist_audit.py`.
- Handoff/closeout docs:
  `tmp/active_wave_plan.md`,
  `docs/milestones/P15_internal_claim_and_handoff_sync_after_h25/status.md`,
  `docs/milestones/P15_internal_claim_and_handoff_sync_after_h25/artifact_index.md`,
  `docs/milestones/P15_internal_claim_and_handoff_sync_after_h25/handoff_notes.md`,
  `docs/milestones/P15_internal_claim_and_handoff_sync_after_h25/commit_hygiene_handoff.md`.
- Stable machine outputs for this closeout:
  `results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json`,
  `results/P5_public_surface_sync/README.md`,
  `results/P5_public_surface_sync/checklist.json`,
  `results/P5_public_surface_sync/summary.json`,
  `results/P5_public_surface_sync/surface_snapshot.json`.

## Self-Contained Dependency Set

The narrow closeout subset above is only self-contained if the earlier
`H25 active / H23 frozen` doc semantics are already committed in a prior
packet. If they are not, the closeout commit must also include:

- `STATUS.md`
- `docs/publication_record/README.md`
- `docs/publication_record/current_stage_driver.md`
- `docs/publication_record/release_preflight_checklist.md`

Without those files, the updated `P5` and preflight exporters/tests can become
temporarily inconsistent with the checked-in docs.

## State-Dependent Outputs

- `results/release_worktree_hygiene_snapshot/status_snapshot.json`
- `results/release_worktree_hygiene_snapshot/summary.json`
- `results/release_preflight_checklist_audit/README.md`
- `results/release_preflight_checklist_audit/checklist.json`
- `results/release_preflight_checklist_audit/snapshot.json`
- `results/release_preflight_checklist_audit/summary.json`

These should be regenerated inside the actual commit worktree, because the
current integrated tree still reports
`release_commit_state = dirty_worktree_release_commit_blocked`.

## Commit Guidance

- Do not create an outward sync commit from the current integrated tree.
- Save the current `H30` plan/handoff first, then create an isolated worktree
  for the commit subset.
- Prefer a two-step split when the broader post-`H23` packet is still
  uncommitted:
  1. `post-h23-core-packet`:
     the prerequisite `H24/R30/R31/H25` docs, scripts, tests, and stable
     outputs that establish `H25 active / H23 frozen` semantics.
  2. `h25-closeout-audits`:
     the narrower `P5` / preflight closeout wording, tests, handoff docs, and
     refreshed stable outputs listed above.
- Re-run:
  `uv run python scripts/export_release_worktree_hygiene_snapshot.py`
  and
  `uv run python scripts/export_release_preflight_checklist_audit.py`
  inside that clean worktree immediately before commit.
- Keep the commit path-scoped to this wave; do not sweep unrelated dirty-tree
  changes into the same review.
- Do not forget the untracked
  `results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json`
  if the closeout subset is committed.

## Misc Hygiene Notes

- `results/R20_d0_runtime_mechanism_ablation_matrix/probe_read_rows.json` is
  already ignored in `.gitignore`; no extra ignore rule is needed.
- If a later clean-worktree commit is prepared, the newly synchronized
  `F2/F3` planning docs and any matching `P15` handoff note updates may be
  included with the internal-only closeout subset, but they should not be mixed
  into a runtime or outward-release commit by accident.
