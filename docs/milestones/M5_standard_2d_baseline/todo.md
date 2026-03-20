# TODO

Legacy note: the remaining unchecked rows are tracked in
`docs/milestones/H1_legacy_backlog_reconciliation/classification_matrix.md`
and are not active on the current frozen paper scope by default.

- [x] Define the baseline architecture scaffold and structured trace dataset
- [x] Keep logs and claims separate from the hard-max branch
- [x] Install and validate the Torch runtime for this branch
- [x] Run the first teacher-forced baseline training slice
- [x] Evaluate free-running rollout on the same families used in `M4`
- [x] Add a factorized numeric serialization comparison against the original atomic branch
- [x] Add an event-grouped serialization that removes replay-recoverable bookkeeping fields
- Maintenance-only note: keep the current zero-exact baseline reproducible; do
  not pursue rescue work unless `R4` requires one final side-by-side baseline
  table on the current active suite.
- Maintenance-only note: if reactivated, allow at most one clearly motivated
  intervention and compare it against the existing event-grouped artifact.
