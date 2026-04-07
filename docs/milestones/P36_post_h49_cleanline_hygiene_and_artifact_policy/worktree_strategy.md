# P36 Worktree Strategy

- `D:/zWenbo/AI/LLMCompute-worktrees/h50-next-wave` is the clean execution
  surface for this wave.
- dirty root `main` is not a scientific execution surface.
- `F26/P36` land first on the clean worktree branch.
- `R51` and `R52` should execute from clean descendant worktrees, not from
  dirty root `main`.
- shared integration and final packet closeout stay on the clean line until a
  later explicit merge packet exists.
