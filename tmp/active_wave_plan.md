# Active Wave Plan

## Current Wave

Current scientific/control stack:

- current active decision packet:
  `H27_refreeze_after_r32_r33_same_endpoint_decision`;
- current boundary refreeze packet:
  `H26_refreeze_after_r32_boundary_sharp_zoom`;
- completed bounded systems-audit lane:
  `R33_d0_non_retrieval_overhead_localization_audit`;
- blocked future lanes:
  `R29_d0_same_endpoint_systems_recovery_execution_gate` and
  `F3_post_h23_scope_lift_decision_bundle`;
- future frontier review:
  `F2_future_frontier_recheck_activation_matrix` remains planning-only.

Immediate active wave:

no active runtime wave

This downstream wave is closed. `R32 -> H26 -> R33 -> H27` executed from
isolated next-stage worktrees, and no further runtime lane should open by
momentum before a new explicit plan-mode packet is saved.

## Current Facts

- `R32` executed `60/60` bounded candidates and ended at
  `grid_extended_still_not_localized`.
- `H26` froze that boundary result and preserved deferred `R33` as justified
  next.
- `R33` executed `12/12` exact audited rows and ended at
  `suite_stable_noncompetitive_after_localization`.
- `R33` localized the dominant non-retrieval component to
  `state_update_bookkeeping_seconds` across all five audited suites.
- `H27` freezes the post-`R33` systems reading as
  `systems_more_sharply_negative`.
- `R29` and `F3` remain blocked; `F2` remains planning-only.

## Immediate Objectives

1. Preserve `H27` as the current active routing packet.
2. Preserve `H26` and `R33` as the current bounded post-`H25` evidence base.
3. Avoid opening any new runtime lane until a later explicit planning packet is
   written and saved.
4. Keep `R29`, `F3`, and frontier work blocked unless a later packet changes
   their preconditions.

## Last Completed Order

Immediate completed order:

`P16_h25_commit_hygiene_and_clean_worktree_promotion` ->
clean-worktree `R32_d0_family_local_boundary_sharp_zoom` ->
`H26_refreeze_after_r32_boundary_sharp_zoom` ->
clean-worktree `R33_d0_non_retrieval_overhead_localization_audit` ->
`H27_refreeze_after_r32_r33_same_endpoint_decision`

## Next Required Order

new explicit planning packet ->
any later justified runtime lane

## Validation Snapshot

- `uv run pytest tests/test_export_r33_d0_non_retrieval_overhead_localization_audit.py
  tests/test_export_h27_refreeze_after_r32_r33_same_endpoint_decision.py`
  passed in `wt-r33` (`6 passed`).
- `results/R33_d0_non_retrieval_overhead_localization_audit/summary.json`
  reports
  `lane_verdict = suite_stable_noncompetitive_after_localization`.
- `results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`
  should remain the current downstream routing reference after export.

## Current References

- `docs/plans/2026-03-22-post-unattended-r32-mainline-design.md`
- `docs/plans/2026-03-22-post-h25-r32-r33-near-term-design.md`
- `docs/milestones/R32_d0_family_local_boundary_sharp_zoom/`
- `docs/milestones/H26_refreeze_after_r32_boundary_sharp_zoom/`
- `docs/milestones/R33_d0_non_retrieval_overhead_localization_audit/`
- `docs/milestones/H27_refreeze_after_r32_r33_same_endpoint_decision/`
- `results/H26_refreeze_after_r32_boundary_sharp_zoom/summary.json`
- `results/R33_d0_non_retrieval_overhead_localization_audit/summary.json`
- `results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`

## If Blocked

- do not reopen `R29` or `F3` by momentum;
- do not treat `R33` localization as automatic same-endpoint recovery
  authorization;
- do not open a new runtime lane without a new explicit plan-mode packet.
