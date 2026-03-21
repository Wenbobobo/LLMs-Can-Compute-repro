# Current Stage Driver

## Active driver

The current active stage is:

- `H21_refreeze_after_r22_r23`

This stage starts from the locked submission-candidate bundle and restrained
release-candidate checkpoint created by `P8` and `P9`, from the completed
bounded return packet `H4/E1a/E1b/H5`, from the completed bounded mainline
packet `H6/R3/R4/(inactive R5)/H7`, from the completed same-endpoint
long-horizon packet `H8/R6/R7/H9`, from the completed bounded same-endpoint
follow-up packet `H10/H11/R8/R9/R10/H12`, from the preserved
governance/runtime handoff `H13_post_h12_rollover_and_next_stage_staging`
plus its standing `V1_full_suite_validation_runtime_audit` companion, from
the completed prior reopen/refreeze packet
`H14_core_first_reopen_and_scope_lock` with landed `R11`, `R12`, and the
preserved `H15_refreeze_and_decision_sync` closeout, from the completed
same-scope reopen/refreeze packet `H16/R15/R16/R17/R18/H17`, from the
completed same-endpoint mainline reopen/refreeze packet
`H18/R19/R20/R21/H19`, and from the completed post-`H19`
reentry/refreeze follow-up `H20/R22/R23/H21`.

The current stage records the frozen same-endpoint state after the landed
`R22/R23` follow-up on top of the preserved `H18/R19/R20/R21/H19` packet. It
does not authorize a wider endpoint, a broader
"LLMs are computers" thesis, or frontier/demo wording by momentum. Any later
frontier review remains conditional-only and planning-only unless a later
explicit plan says otherwise.

The next downstream operational lane is
`P12_manuscript_and_manifest_maintenance` under
`docs/plans/2026-03-21-post-r22-r23-h21-mainline-design.md`. That lane updates
claim/evidence ledgers and manifests downstream of landed `H21` evidence
without reopening runtime scope. `P13` remains the later outward-sync / hygiene
lane. Any later broader review remains blocked behind the planning-only
`F2_future_frontier_recheck_activation_matrix`.

Current status inside this driver: `H15` remains the preserved prior refreeze
decision rather than the active stage. `R15` landed as the first concrete lane
under `H16`, extending retrieval-pressure coverage to the four `R6` families
that were not covered by `R8` while staying exact on the same endpoint. `R16`
landed as the bounded real-trace precision saturation follow-up on the
admitted `R8/R15` memory surface, keeping all `8/8` screened streams
`effective_here` while localizing the preserved helper-checkpoint boundary.
`R17` landed as the bounded full-surface runtime bridge: all `8/8` admitted
runtime rows stayed exact, median accelerated-versus-linear speedup remained
only about `1.0019x`, median accelerated-versus-lowered ratio remained about
`1257.5x`, and focused attribution named one bounded `R18` repair target on
`helper_checkpoint_braid_long/retrieval_total`. `R18a` first measured one
narrow decomp-first repair probe and failed its `2.0x` target gate, but `R18b`
then closed the comparator-only runtime repair packet: pointer-like exact
retrieval stayed exact on the focused target plus matched control, the target
reached about `1308.5x` versus the recorded `R17` accelerated baseline, and
the full admitted `8/8` confirmation sweep stayed exact with about `1252.7x`
median speedup versus the recorded `R17` accelerated baseline. `H17` now
remains preserved as the prior same-scope refreeze state, with
`frontier_recheck_decision = conditional_plan_required`. `H18` then reopened
bounded same-endpoint runtime work without widening scope. `R19` closed the
first `H18` runtime lane on the same endpoint: `linear_exact`, `accelerated`,
and `pointer_like_exact` stayed exact on admitted `8/8` plus heldout `16/16`
rows, with no heldout family failure. `R20` then closed the bounded mechanism
lane on the fixed `16`-row sample set: `pointer_like_exact` stayed exact on
`16/16`, while both negative controls failed on `16/16`. `R21` then landed as
the bounded executor-boundary lane: pointer-like exact stayed exact on all
`96/96` executed candidates in the fixed `48`-branch grid, and no bounded
branch failure was observed. `H19` refroze that packet as the preserved
pre-`R22/R23` same-endpoint state, with
`decision_state = same_endpoint_refreeze_complete` and
`historical_next_priority_lane = p13_public_surface_sync_and_repo_hygiene`.
`H20` then
separated dirty-tree hygiene from the next science wave. `R22` extended the
boundary scan to `102/102` executed candidates without localizing a failure.
`R23` reran the full positive `D0` systems universe, kept pointer-like exact
exact on `25/25` rows, but still failed to overturn the mixed systems gate.
`H21` now refreezes that follow-up as the current same-endpoint state, with
`decision_state = post_r22_r23_refreeze_complete`,
`boundary_verdict = extended_grid_no_break_still_not_localized`,
`systems_verdict = systems_still_mixed`,
`future_frontier_review_state = planning_only_conditionally_reviewable`, and
`next_priority_lane = p12_manuscript_and_manifest_maintenance`.

