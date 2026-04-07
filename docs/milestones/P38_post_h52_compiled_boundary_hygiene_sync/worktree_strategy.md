# Worktree Strategy

- The clean `f29-post-h52-compiled-boundary-reentry` worktree is the control
  and execution surface for `F29/H53/P38/R58/R59/H54`.
- Dirty root `main` is not a scientific execution surface.
- If later sidecar work needs isolation, use successor clean worktrees rather
  than reopening dirty root `main`.
- Preserve packet-sized commits and results on the clean `F29` worktree only.
