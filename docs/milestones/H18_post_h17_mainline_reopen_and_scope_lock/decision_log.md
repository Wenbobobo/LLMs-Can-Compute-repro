# Decision Log

- Keep `H17_refreeze_and_conditional_frontier_recheck` as the current frozen
  scientific state until `R19/R20/R21` land and `H19` refreezes a new packet.
- Treat the current dirty tree as three explicit buckets:
  - prior-wave `H16/H17/R15/R16/R17/R18` closeout and exporter sync;
  - next-wave runtime workspace for `H18/R19/R20/R21/H19`;
  - later `P13` public-surface and repo-hygiene sync.
- Treat the current modified runtime code under `src/bytecode/` and
  `src/model/` plus the focused executor tests as next-wave runtime workspace
  rather than release-facing sync.
- Keep `release_summary_draft.md` and any future outward-facing short summary
  work in the later `P13` bucket.
- Suggested worktree ownership:
  - `main`: integration and guarded doc sync;
  - `wt-r19`: held-out same-endpoint generalization matrix;
  - `wt-r20`: mechanism ablation matrix;
  - `wt-r21`: exact-executor boundary map;
  - `wt-f2`: future-frontier activation matrix plus `P12` ledger upkeep.
- Do not let a dirty-tree split be interpreted as scientific widening; it is
  only a staging discipline for the next same-scope wave.
