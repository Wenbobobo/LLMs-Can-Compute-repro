# Current Stage Driver

## Active driver

The current active stage is:

- `H15_refreeze_and_decision_sync`

This stage starts from the locked submission-candidate bundle and restrained
release-candidate checkpoint created by `P8` and `P9`, from the completed
bounded return packet `H4/E1a/E1b/H5`, from the completed bounded mainline
packet `H6/R3/R4/(inactive R5)/H7`, from the completed same-endpoint
long-horizon packet `H8/R6/R7/H9`, from the completed bounded same-endpoint
follow-up packet `H10/H11/R8/R9/R10/H12`, from the preserved
governance/runtime handoff `H13_post_h12_rollover_and_next_stage_staging`
plus its standing `V1_full_suite_validation_runtime_audit` companion, and
from the now completed core-first reopen packet
`H14_core_first_reopen_and_scope_lock` with landed `R11` and `R12`.

The current stage does not open a new science lane. It records that the repo
is now refrozen on the same endpoint after one explicit reopen wave.

Current status inside this driver: `H14` is now the completed reopened packet
rather than the active stage. `R11` keeps the geometry parity slice exact
while blocking same-endpoint speedup wording. `R12` keeps current executor
exports exact while making the harder-slice inventory explicit. `H15`
synchronized root/publication/control docs and standing guards to that
completed packet, left `R13` inactive, left `R14` unjustified, and requires a
later explicit full plan before any new active science lane starts.

