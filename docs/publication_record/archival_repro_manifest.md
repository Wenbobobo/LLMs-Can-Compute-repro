# Archival Repro Manifest

Status: archival manifest for the current locked checkpoint. This file records
what should be archived, how to regenerate core artifacts, and what must stay
out of the public bundle.

## Environment baseline

- Python `3.12`
- `uv` for environment and command orchestration
- current reproducibility summaries are generated from the repo-local virtual
  environment recorded in result JSON files
- CUDA is optional for archive readers; result bundles already record whether
  GPU support was present when exports ran

## Archive payload

- repository source under `src/`, `scripts/`, and `tests/`
- publication ledgers under `docs/publication_record/`
- milestone logs under `docs/milestones/`
- machine-readable outputs under `results/`
- top-level control surface: `README.md`, `STATUS.md`, `pyproject.toml`,
  `uv.lock`

## Canonical regeneration commands

```bash
uv sync --group dev
uv run python scripts/export_p1_figure_table_sources.py
uv run python scripts/render_p1_paper_artifacts.py
uv run python scripts/export_p1_paper_readiness.py
uv run python scripts/export_h18_post_h17_mainline_reopen_guard.py
uv run python scripts/export_r19_d0_pointer_like_surface_generalization_gate.py
uv run python scripts/export_r20_d0_runtime_mechanism_ablation_matrix.py
uv run python scripts/export_r21_d0_exact_executor_boundary_break_map.py
uv run python scripts/export_h19_refreeze_and_next_scope_decision.py
uv run python scripts/export_h20_post_h19_mainline_reentry_and_hygiene_split.py
uv run python scripts/export_r22_d0_true_boundary_localization_gate.py
uv run python scripts/export_r23_d0_same_endpoint_systems_overturn_gate.py
uv run python scripts/export_h21_refreeze_after_r22_r23.py
uv run python scripts/export_h22_post_h21_boundary_reopen_and_dual_track_lock.py
uv run python scripts/export_r26_d0_boundary_localization_execution_gate.py
uv run python scripts/export_r28_d0_trace_retrieval_contract_audit.py
uv run python scripts/export_r27_d0_boundary_localization_extension_gate.py
uv run python scripts/export_h23_refreeze_after_r26_r27_r28.py
uv run python scripts/export_r30_d0_boundary_reauthorization_packet.py
uv run python scripts/export_r31_d0_same_endpoint_systems_recovery_reauthorization_packet.py
uv run python scripts/export_h25_refreeze_after_r30_r31_decision_packet.py
uv run python scripts/export_h28_post_h27_origin_core_reanchor_packet.py
uv run python scripts/export_r34_origin_retrieval_primitive_contract_gate.py
uv run python scripts/export_r35_origin_append_only_stack_vm_execution_gate.py
uv run python scripts/export_h29_refreeze_after_r34_r35_origin_core_gate.py
uv run python scripts/export_r36_origin_long_horizon_precision_scaling_gate.py
uv run python scripts/export_r37_origin_compiler_boundary_gate.py
uv run python scripts/export_h30_post_r36_r37_scope_decision_packet.py
uv run python scripts/export_h33_post_h32_conditional_next_question_packet.py
uv run python scripts/export_r39_origin_compiler_control_surface_dependency_audit.py
uv run python scripts/export_h34_post_r39_later_explicit_scope_decision_packet.py
uv run python scripts/export_h35_post_p23_bounded_scalar_family_runtime_decision_packet.py
uv run python scripts/export_r40_origin_bounded_scalar_locals_and_flags_gate.py
uv run python scripts/export_h36_post_r40_bounded_scalar_family_refreeze.py
uv run python scripts/export_p25_post_h36_clean_promotion_prep.py
uv run python scripts/export_h37_post_h36_runtime_relevance_decision_packet.py
uv run python scripts/export_h38_post_f16_runtime_relevance_reopen_decision_packet.py
uv run python scripts/export_p26_post_h37_promotion_and_artifact_hygiene_audit.py
uv run python scripts/export_h40_post_h38_semantic_boundary_activation_packet.py
uv run python scripts/export_r42_origin_append_only_memory_retrieval_contract_gate.py
uv run python scripts/export_f20_post_r42_dual_mode_model_mainline_bundle.py
uv run python scripts/export_h41_post_r42_aggressive_long_arc_decision_packet.py
uv run python scripts/export_p27_post_h41_clean_promotion_and_explicit_merge_packet.py
uv run python scripts/export_r43_origin_bounded_memory_small_vm_execution_gate.py
uv run python scripts/export_r45_origin_dual_mode_model_mainline_gate.py
uv run python scripts/export_h42_post_r43_route_selection_packet.py
uv run python scripts/export_r44_origin_restricted_wasm_useful_case_execution_gate.py
uv run python scripts/export_h43_post_r44_useful_case_refreeze.py
uv run python scripts/export_p28_post_h43_publication_surface_sync.py
uv run python scripts/export_h15_refreeze_and_decision_sync.py
uv run python scripts/export_h14_core_first_reopen_guard.py
uv run python scripts/export_h13_post_h12_governance_stage_health.py
uv run python scripts/export_v1_full_suite_validation_runtime_audit.py
uv run python scripts/export_v1_full_suite_validation_runtime_timing_followup.py
uv run python scripts/export_p5_public_surface_sync.py
uv run python scripts/export_p5_callout_alignment.py
uv run python scripts/export_h2_bundle_lock_audit.py
uv run python scripts/export_release_worktree_hygiene_snapshot.py
uv run python scripts/export_release_preflight_checklist_audit.py
uv run python scripts/export_p10_submission_archive_ready.py
uv run pytest -q
```

