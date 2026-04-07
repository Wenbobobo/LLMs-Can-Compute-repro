# Merge And Worktree Policy

- save the current planning document before starting any execution wave;
- branch future work from a clean worktree, not from dirty `main`;
- prefer one isolated worktree per packet family;
- use subagents only for non-overlapping lanes:
  control-surface synthesis,
  future-gate specification,
  repo-hygiene / artifact audit;
- keep `main` untouched until a later hygiene packet reconciles it;
- land planning bundles on their own branch before any runtime gate is
  authorized;
- do not let promotion hygiene or branch cleanup widen scientific scope.