`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint follow-up
packet, `H8/R6/R7/H9` remains the completed direct same-endpoint baseline
underneath it, and `H6/R3/R4/(inactive R5)/H7` remains the deeper historical
baseline. `H13_post_h12_rollover_and_next_stage_staging` remains preserved,
and `V1_full_suite_validation_runtime_audit` remains a standing operational
reference rather than an active science lane.

## Execution order

The completed reopened wave ran in the order:
`H14_core_first_reopen_and_scope_lock` ->
`R11_geometry_fastpath_reaudit` ->
`R12_append_only_executor_long_horizon` ->
optional `R13_small_model_executor_reactivation` ->
bounded `R14_bounded_compiled_probe` ->
`H15_refreeze_and_decision_sync`.

1. Preserve the full current-round plan in `tmp/`.
2. Preserve `H10/H11/R8/R9/R10/H12` as the latest completed same-endpoint
   follow-up packet rather than the active packet.
3. Preserve `H13_post_h12_rollover_and_next_stage_staging` and
   `V1_full_suite_validation_runtime_audit` as the completed
   governance/runtime handoff rather than the active science lane.
4. Preserve `H8/R6/R7/H9` as the completed direct same-endpoint baseline and
   `H6/R3/R4/(inactive R5)/H7` as the deeper exactness/mechanism baseline.
5. Preserve `H14_core_first_reopen_and_scope_lock` as the completed reopened
   packet on the same narrow mechanism target.
6. Keep `R13_small_model_executor_reactivation` inactive unless a later
   bounded executor gap appears.
7. Keep `R14_bounded_compiled_probe` unjustified unless a later bounded
   contradiction or explicit compiled need appears.
8. Require a new explicit full plan before any further active lane starts.

## Standing gates

- `results/H15_refreeze_and_decision_sync/summary.json`
- `results/H14_core_first_reopen_guard/summary.json`
- `results/P1_paper_readiness/summary.json`
- `results/P5_public_surface_sync/summary.json`
- `results/P5_callout_alignment/summary.json`
- `results/H2_bundle_lock_audit/summary.json`
- `results/P10_submission_archive_ready/summary.json`
- `results/release_worktree_hygiene_snapshot/summary.json`
- `results/release_preflight_checklist_audit/summary.json`
- `results/H13_post_h12_governance_stage_health/summary.json`
- `results/R1_precision_mechanism_closure/summary.json`
- `results/R2_systems_baseline_gate/summary.json`
- `results/M7_frontend_candidate_decision/decision_summary.json`
- `results/V1_full_suite_validation_runtime_audit/summary.json`
- `results/V1_full_suite_validation_runtime_timing_followup/summary.json`
- `results/H10_r7_reconciliation_guard/summary.json`
- `results/H11_post_h9_mainline_rollover_guard/summary.json`
- `results/H8_driver_replacement_guard/summary.json`
- `results/H6_mainline_rollover_guard/summary.json`
- `pytest -q`
- `git diff --check`

## Active bounded lanes

- `H15_refreeze_and_decision_sync` is the current refrozen control stage.
- `H14_core_first_reopen_and_scope_lock` is preserved as the completed
  reopen packet on the same narrow mechanism target.
- `R11_geometry_fastpath_reaudit` has landed and keeps the exact `2D`
  fast-path story bounded to parity plus wording re-audit rather than
  same-endpoint speedup.
- `R12_append_only_executor_long_horizon` has landed and keeps the
  append-only/latest-write executor story bounded to the current exact exports
  plus explicit harder-slice inventory.
- `R13_small_model_executor_reactivation` stays inactive and bounded, and is
  not currently needed on the exported evidence state.
- `R14_bounded_compiled_probe` stays bounded and is not currently justified on
  the exported evidence state.
- `H13_post_h12_rollover_and_next_stage_staging` and
  `V1_full_suite_validation_runtime_audit` remain preserved handoff artifacts
  and standing operational references.
- `release_preflight_checklist_audit` keeps outward sync machine-audited while
  the repo still allows a dirty working tree between release-facing commits.
- `release_worktree_hygiene_snapshot` keeps the remaining clean-tree release
  check machine-readable by classifying whether the current worktree blocks an
  outward sync commit.
- `H13_post_h12_governance_stage_health` keeps one machine-readable preserved
  handoff summary over the current `H13/V1` control stack, preserved
  baselines, outward-sync audit, and archive-handoff state.
- the full-suite `pytest -q` runtime issue remains operationally classified as
  healthy but slow: collection completes, targeted standing suites remain
  green, and the bounded top-`6` per-file timing follow-up completed with no
  timeouts, so full runs should be reserved for long unattended windows.
- `M7` no-widening remains in force throughout the packet.

## Conditional reopen path

`E1c` remains conditional only. `E1c_compiled_boundary_patch` may activate
only if the completed same-endpoint packets or a later explicit review exposes
a concrete contradiction in the frozen tiny typed-bytecode `D0` boundary.

## Historical-complete references

These remain the completed baseline while the current stage keeps the repo
refrozen on the same narrow endpoint.

- `docs/milestones/H15_refreeze_and_decision_sync/result_digest.md`
- `docs/milestones/H14_core_first_reopen_and_scope_lock/result_digest.md`
- `docs/milestones/H13_post_h12_rollover_and_next_stage_staging/result_digest.md`
- `docs/milestones/H12_refreeze_and_record_sync/result_digest.md`
- `docs/milestones/H10_r7_reconciliation_and_refreeze/result_digest.md`
- `docs/milestones/H11_post_h9_mainline_rollover/result_digest.md`
- `docs/milestones/H8_driver_replacement_and_baseline_sync/result_digest.md`
- `docs/milestones/R6_d0_long_horizon_scaling_gate/result_digest.md`
- `docs/milestones/R7_d0_same_endpoint_runtime_bridge/result_digest.md`
- `docs/milestones/H9_refreeze_and_record_sync/result_digest.md`
- `docs/milestones/H6_mainline_rollover_and_backlog_sync/result_digest.md`
- `docs/milestones/R3_d0_exact_execution_stress_gate/result_digest.md`
- `docs/milestones/R4_mechanistic_retrieval_closure/result_digest.md`
- `docs/milestones/R5_same_scope_systems_stopgo_followup/result_digest.md`
- `docs/milestones/H7_refreeze_and_record_sync/result_digest.md`
- `docs/milestones/H4_reproduction_mainline_return/result_digest.md`
- `docs/milestones/E1a_precision_patch/result_digest.md`
- `docs/milestones/E1b_systems_patch/result_digest.md`
- `docs/milestones/H5_repro_sync_and_refreeze/result_digest.md`
- `docs/milestones/H3_stage_driver_consolidation_and_plan_index/result_digest.md`
- `docs/milestones/P10_submission_packet_and_archival_repro_bundle/result_digest.md`
- `docs/milestones/P11_manuscript_targeting_and_derivative_controls/result_digest.md`
- `docs/milestones/F1_future_evidence_playbooks/result_digest.md`
- `docs/publication_record/paper_package_plan.md`
- `docs/milestones/P8_submission_candidate_and_bundle_lock/result_digest.md`
- `docs/milestones/P9_release_candidate_and_public_surface_freeze/result_digest.md`
- `docs/milestones/H2_release_hygiene_and_audit_promotion/result_digest.md`