## Integrity checks

- `results/P1_paper_readiness/summary.json` shows `10/10` ready figure/table
  items and no blocked or partial rows
- `results/H30_post_r36_r37_scope_decision_packet/summary.json` records the
  preserved prior Origin-core routing/refreeze packet after the tiny compiled
  boundary gate
- `results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json`
  records the explicit later decision packet that fixed the admitted extension
  row and the boundary probe
- `results/R38_origin_compiler_control_surface_extension_gate/summary.json`
  records one richer same-substrate compiled control/call family
- `results/H32_post_r38_compiled_boundary_refreeze/summary.json` records the
  preserved earlier compiled-boundary routing/refreeze packet after the
  explicit extension and keeps any later compiler-boundary extension
  conditional on a new plan packet
- `results/H33_post_h32_conditional_next_question_packet/summary.json`
  records the preserved earlier docs-only packet that selected exactly one
  same-substrate question on the compiled-boundary line
- `results/R39_origin_compiler_control_surface_dependency_audit/summary.json`
  records one declared helper-body permutation with target renumbering
  surviving on the admitted row and the named same-family boundary probe
- `results/H34_post_r39_later_explicit_scope_decision_packet/summary.json`
  records the preserved earlier docs-only freeze-complete-for-now packet above
  the compiled-boundary line
- `results/H35_post_p23_bounded_scalar_family_runtime_decision_packet/summary.json`
  records the preserved prior bounded-scalar runtime authorization packet
- `results/R40_origin_bounded_scalar_locals_and_flags_gate/summary.json`
  records the completed bounded-scalar same-substrate runtime gate
- `results/H36_post_r40_bounded_scalar_family_refreeze/summary.json` records
  the preserved active routing/refreeze packet underneath the current
  semantic-boundary route
- `results/H37_post_h36_runtime_relevance_decision_packet/summary.json`
  records the preserved prior keep-freeze decision after `H36`
- `results/H38_post_f16_runtime_relevance_reopen_decision_packet/summary.json`
  records the preserved prior docs-only keep-freeze packet above `F16`
- `results/P25_post_h36_clean_promotion_prep/summary.json` records the
  preserved prior clean promotion-prep lane
- `results/P26_post_h37_promotion_and_artifact_hygiene_audit/summary.json`
  records the preserved prior operational audit lane
- `results/H40_post_h38_semantic_boundary_activation_packet/summary.json`
  records the preserved prior activation packet that authorized exact `R42`
- `results/R42_origin_append_only_memory_retrieval_contract_gate/summary.json`
  records the completed semantic-boundary retrieval-contract gate with exact
  value plus maximizer-row identity
- `results/F20_post_r42_dual_mode_model_mainline_bundle/summary.json`
  records the coequal-mainline model posture without replacing exact evidence
- `results/H41_post_r42_aggressive_long_arc_decision_packet/summary.json`
  records the preserved prior docs-only decision packet that authorized exact
  `R43` plus coequal `R45`
- `results/P27_post_h41_clean_promotion_and_explicit_merge_packet/summary.json`
  records the completed explicit merge packet and keeps `merge_executed = false`
- `results/R43_origin_bounded_memory_small_vm_execution_gate/summary.json`
  records the completed exact bounded-memory small-VM gate on `5/5` fixed
  families
- `results/R45_origin_dual_mode_model_mainline_gate/summary.json` records the
  completed coequal model lane on the landed `R43` contract family
- `results/H42_post_r43_route_selection_packet/summary.json` records the
  preserved prior docs-only packet that authorized exact `R44`
- `results/R44_origin_restricted_wasm_useful_case_execution_gate/summary.json`
  records the completed current restricted useful-case gate on the fixed
  three-kernel ladder
- `results/H43_post_r44_useful_case_refreeze/summary.json` records the current
  docs-only useful-case refreeze packet and restores
  `no_active_downstream_runtime_lane`
- `results/P28_post_h43_publication_surface_sync/summary.json` records the
  completed publication/control sync packet that keeps `H43` current while
  aligning downstream ledgers
- `results/R37_origin_compiler_boundary_gate/summary.json` records one narrow
  positive fact beyond `H29/R36`: one admitted tiny bytecode subset survives
  source reference, lowering parity, and free-running exact execution on the
  active substrate
