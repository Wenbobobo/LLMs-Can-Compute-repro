# Commit Split Manifest

## Summary

`P17` should prefer the narrowest self-contained split that preserves
`H30 active / H27 preserved-closeout / H25-H23 historical-context` semantics.
Use one commit only if the full subset is already clean and reviewable in the
isolated worktree. Otherwise split into the two packets below.

## Packet 1: `origin-core-h28-to-h30-packet`

Use this packet for the actual scientific/runtime/code bundle that reanchors
the repo on the narrow Origin-core line and lands the `R37 -> H30` result.

Recommended paths:

- `src/exec_trace/__init__.py`
- `src/exec_trace/datasets.py`
- `src/model/__init__.py`
- `src/model/exact_hardmax.py`
- `src/model/free_running_executor.py`
- `tests/test_model_exact_hardmax.py`
- `tests/test_model_free_running_executor.py`
- `tests/test_trace_interpreter.py`
- `scripts/export_h28_post_h27_origin_core_reanchor_packet.py`
- `scripts/export_r34_origin_retrieval_primitive_contract_gate.py`
- `scripts/export_r35_origin_append_only_stack_vm_execution_gate.py`
- `scripts/export_h29_refreeze_after_r34_r35_origin_core_gate.py`
- `scripts/export_r36_origin_long_horizon_precision_scaling_gate.py`
- `scripts/export_r37_origin_compiler_boundary_gate.py`
- `scripts/export_h30_post_r36_r37_scope_decision_packet.py`
- `tests/test_export_h28_post_h27_origin_core_reanchor_packet.py`
- `tests/test_export_r34_origin_retrieval_primitive_contract_gate.py`
- `tests/test_export_r35_origin_append_only_stack_vm_execution_gate.py`
- `tests/test_export_h29_refreeze_after_r34_r35_origin_core_gate.py`
- `tests/test_export_r36_origin_long_horizon_precision_scaling_gate.py`
- `tests/test_export_r37_origin_compiler_boundary_gate.py`
- `tests/test_export_h30_post_r36_r37_scope_decision_packet.py`
- `results/H28_post_h27_origin_core_reanchor_packet/`
- `results/R34_origin_retrieval_primitive_contract_gate/`
- `results/R35_origin_append_only_stack_vm_execution_gate/`
- `results/H29_refreeze_after_r34_r35_origin_core_gate/`
- `results/R36_origin_long_horizon_precision_scaling_gate/`
- `results/R37_origin_compiler_boundary_gate/`
- `results/H30_post_r36_r37_scope_decision_packet/`
- `docs/milestones/H28_post_h27_origin_core_reanchor_packet/`
- `docs/milestones/R34_origin_retrieval_primitive_contract_gate/`
- `docs/milestones/R35_origin_append_only_stack_vm_execution_gate/`
- `docs/milestones/H29_refreeze_after_r34_r35_origin_core_gate/`
- `docs/milestones/R36_origin_long_horizon_precision_scaling_gate/`
- `docs/milestones/R37_origin_compiler_boundary_gate/`
- `docs/milestones/H30_post_r36_r37_scope_decision_packet/`
- `docs/plans/2026-03-22-post-h27-origin-core-pivot-plan.md`
- `docs/plans/2026-03-22-post-r36-explicit-next-wave-design.md`
- `docs/claims_matrix.md`
- `docs/publication_record/claim_ladder.md`
- `docs/milestones/F4_post_h23_origin_claim_delta_matrix/claim_delta_matrix.md`

Exclude from this packet when possible:

- `README.md`
- `STATUS.md`
- `docs/plans/2026-03-22-post-h30-explicit-next-wave-design.md`
- `docs/milestones/P15_internal_claim_and_handoff_sync_after_h25/`
- `docs/milestones/P17_h30_commit_hygiene_and_clean_worktree_promotion/`
- publication-facing entrypoint docs that only explain the landed state

## Packet 2: `h30-entrypoint-closeout`

Use this packet for current-facing docs, handoff notes, and clean-worktree
packaging guidance after packet 1 is already present or when the branch already
contains the scientific packet.

Recommended paths:

- `README.md`
- `STATUS.md`
- `tmp/active_wave_plan.md`
- `docs/plans/README.md`
- `docs/plans/2026-03-22-post-h30-explicit-next-wave-design.md`
- `docs/milestones/README.md`
- `docs/milestones/P15_internal_claim_and_handoff_sync_after_h25/`
- `docs/milestones/P17_h30_commit_hygiene_and_clean_worktree_promotion/`
- `docs/publication_record/README.md`
- `docs/publication_record/current_stage_driver.md`
- `docs/publication_record/experiment_manifest.md`
- `docs/publication_record/archival_repro_manifest.md`
- `docs/publication_record/negative_results.md`
- `docs/publication_record/release_candidate_checklist.md`
- `docs/publication_record/release_preflight_checklist.md`
- `docs/publication_record/release_summary_draft.md`
- `docs/publication_record/review_boundary_summary.md`
- `docs/publication_record/submission_packet_index.md`

Optional additions if they are already in the same review for self-containment:

- `docs/publication_record/claim_ladder.md`
- `docs/claims_matrix.md`
- `docs/milestones/F4_post_h23_origin_claim_delta_matrix/claim_delta_matrix.md`

Exclude from this packet:

- unrelated manuscript/blog churn outside the current `H30` surface;
- new runtime outputs beyond the landed `H30` packet;
- old same-endpoint execution subsets not needed for the closeout review.

## Decision Rule

- If the clean branch does not already contain the scientific
  `H28/R34/R35/H29/R36/R37/H30` bundle, land packet 1 first.
- If packet 2 is coherent only after packet 1, keep the split explicit rather
  than mixing them.
- If both packets together are still too large, reduce scope again rather than
  mixing a later explicit packet into the same closeout batch.
