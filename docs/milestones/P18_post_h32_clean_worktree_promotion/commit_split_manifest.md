# Commit Split Manifest

## Summary

`P18` should prefer the narrowest self-contained split that preserves
`H32 active / H30-H31 preserved-upstream packet / blocked-lane discipline`
semantics.

Use one commit only if the full subset is already clean and reviewable in this
successor worktree. Otherwise split into the two packets below.

## Packet 1: `h31-r38-h32-scientific-packet`

Use this packet for the actual decision/runtime bundle that lands the later
explicit packet, the one-row extension gate, and the post-`R38` refreeze.

Recommended paths:

- `scripts/export_h31_post_h30_later_explicit_boundary_decision_packet.py`
- `scripts/export_r38_origin_compiler_control_surface_extension_gate.py`
- `scripts/export_h32_post_r38_compiled_boundary_refreeze.py`
- `tests/test_export_h31_post_h30_later_explicit_boundary_decision_packet.py`
- `tests/test_export_r38_origin_compiler_control_surface_extension_gate.py`
- `tests/test_export_h32_post_r38_compiled_boundary_refreeze.py`
- `docs/milestones/H31_post_h30_later_explicit_boundary_decision_packet/`
- `docs/milestones/R38_origin_compiler_control_surface_extension_gate/`
- `docs/milestones/H32_post_r38_compiled_boundary_refreeze/`
- `results/H31_post_h30_later_explicit_boundary_decision_packet/`
- `results/R38_origin_compiler_control_surface_extension_gate/`
- `results/H32_post_r38_compiled_boundary_refreeze/`
- `docs/claims_matrix.md`
- `docs/publication_record/claim_ladder.md`
- `docs/milestones/F4_post_h23_origin_claim_delta_matrix/claim_delta_matrix.md`

Exclude from this packet when possible:

- `README.md`
- `STATUS.md`
- `docs/publication_record/current_stage_driver.md`
- `tmp/active_wave_plan.md`
- `docs/publication_record/README.md`
- `docs/milestones/P18_post_h32_clean_worktree_promotion/`
- broader publication or release wording sweeps.

## Packet 2: `h32-entrypoint-closeout`

Use this packet for current-facing docs, active driver updates, saved plan
indexing, and the clean-worktree runbook once packet 1 is already present.

Recommended paths:

- `README.md`
- `STATUS.md`
- `tmp/active_wave_plan.md`
- `docs/plans/README.md`
- `docs/plans/2026-03-22-post-h30-h31-r38-extension-plan.md`
- `docs/milestones/README.md`
- `docs/milestones/P18_post_h32_clean_worktree_promotion/`
- `docs/publication_record/README.md`
- `docs/publication_record/current_stage_driver.md`
- `docs/publication_record/experiment_manifest.md`
- `docs/publication_record/review_boundary_summary.md`
- `docs/publication_record/release_summary_draft.md`
- `docs/publication_record/archival_repro_manifest.md`
- `docs/publication_record/submission_packet_index.md`
- `docs/publication_record/release_preflight_checklist.md`
- `docs/publication_record/release_candidate_checklist.md`

Optional additions if they are already coherent in the same review:

- `docs/milestones/H30_post_r36_r37_scope_decision_packet/`
- `docs/milestones/P17_h30_commit_hygiene_and_clean_worktree_promotion/`

Exclude from this packet:

- unrelated manuscript/blog churn;
- any broader compiler or demo plan;
- any attempt to restage dirty integrated-tree changes.

## Decision Rule

- land packet 1 first if the scientific/runtime result is not already isolated;
- keep packet 2 docs-only when possible;
- reduce scope again rather than mixing a later plan or broader runtime lane
  into the same promotion batch.
