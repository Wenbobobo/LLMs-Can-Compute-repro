# TODO

Legacy note: the remaining unchecked rows are tracked in
`docs/milestones/H1_legacy_backlog_reconciliation/classification_matrix.md`
and are not active on the current frozen paper scope by default.

- [x] Build a structured event codec for trainable labels
- [x] Train a neural decoder over induced transition labels
- [x] Run free-running held-out rollout on countdown, branch, and memory
- Dormant follow-up: replace opcode-only conditioning with a context-richer
  event decoder only if `R4_mechanistic_retrieval_closure` requires it.
- Dormant follow-up: test a richer decoder on the current held-out slice only
  when that branch is explicitly reactivated.
- Dormant follow-up: extend the neural branch to deeper mixed memory/stack
  programs only after `R3` closes the current `D0` exact-execution stress gate.
