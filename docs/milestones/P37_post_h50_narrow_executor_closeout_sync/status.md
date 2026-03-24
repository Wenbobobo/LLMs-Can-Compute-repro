# P37 Status

- completed operational/docs sync packet after landed `H50` and landed `H51`;
- preserves `H52` as the current active docs-only closeout;
- preserves `H51` as the preserved prior mechanism-reentry packet;
- preserves `H50` as the preserved prior broader-route closeout;
- preserves `H43` as the current paper-grade endpoint;
- preserves the clean `F28/H51` worktree as the historical control surface
  for the closed wave;
- keeps descendant clean worktrees as the only scientific execution surfaces
  for `R55`, `R56`, and `R57`;
- quarantines dirty root `main` from scientific execution;
- keeps `merge_executed = false` explicit and keeps `main` untouched during
  `F28/H51/R55/R56/R57/H52`;
- codifies compact-summary-in-git and raw-row-dump-out-of-git defaults,
  `.gitignore`-backed raw-row ignore rules, and zero tracked `>=10 MiB`
  artifacts in the clean worktree; and
- records the commit cadence for planning, docs-only packets, exact gates, the
  comparator gate, and the final decision packet after the lane closes to
  `no_active_downstream_runtime_lane`.
- leaves no further execution task open on this branch.
