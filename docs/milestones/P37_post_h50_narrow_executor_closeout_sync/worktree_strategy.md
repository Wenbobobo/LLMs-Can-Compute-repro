# P37 Worktree Strategy

- `D:/zWenbo/AI/LLMCompute-worktrees/f28-h51-post-h50-origin-mechanism-reentry`
  is the historical clean control surface for the closed wave.
- `D:/zWenbo/AI/LLMCompute-worktrees/r55-origin-2d-hardmax-retrieval-equivalence`
  is the preferred clean execution surface for `R55`.
- `D:/zWenbo/AI/LLMCompute-worktrees/r56-origin-append-only-trace-vm-semantics`
  is the preferred clean execution surface for `R56`.
- `D:/zWenbo/AI/LLMCompute-worktrees/r57-origin-accelerated-trace-vm-comparator`
  is the preferred clean execution surface for `R57` and the preserved
  closeout surface for `H52`.
- dirty root `main` is not a scientific execution surface.
- `F28`, `H51`, and `P37` land first on the clean control worktree branch.
- `R55`, `R56`, and `R57` should execute from descendant clean worktrees, not
  from dirty root `main`.
- `R57` forks only after `R56` fixes an exact row set worth comparing.
- shared integration and final packet closeout stay on the clean line until a
  later explicit merge packet exists.
