# 2026-03-22 Post-Unattended R32 Mainline Design

## Summary

The narrow scientific target remains unchanged:

1. keep the fixed tiny typed-bytecode `D0` endpoint;
2. preserve `H23_refreeze_after_r26_r27_r28` as the frozen scientific state;
3. preserve `H25_refreeze_after_r30_r31_decision_packet` as the active
   operational routing packet;
4. execute `R32_d0_family_local_boundary_sharp_zoom` as the next true science
   lane only after the current dirty-tree closeout is isolated in a clean
   worktree;
5. keep `R33_d0_non_retrieval_overhead_localization_audit` deferred,
   `R29_d0_same_endpoint_systems_recovery_execution_gate` blocked, and
   `F3_post_h23_scope_lift_decision_bundle` blocked.

The next batch should therefore run in two layers rather than one blended
wave:

- an immediate operational closeout lane:
  `P16_h25_commit_hygiene_and_clean_worktree_promotion`;
- the next bounded science lane:
  `R32_d0_family_local_boundary_sharp_zoom`;
- then a new same-endpoint refreeze:
  `H26_refreeze_after_r32_boundary_sharp_zoom`;
- only then, conditional downstream systems follow-up:
  deferred `R33_d0_non_retrieval_overhead_localization_audit`;
- then a second same-endpoint decision packet if `R33` runs:
  `H27_refreeze_after_r32_r33_same_endpoint_decision`.

## Execution Protocol

- Save this design before execution and refresh `tmp/active_wave_plan.md`.
- Do not start new runtime execution from the current integrated dirty tree.
- Keep write sets isolated:
  - `main`: integration, driver sync, final verification, commit, push;
  - `wt-h25-clean`: `P16` only;
  - `wt-r32`: `R32` and `H26` only;
  - `wt-r33`: `R33` and `H27` only, and only if `H26` keeps `R33`
    justified next.
- Keep doc/paper/blog maintenance downstream of landed evidence. Until
  `R32` closes, those tasks remain low-priority piggyback work only.
- Prefer two existing subagents with disjoint ownership if delegation is used:
  one for evidence/doc freeze work and one for execution-lane verification. Do
  not increase parallel tool churn beyond that.

## Wave Order

### Wave 0: `P16_h25_commit_hygiene_and_clean_worktree_promotion`

- Save this design and the refreshed active-wave handoff.
- Split the current dirty-tree closeout into reviewable subsets.
- Treat current hygiene blockers as operational only, not scientific.
- If the broader post-`H23` packet is not yet committed, use a two-step split:
  1. `post-h23-core-packet`:
     `H24/R30/R31/H25` docs, scripts, tests, and stable outputs.
  2. `h25-closeout-audits`:
     `P5`, release preflight wording/tests, `P15`, and regenerated
     state-dependent closeout outputs.
- Re-run
  `uv run python scripts/export_release_worktree_hygiene_snapshot.py`
  and
  `uv run python scripts/export_release_preflight_checklist_audit.py`
  inside the clean worktree immediately before commit.

Acceptance:

- the closeout becomes reviewable as one or two path-scoped clean-worktree
  commits;
- `H25 active / H23 frozen` semantics stay self-consistent;
- no new runtime, widened endpoint, or claim drift appears in this wave.

### Wave 1: `R32_d0_family_local_boundary_sharp_zoom`

- Activate `R32` only from a clean next-stage worktree.
- Reuse the landed `R30` candidate core exactly:
  - `checkpoint_replay_long/u32/h3.0/plus_two/flattened`
  - `helper_checkpoint_braid_long/u20/h3.0/plus_two/flattened`
  - `subroutine_braid_long/u20/h3.0/plus_two/flattened`
  - `helper_checkpoint_braid/u8/h2.0/plus_one/flattened`
  - `subroutine_braid/u6/h2.0/plus_one/flattened`
- Keep the four approved axes only:
  `unique_address_target`,
  `horizon_multiplier`,
  `checkpoint_depth`,
  `hot_address_skew`.
- Use the saved first-pass ladder in
  `docs/milestones/R32_d0_family_local_boundary_sharp_zoom/execution_manifest.md`.
- Stop each branch after `2` reproduced exactness failures.
- Require one `first_fail` plus at least one neighboring exact row before any
  localization claim.

Acceptance:

- `R32` ends with one explicit verdict:
  `first_boundary_failure_localized`,
  `near_boundary_mixed_signal_needs_confirmation`,
  `grid_extended_still_not_localized`, or
  `resource_limited_before_localization`;
- the lane exports the full required result set and does not reopen a broader
  grid by momentum.

### Wave 2: `H26_refreeze_after_r32_boundary_sharp_zoom`

- Freeze the `R32` outcome into one machine-readable same-endpoint decision
  packet.
- Reclassify `supported_here`, `unsupported_here`, and `disconfirmed_here`
  without widening endpoint scope.
- Decide whether downstream same-endpoint work stops, or whether deferred
  `R33` remains justified.

Acceptance:

- `H26` records one explicit post-`R32` routing decision;
- `R33` is either preserved as the next justified deferred audit lane or
  explicitly deactivated on current evidence;
- `R29` and `F3` remain blocked unless a later explicit packet says otherwise.

### Wave 3: deferred `R33_d0_non_retrieval_overhead_localization_audit`

- Enter this wave only if `H26` keeps `R33` justified next.
- Start from the saved stratified `10`-to-`12` row audit packet.
- Keep the comparator set fixed:
  `spec_reference`,
  `lowered_exec_trace`,
  `pointer_like_exact`.
- Decompose only the current non-retrieval bucket into:
  `dispatch_decode_seconds`,
  `state_update_bookkeeping_seconds`,
  `tensor_python_plumbing_seconds`,
  `residual_fixed_overhead_seconds`.
- Escalate to the full `25` `R23` rows only if first-pass component rankings
  remain unstable or inconclusive.

Acceptance:

- `R33` ends with one explicit verdict:
  `non_retrieval_overhead_localized`,
  `non_retrieval_overhead_still_aggregate_only`,
  `suite_stable_noncompetitive_after_localization`, or
  `instrumentation_blocked_without_scope_drift`;
- the lane never acts as direct `R29` authorization.

### Wave 4: `H27_refreeze_after_r32_r33_same_endpoint_decision`

- Freeze the post-`R33` same-endpoint state if `R33` ran.
- Record whether the systems story remains mixed, becomes more sharply
  negative, or becomes materially positive on the current endpoint.
- Reassess whether `R29`, `F3`, or any future `F2` review is still blocked.

Acceptance:

- `H27` records one explicit post-`R33` same-endpoint decision;
- `R29`, `F3`, and `F2` are not reopened by narrative momentum;
- any broader move still requires a later explicit reauthorization packet.

## Validation

- `Wave 0`:
  focused exporter tests for `R30/R31/H25/P5/preflight`, plus regenerated
  hygiene/preflight outputs from the clean worktree.
- `Wave 1`:
  focused `R32` execution/exporter checks, plus any touched executor/runtime
  tests.
- `Wave 2`:
  `H26` exporter/tests and result-summary coherence.
- `Wave 3`:
  exactness must not regress on the audited rows; component decomposition must
  map back to the current aggregate timing family.
- `Wave 4`:
  `H27` exporter/tests and current-stage-driver synchronization.

## Defaults

- Stay on the same narrow `D0` endpoint.
- Do not treat `P16` as a science lane.
- Do not treat `R33` as active until `H26` explicitly leaves it justified.
- Do not treat `R30`, `R31`, or `H25` as scope-lift reauthorization.
- Do not let README/blog/manuscript wording outrun landed evidence.