`H14/R11/R12/H15` remains the completed prior reopen/refreeze packet.
`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint follow-up
packet before the later reopen packets. `H8/R6/R7/H9` remains the completed
direct same-endpoint baseline underneath it, and `H6/R3/R4/(inactive R5)/H7`
remains the deeper historical baseline. `H13_post_h12_rollover_and_next_stage_staging`
remains preserved, and `V1_full_suite_validation_runtime_audit` remains a
standing operational reference rather than an active science lane.

## Execution order

The completed same-scope reopen/refreeze wave ran in the order:
`H16_post_h15_same_scope_reopen_and_scope_lock` ->
`R15_d0_remaining_family_retrieval_pressure_gate` ->
`R16_d0_real_trace_precision_boundary_saturation` ->
`R17_d0_full_surface_runtime_bridge` ->
comparator-only `R18_d0_same_endpoint_runtime_repair_counterfactual`
(`R18a` then `R18b`, without needing `R18c`) ->
`H17_refreeze_and_conditional_frontier_recheck`.

The completed same-endpoint mainline reopen/refreeze wave then ran in the
order:
`H18_post_h17_mainline_reopen_and_scope_lock` ->
`R19_d0_pointer_like_surface_generalization_gate` ->
`R20_d0_runtime_mechanism_ablation_matrix` ->
`R21_d0_exact_executor_boundary_break_map` ->
`H19_refreeze_and_next_scope_decision`.

The completed post-`H19` follow-up wave then ran in the order:
`H20_post_h19_mainline_reentry_and_hygiene_split` ->
`R22_d0_true_boundary_localization_gate` ->
`R23_d0_same_endpoint_systems_overturn_gate` ->
`H21_refreeze_after_r22_r23`.

1. Preserve `H21_refreeze_after_r22_r23` as the current frozen same-endpoint
   state.
2. Preserve `H20/R22/R23` as the completed post-`H19` follow-up packet
   underneath `H21`.
3. Preserve `H19_refreeze_and_next_scope_decision` as the immediate
   pre-refreeze same-endpoint control state.
4. Preserve `H18/R19/R20/R21` as the completed same-endpoint mainline reopen
   packet underneath `H19`.
5. Preserve `H17_refreeze_and_conditional_frontier_recheck` as the prior
   same-scope refreeze state.
6. Preserve `H16/R15/R16/R17/R18` as the completed same-scope reopen packet.
7. Preserve `H15_refreeze_and_decision_sync` as the prior completed refreeze
   decision.
8. Preserve `H14/R11/R12/H15` as the completed prior reopen/refreeze packet.
9. Preserve `H10/H11/R8/R9/R10/H12` as the latest completed same-endpoint
   follow-up packet before the later reopen waves.
10. Preserve `H13_post_h12_rollover_and_next_stage_staging` and
    `V1_full_suite_validation_runtime_audit` as the completed
    governance/runtime handoff rather than the active science lane.
11. Preserve `H8/R6/R7/H9` as the completed direct same-endpoint baseline and
    `H6/R3/R4/(inactive R5)/H7` as the deeper exactness/mechanism baseline.
12. Require a later explicit plan before any future frontier recheck or scope
    lift.

## Next planned order

The next downstream sequence after landed `H21` is:
`P12_manuscript_and_manifest_maintenance` ->
`P13_public_surface_sync_and_repo_hygiene` ->
planning-only `F2_future_frontier_recheck_activation_matrix` if later review
ever becomes worth re-evaluating.

Control references for that downstream wave:
- `results/H21_refreeze_after_r22_r23/summary.json`
- `results/H20_post_h19_mainline_reentry_and_hygiene_split/summary.json`
- `results/R22_d0_true_boundary_localization_gate/summary.json`
- `results/R23_d0_same_endpoint_systems_overturn_gate/summary.json`
- `results/H19_refreeze_and_next_scope_decision/summary.json`
- `results/H18_post_h17_mainline_reopen_guard/summary.json`
- `results/R19_d0_pointer_like_surface_generalization_gate/summary.json`
- `results/R19_d0_pointer_like_surface_generalization_gate/manifest_rows.json`
- `results/R19_d0_pointer_like_surface_generalization_gate/runtime_rows.json`
- `results/R20_d0_runtime_mechanism_ablation_matrix/summary.json`
- `results/R20_d0_runtime_mechanism_ablation_matrix/runtime_matrix_rows.json`
- `results/R21_d0_exact_executor_boundary_break_map/summary.json`
- `results/R21_d0_exact_executor_boundary_break_map/branch_summary.json`
- `docs/milestones/F2_future_frontier_recheck_activation_matrix/activation_matrix.md`
- `docs/milestones/P12_manuscript_and_manifest_maintenance/h19_packet_ledger_map.md`

## Standing gates

- `results/H21_refreeze_after_r22_r23/summary.json`
- `results/H20_post_h19_mainline_reentry_and_hygiene_split/summary.json`
- `results/R22_d0_true_boundary_localization_gate/summary.json`
- `results/R23_d0_same_endpoint_systems_overturn_gate/summary.json`
- `results/H19_refreeze_and_next_scope_decision/summary.json`
- `results/H17_refreeze_and_conditional_frontier_recheck/summary.json`
- `results/H16_post_h15_same_scope_reopen_guard/summary.json`
- `results/H15_refreeze_and_decision_sync/summary.json`
- `results/R15_d0_remaining_family_retrieval_pressure_gate/summary.json`
- `results/R16_d0_real_trace_precision_boundary_saturation/summary.json`
- `results/R17_d0_full_surface_runtime_bridge/summary.json`
- `results/R18_d0_same_endpoint_runtime_repair_counterfactual/summary.json`
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

- `H21_refreeze_after_r22_r23` is the current frozen same-endpoint control
  stage.
- `H20_post_h19_mainline_reentry_and_hygiene_split` is preserved as the
  reentry/hygiene split guard underneath `H21`.
- `R22_d0_true_boundary_localization_gate` has landed as the harder bounded
  boundary follow-up and still did not localize a failure.
- `R23_d0_same_endpoint_systems_overturn_gate` has landed as the harder
  same-endpoint systems follow-up and still leaves the systems story mixed.
- `P12_manuscript_and_manifest_maintenance` is the immediate next-priority
  manuscript / manifest lane for landed `H21` evidence.
- `H18_post_h17_mainline_reopen_and_scope_lock` is preserved as the completed
  same-endpoint planning guard rather than the frozen state.
- `R19_d0_pointer_like_surface_generalization_gate` has landed as the
  admitted-plus-heldout runtime generalization lane under `H18`.
- `R20_d0_runtime_mechanism_ablation_matrix` has landed as the bounded
  mechanism lane under the same endpoint.
- `R21_d0_exact_executor_boundary_break_map` has landed as the bounded
  executor-boundary lane: the fixed scan stayed exact on `96/96` executed
  candidates and did not yet observe a branch failure inside the bounded grid.
- `H17_refreeze_and_conditional_frontier_recheck` is preserved as the prior
  same-scope refreeze control stage for the completed `H16/R15/R16/R17/R18`
  packet.
- `H16_post_h15_same_scope_reopen_and_scope_lock` is preserved as the earlier
  same-scope reopen packet rather than the active stage.
- `H15_refreeze_and_decision_sync` is preserved as the prior refreeze and
  decision-sync record rather than the active stage.
- `P13_public_surface_sync_and_repo_hygiene` is the downstream public-surface
  sync and repo-hygiene lane after `P12` stabilizes the post-`H21` ledgers.
- `F2_future_frontier_recheck_activation_matrix` remains planning-only and
  does not authorize widened experiments.
- `H14_core_first_reopen_and_scope_lock` remains preserved as the completed
  prior reopen packet on the same narrow mechanism target.
- `H13_post_h12_rollover_and_next_stage_staging` and
  `V1_full_suite_validation_runtime_audit` remain preserved handoff artifacts
  and standing operational references.
- `release_preflight_checklist_audit` keeps outward sync machine-audited while
  the repo still allows a dirty working tree between release-facing commits.
- `release_worktree_hygiene_snapshot` keeps the remaining clean-tree release
  check machine-readable by classifying whether the current worktree blocks an
  outward sync commit.
- the full-suite `pytest -q` runtime issue remains operationally classified as
  healthy but slow: collection completes, targeted standing suites remain
  green, and the bounded top-`6` per-file timing follow-up completed with no
  timeouts, so full runs should be reserved for long unattended windows.
- `M7` no-widening remains in force throughout the packet.

## Conditional reopen path

`E1c` remains conditional only. `E1c_compiled_boundary_patch` may activate
only if the current same-endpoint packets expose a concrete contradiction in
the frozen tiny typed-bytecode `D0` boundary. Any later frontier recheck
remains conditional-only and must start from the frozen `H21` state while also
passing the planning-only `F2` trigger discipline before a new explicit plan.

## Historical-complete references

These remain the completed baseline while the current stage keeps the repo
active on the same narrow endpoint.

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
