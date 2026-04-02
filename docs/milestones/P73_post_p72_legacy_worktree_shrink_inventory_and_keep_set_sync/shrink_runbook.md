# Shrink Runbook

Safety rules before any local removal:

- inspect candidates only under `D:/zWenbo/AI/LLMCompute-worktrees/`
- never touch `D:/zWenbo/AI/LLMCompute`
- never touch any worktree under `D:/zWenbo/AI/wt/`
- do not remove dirty worktrees
- prefer `git worktree remove <path>` for clean legacy paths
- branch refs remain preserved unless there is a separate explicit branch-prune
  decision
- keep `wip/r33-next` unless a later archive-only phase explicitly retires it
