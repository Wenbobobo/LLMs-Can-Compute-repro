# P56 Worktree Runbook

Historical note: the original candidate branch/worktree described below was
later absorbed locally into `wip/p56-main-scratch` and removed. Keep using
this runbook as the packet's historical execution record, not as the active
current worktree map.

1. start from `wip/p56-post-h64-clean-merge-candidate`, not dirty root
   `main`;
2. confirm `wip/h64-post-h63-archive-first-freeze` is synced to
   `origin/wip/h64-post-h63-archive-first-freeze`;
3. confirm dirty root `main` is still parked via
   `git worktree list --porcelain`;
4. inspect `git diff --stat main..wip/h64-post-h63-archive-first-freeze`;
5. inspect the packet-only candidate delta against
   `wip/h64-post-h63-archive-first-freeze`;
6. use `wip/p56-main-scratch` only as a clean `main` comparison snapshot;
7. perform dry conflict inspection only inside the clean descendant worktrees;
8. never treat `D:/zWenbo/AI/LLMCompute` as an integration base or conflict
   resolution source.
