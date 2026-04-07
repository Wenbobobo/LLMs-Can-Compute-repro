# 2026-03-22 Post-H25 R32-R33 Near-Term Design

## Summary

`H25_refreeze_after_r30_r31_decision_packet` is now the active operational
decision packet. It preserves `H23_refreeze_after_r26_r27_r28` as the current
frozen scientific state and authorizes only one primary next science lane:
`R32_d0_family_local_boundary_sharp_zoom`. It keeps
`R33_d0_non_retrieval_overhead_localization_audit` as a deferred systems-audit
prerequisite lane and leaves `R29` and `F3` blocked.

The next unattended planning step should therefore stay narrow:

1. make `R32` executable without reopening the historical full grid;
2. make `R33` concrete enough that it can run later without drifting into a
   vague systems-recovery narrative;
3. avoid executing either lane from the current dirty-tree closeout state.

## Approach Options

### Option A: Execute `R32` immediately and leave `R33` as a note

Pros:
- advances the primary science lane fastest.

Cons:
- current dirty-tree hygiene makes any immediate execution packet harder to
  isolate reviewably;
- `R33` stays underspecified, so a later deferred switch risks reopening
  design work during execution time.

### Option B: Plan `R32` and `R33` now, execute `R32` first later

Pros:
- matches `H25`: `R32` stays primary and `R33` stays deferred;
- gives unattended continuation a concrete manifest for both lanes;
- keeps current work inside planning and handoff, not mixed with new runtime.

Cons:
- does not produce new scientific evidence in this batch.

Recommendation:
- choose Option B.

### Option C: Switch to `R33` first

Pros:
- may reduce later systems ambiguity.

Cons:
- conflicts with `H25` priority order;
- risks treating a deferred audit as the new mainline by momentum.

Reject this option unless a later explicit packet changes the priority order.

## R32 Minimal Execution Design

`R32` should inherit the exact `R30` candidate core and stop rules rather than
inventing a new grid:

- `checkpoint_replay_long/u32/h3.0/plus_two/flattened`
- `helper_checkpoint_braid_long/u20/h3.0/plus_two/flattened`
- `subroutine_braid_long/u20/h3.0/plus_two/flattened`
- `helper_checkpoint_braid/u8/h2.0/plus_one/flattened`
- `subroutine_braid/u6/h2.0/plus_one/flattened`

Approved axes remain:

- `unique_address_target`
- `horizon_multiplier`
- `checkpoint_depth`
- `hot_address_skew`

The smallest actionable ladder is family-local and ceiling-relative:

- long families:
  push `unique_address_target` by `+4` then `+8`,
  `horizon_multiplier` by `+0.5` then `+1.0`,
  and `checkpoint_depth` by one notch beyond the current ceiling;
- continuity anchors:
  push `unique_address_target` by `+2` then `+4`,
  `horizon_multiplier` by `+0.5` then `+1.0`,
  and `checkpoint_depth` by one notch beyond the current ceiling;
- prioritize `flattened` first and use `baseline` only as nearby confirmation
  around any reproduced failure.

Required outputs should mirror `R26/R27` where possible:

- `manifest_rows.json`
- `boundary_rows.json`
- `branch_summary.json`
- `positive_rows.json`
- `failure_rows.json`
- `first_fail_digest.json`
- `neighbor_exact_rows.json`
- `localized_boundary.json`
- `summary.json`

The lane stops on the predeclared `R30` rules:

- stop a branch after `2` reproduced exactness failures;
- stop the lane if every branch either fails cleanly or exhausts the ladder
  without a failure;
- require one `first_fail` plus at least one neighboring exact row before any
  localization claim.

## R33 Minimal Execution Design

`R33` remains deferred, but it should be executable without reopening design
work. The recommended first execution packet is a stratified `10`-to-`12` row
audit across the `5` current positive `D0` suites from `R23`, because that is
the smallest honest attribution pass that still tests whether the current lag
is suite-stable or dominated by one executor-local non-retrieval bucket.

Fixed comparator set:

- `spec_reference`
- `lowered_exec_trace`
- `pointer_like_exact`

The first-pass sampling rule should be:

- `2` rows per suite;
- one median `pointer_like_ratio_vs_best_reference` row per suite;
- one worst `pointer_like_ratio_vs_best_reference` row per suite;
- include at least one control-heavy row when the suite offers one.

Escalate from the stratified packet to the full `25` `R23` rows only if
dominant-component rankings remain unstable across suites or the first pass
fails to isolate one credible non-retrieval bucket.

The audit should keep the current aggregate runtime fields and decompose the
existing `pointer_like_exact_non_retrieval_seconds` bucket into bounded
subcomponents that still map back to the current aggregates. The minimum useful
targets are:

- `dispatch_decode_seconds`
- `state_update_bookkeeping_seconds`
- `tensor_python_plumbing_seconds`
- `residual_fixed_overhead_seconds`

Required outputs:

- `sample_manifest.json`
- `component_profile_rows.json`
- `component_profile_rows.csv`
- `suite_component_summary.json`
- `comparator_summary.json`
- `attribution_verdict.json`
- `summary.json`

Kill criteria stay strict:

- if exactness regresses, stop and record a stronger negative;
- if improvement appears only after dropping `spec_reference` or
  `lowered_exec_trace`, stop and keep `R29` blocked;
- if the same non-retrieval bucket dominates in every suite on the stratified
  pass, stop without escalating directly to `R29`;
- if decomposition requires widened suites, widened endpoints, or invasive code
  churn that changes the science target, stop and record an instrumentation
  blocker instead of widening scope.

## Execution Order And Handoff

- Current batch:
  planning only, no new runtime execution.
- Next execution batch:
  `R32` first, from a clean worktree or later explicit next-stage packet.
- `R33`:
  stays deferred until either `R32` finishes or a later packet explicitly
  prioritizes the systems audit.

The concrete next handoff artifacts should therefore be:

- `docs/milestones/R32_d0_family_local_boundary_sharp_zoom/execution_manifest.md`
- `docs/milestones/R33_d0_non_retrieval_overhead_localization_audit/component_localization_manifest.md`
- refreshed milestone `todo.md`, `acceptance.md`, `status.md`, and
  `artifact_index.md` files for both lanes.
