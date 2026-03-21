# Status

Provisioned on 2026-03-20 as the required closeout stage after `H16`, and
exported on 2026-03-20 after the landed `R18b` closeout.

- `H17` is downstream of landed `R15/R16/R17` and the closed comparator-only
  `R18` packet;
- it now records one explicit post-`H16` refrozen same-scope state;
- `R18` closes as `r18_runtime_repair_confirmed` on the same endpoint;
- future frontier recheck is no longer silently blocked by missing closeout,
  but it still requires a separate conditional plan before any scope lift;
- the current release/worktree state remains `dirty_worktree_release_commit_blocked`.