- `results/R36_origin_long_horizon_precision_scaling_gate/summary.json`
  records the active narrow precision boundary rather than a broad precision
  robustness claim
- `results/H29_refreeze_after_r34_r35_origin_core_gate/summary.json` records
  the preserved upstream Origin-core refreeze chain
- `results/H28_post_h27_origin_core_reanchor_packet/summary.json` records the
  Origin-core pivot away from the older same-endpoint route
- `results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`
  records the preserved negative closeout of the older same-endpoint route
- `results/H23_refreeze_after_r26_r27_r28/summary.json` records the preserved
  historical same-endpoint refreeze state, keeps the boundary unresolved inside the
  bounded `R22/R26/R27` envelope, keeps the mechanism contract positive only
  with partial control isolation, preserves the mixed systems verdict, and
  points the next downstream docs lane at `P14`
- `results/H25_refreeze_after_r30_r31_decision_packet/summary.json` records
  the preserved historical same-endpoint operational decision packet: `H23`
  stays the frozen scientific state, `R32` becomes the primary next lane,
  `R33` stays deferred, and `R29/F3` remain blocked
- `results/R30_d0_boundary_reauthorization_packet/summary.json` records the
  post-`H23` boundary decision that routes the next justified boundary work
  through one family-local `R32` sharp zoom rather than another historical
  full-grid expansion
- `results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json`
  records the post-`H23` systems decision that keeps direct `R29` reopening
  blocked and routes any later same-endpoint systems story through the
  narrower `R33` audit first
- `results/H22_post_h21_boundary_reopen_and_dual_track_lock/summary.json`
  records the bounded post-`H21` reopen-control packet
- `results/R26_d0_boundary_localization_execution_gate/summary.json` and
  `results/R27_d0_boundary_localization_extension_gate/summary.json` both
  preserve no-break-observed boundary packets rather than true boundary
  localization
- `results/R28_d0_trace_retrieval_contract_audit/summary.json` records the
  current mechanism-contract support result without turning it into a systems
  win
- `results/H21_refreeze_after_r22_r23/summary.json` remains the preserved
  immediate pre-reopen same-endpoint control state
- `results/H19_refreeze_and_next_scope_decision/summary.json` remains the
  preserved pre-`R22/R23` refrozen same-endpoint control state
- `results/H15_refreeze_and_decision_sync/summary.json` records the current
  preserved prior refrozen stage, leaves `R13` inactive, leaves `R14`
  unjustified, and shows zero blocked items
- `results/H14_core_first_reopen_guard/summary.json` shows zero blocked items
  on the preserved core-first reopen control surface
- `results/H13_post_h12_governance_stage_health/summary.json` shows zero
  blocked items on the preserved governance/runtime handoff
- `results/V1_full_suite_validation_runtime_audit/summary.json` records a
  successful collect-only inventory on the current suite
- `results/V1_full_suite_validation_runtime_timing_followup/summary.json`
  reports `healthy_but_slow` with zero timed-out files
- `results/release_worktree_hygiene_snapshot/summary.json` reports either
  `dirty_worktree_release_commit_blocked` or
  `clean_worktree_ready_if_other_gates_green`, and does not report
  `content_issues_present`
- `results/release_preflight_checklist_audit/summary.json` reports
  `docs_and_audits_green`
- `results/P5_public_surface_sync/summary.json` shows zero blocked items
- `results/P5_callout_alignment/summary.json` shows zero blocked rows
- `results/H2_bundle_lock_audit/summary.json` shows zero blocked items
- `results/P10_submission_archive_ready/summary.json` shows zero blocked items

## Restricted-source exclusion

Local-only source material under `docs/Origin/` and `docs/origin/` stays out of
the archival/public packet. The current public-safe docs mention those paths
only as excluded inputs, never as required release artifacts.

## Archive interpretation rule

This archive is evidence for a narrow mechanistic endpoint: append-only traces,
exact latest-write retrieval, bounded precision, and one tiny compiled
boundary on the active Origin-core substrate. It is not evidence for arbitrary
`C`, general LLM computation, or current-scope end-to-end systems superiority.
The current active docs-only packet is `H43`, above the preserved active
`H36` routing/refreeze packet, the completed `R42/R43/R44/R45`
semantic-boundary gate stack, and the completed `P27/P28` operational
release-control pair. The earlier `H32 -> H33 -> R39 -> H34` compiled-boundary
line remains preserved historical support rather than the active routing top.
`H35/R40/H36` record the later bounded-scalar reopen and refreeze that now sit
directly underneath the semantic-boundary route. `H27/H28` explain the pivot
away from the older same-endpoint route. The preserved `H23` packet
strengthens same-endpoint boundary and mechanism evidence inside the fixed
`D0` boundary, but it still does not localize the true executor boundary,
still preserves only partial control isolation, and still does not overturn
the mixed same-endpoint systems gate. The later `R30/R31/H25` stack remains
historical route-selection context only; it does not widen the current science
claim set.
