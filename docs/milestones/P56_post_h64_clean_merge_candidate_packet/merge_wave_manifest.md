# P56 Merge Wave Manifest

## Fixed Branch Roles

Historical note: the explicit candidate branch/worktree recorded here was later
absorbed locally into `wip/p56-main-scratch` and removed. The branch-role map
below remains the authoritative `P56` packet record.

- clean source branch: `wip/h64-post-h63-archive-first-freeze`
- clean source worktree:
  `D:/zWenbo/AI/wt/h64-post-h63-archive-first-freeze`
- explicit candidate branch: `wip/p56-post-h64-clean-merge-candidate`
- explicit candidate worktree:
  `D:/zWenbo/AI/wt/p56-post-h64-clean-merge-candidate`
- clean `main` scratch branch: `wip/p56-main-scratch`
- clean `main` scratch worktree:
  `D:/zWenbo/AI/wt/p56-main-scratch`
- parked root worktree:
  `D:/zWenbo/AI/LLMCompute`
- parked root branch prefix:
  `wip/root-main-parking`
- target branch: `main`

## Fixed Packet Mode

- `promotion_mode = clean_descendant_merge_candidate`
- `merge_posture = clean_descendant_only_never_dirty_root_main`
- `merge_recommended = false`
- `merge_executed = false`
- no direct merge inside `P56`

## Required Review Conditions

1. confirm `wip/h64-post-h63-archive-first-freeze` is still synced to
   `origin/wip/h64-post-h63-archive-first-freeze`;
2. review one coherent packet range above preserved `H58/H43`:
   `P50 -> P51 -> P52 -> F38 -> H63 -> P53 -> P54 -> P55 -> H64 -> P56`;
3. keep raw-row dumps and tracked oversize artifacts outside the merge set;
4. treat the `main` delta as inventory only, not as merge authorization; and
5. keep dirty root `main` parked and out of conflict resolution.

## Scope Lock

- `P56` does not execute a merge;
- `P56` does not authorize runtime;
- `P56` does not treat `R63` as anything except a dormant non-runtime dossier;
- `P56` does not widen to broad Wasm or arbitrary `C`; and
- `P56` does not route through dirty root `main`.
