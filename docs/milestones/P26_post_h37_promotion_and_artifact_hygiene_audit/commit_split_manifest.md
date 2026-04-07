# Commit Split Manifest

## Summary

`P26` should keep current work reviewable against dirty `main` by separating
scientific/runtime history from the new docs/control wave and from purely
operational hygiene.

## Packet 1: `origin-core-runtime-history`

Use this packet for the already-landed scientific/runtime chain that `main`
still lacks.

Recommended paths:

- `src/`
- `scripts/export_h28_post_h27_origin_core_reanchor_packet.py`
- `scripts/export_r34_origin_retrieval_primitive_contract_gate.py`
- `scripts/export_r35_origin_append_only_stack_vm_execution_gate.py`
- `scripts/export_r36_origin_long_horizon_precision_scaling_gate.py`
- `scripts/export_r37_origin_compiler_boundary_gate.py`
- `scripts/export_r38_origin_compiler_control_surface_extension_gate.py`
- `scripts/export_r39_origin_compiler_control_surface_dependency_audit.py`
- `scripts/export_r40_origin_bounded_scalar_locals_and_flags_gate.py`
- `tests/test_export_h28_post_h27_origin_core_reanchor_packet.py`
- `tests/test_export_r34_origin_retrieval_primitive_contract_gate.py`
- `tests/test_export_r35_origin_append_only_stack_vm_execution_gate.py`
- `tests/test_export_r36_origin_long_horizon_precision_scaling_gate.py`
- `tests/test_export_r37_origin_compiler_boundary_gate.py`
- `tests/test_export_r38_origin_compiler_control_surface_extension_gate.py`
- `tests/test_export_r39_origin_compiler_control_surface_dependency_audit.py`
- `tests/test_export_r40_origin_bounded_scalar_locals_and_flags_gate.py`
- `results/H28_post_h27_origin_core_reanchor_packet/`
- `results/R34_origin_retrieval_primitive_contract_gate/`
- `results/R35_origin_append_only_stack_vm_execution_gate/`
- `results/H29_refreeze_after_r34_r35_origin_core_gate/`
- `results/R36_origin_long_horizon_precision_scaling_gate/`
- `results/R37_origin_compiler_boundary_gate/`
- `results/R38_origin_compiler_control_surface_extension_gate/`
- `results/R39_origin_compiler_control_surface_dependency_audit/`
- `results/R40_origin_bounded_scalar_locals_and_flags_gate/`

## Packet 2: `candidate-isolation-control-wave`

Use this packet for the current docs/control wave that lands `F16/H38/P26/F17`
above the preserved `H36/H37/P25/F15` stack.

Recommended paths:

- `README.md`
- `STATUS.md`
- `tmp/active_wave_plan.md`
- `docs/plans/2026-03-23-post-h37-f16-h38-p26-candidate-isolation-design.md`
- `docs/plans/README.md`
- `docs/milestones/F16_post_h37_r41_candidate_isolation_bundle/`
- `docs/milestones/H38_post_f16_runtime_relevance_reopen_decision_packet/`
- `docs/milestones/P26_post_h37_promotion_and_artifact_hygiene_audit/`
- `docs/milestones/F17_post_h38_same_substrate_exit_criteria_bundle/`
- `docs/milestones/README.md`
- `docs/publication_record/`
- `docs/claims_matrix.md`
- `scripts/export_h38_post_f16_runtime_relevance_reopen_decision_packet.py`
- `scripts/export_p26_post_h37_promotion_and_artifact_hygiene_audit.py`
- `tests/test_export_h38_post_f16_runtime_relevance_reopen_decision_packet.py`
- `tests/test_export_p26_post_h37_promotion_and_artifact_hygiene_audit.py`
- `results/H38_post_f16_runtime_relevance_reopen_decision_packet/`
- `results/P26_post_h37_promotion_and_artifact_hygiene_audit/`

## Packet 3: `defer-main-until-clean`

Use this packet only when `main` itself has been cleaned or reconciled.

Required rule:

- do not force-merge the current clean branch into dirty `main`;
- do not let operational artifact cleanup rewrite historical science packets.
