# P27 Worktree Runbook

1. start from `wip/p27-promotion-merge`, not dirty `main`;
2. fast-forward from `wip/h41-r43-mainline` before editing the packet;
3. confirm `wip/h41-r43-mainline` is synced to
   `origin/wip/h41-r43-mainline`;
4. inspect `git diff --stat main..wip/h41-r43-mainline`;
5. land only the operational `P27` packet docs, exporter, test, and compact
   result summaries on `wip/p27-promotion-merge`;
6. push the explicit merge packet branch separately from the scientific source
   branch;
7. merge only after one later explicit review concludes that the packet range
   is coherent and the target branch is clean enough;
8. do not execute `R43` or `R45` inside `P27`; keep them in separate
   downstream worktrees.
