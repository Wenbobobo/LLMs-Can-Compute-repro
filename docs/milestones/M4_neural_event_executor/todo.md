# TODO

Legacy note: the remaining unchecked rows are tracked in
`docs/milestones/H1_legacy_backlog_reconciliation/classification_matrix.md`
and are not active on the current frozen paper scope by default.

- [x] Build a structured event codec for trainable labels
- [x] Train a neural decoder over induced transition labels
- [x] Run free-running held-out rollout on countdown, branch, and memory
- [ ] Replace opcode-only conditioning with a context-richer event decoder
- [ ] Test whether the richer decoder keeps exact rollout on the current held-out slice
- [ ] Extend the neural branch to deeper mixed memory/stack programs
