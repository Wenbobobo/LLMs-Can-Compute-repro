# Decision Log

- Keep `H19_refreeze_and_next_scope_decision` as the frozen input until
  `R22/R23` both land and `H21` refreezes the next packet.
- Treat the current dirty tree as three explicit operational buckets:
  - prior-wave `H18/H19/P13` closeout and guarded doc sync;
  - next-wave runtime science for `R22/R23/H21`;
  - background `P12` claim/evidence/manifest upkeep.
- Suggested worktree ownership:
  - `main`: integration, focused validation, final commit and push;
  - `wt-h20`: reentry split and hygiene guard only;
  - `wt-r22`: true executor-boundary localization only;
  - `wt-r23`: same-endpoint systems-overturn gate only;
  - `wt-p12`: claim/evidence/manifests only.
- Treat the dirty-tree split as an operational control problem, not as
  contradictory science.
- Keep root/publication outward wording downstream until `H21` lands.
