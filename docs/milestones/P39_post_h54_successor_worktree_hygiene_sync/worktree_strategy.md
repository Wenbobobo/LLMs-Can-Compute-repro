# Worktree Strategy

- keep `D:/zWenbo/AI/wt` as the preferred local alias root for future
  worktrees;
- keep `D:/zWenbo/AI/wt/f31` as the preferred alias for the current closed
  execution surface when a short path is useful;
- keep repo-local aliases direct rather than chained through `D:/wt/*`, and
  treat any remaining legacy `D:/wt/*` shortcuts as deprecated;
- keep `f29` preserved as the closed execution surface;
- do new planning in a clean successor worktree under the repo-local `wt`
  root;
- do not run science on dirty root `main`.
