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
- [ ] Improve free-running rollout above the current zero-exact baseline
- [ ] Decide whether the next intervention should target prompt boundary, architecture, or whether `M5` should freeze as a negative control
