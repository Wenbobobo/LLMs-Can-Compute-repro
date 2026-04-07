# P27 Merge Wave Manifest

## Fixed Branch Roles

- clean scientific source branch: `wip/h41-r43-mainline`
- clean scientific source worktree:
  `D:/zWenbo/AI/LLMCompute-worktrees/h41-r43-mainline`
- explicit merge packet branch: `wip/p27-promotion-merge`
- explicit merge packet worktree:
  `D:/zWenbo/AI/LLMCompute-worktrees/p27-promotion-merge`
- target branch: `main`

## Fixed Packet Mode

- `promotion_mode = explicit_merge_wave`
- `merge_recommended = false`
- `merge_executed = false`
- no direct merge inside `P27`

## Required Review Conditions

1. confirm `wip/h41-r43-mainline` is synced to
   `origin/wip/h41-r43-mainline`;
2. review one coherent packet range above the preserved `H36` base:
   `P25 -> F15 -> H37 -> F16 -> H38 -> P26 -> F17 -> F18 -> F19 -> H40 -> R42 -> F20 -> H41 -> P27`;
3. keep dirty-tree-only files and oversized probes outside the merge set;
4. treat merge readiness as an explicit later operational decision, not a
   consequence of being ahead of `main`.

## Scope Lock

- `P27` does not execute `R43`.
- `P27` does not execute `R45`.
- `P27` does not authorize `R44`.
- `P27` does not reopen `R41`.
- `P27` does not widen the scientific claim boundary.
