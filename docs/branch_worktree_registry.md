# Branch And Worktree Registry

This file records the current tight-core keep set, quarantine posture, and
cleanup priorities for the clean-descendant-only repo state after the `H65`
terminal freeze.

## Tight Core Keep Set

| Role | Branch | Path | State | Policy |
| --- | --- | --- | --- | --- |
| current hygiene-only cleanup branch | `wip/p69-post-h65-hygiene-only-cleanup` | `D:/zWenbo/AI/wt/p69-post-h65-hygiene-only-cleanup` | current hygiene-only execution lane above the live published branch | keep as the current repo-hygiene and handoff-sync branch; do not treat it as a replacement published branch |
| current published frozen clean descendant | `wip/p66-post-p65-published-successor-freeze` | `D:/zWenbo/AI/wt/p66-post-p65-published-successor-freeze` | clean published source and active freeze lane | keep as the stable post-`P65` published frozen successor |
| preserved prior successor review lane | `wip/p64-post-p63-successor-stack` | `D:/zWenbo/AI/wt/p64-post-p63-successor-stack` | preserved reviewed pre-publication lane | keep for review provenance and lineage; do not treat as live control |
| preserved prior published clean descendant | `wip/p63-post-p62-tight-core-hygiene` | `D:/zWenbo/AI/wt/p63-post-p62-tight-core-hygiene` | preserved prior published source | keep preserved for lineage and archive packaging; do not treat as live control |
| preserved older published clean descendant | `wip/p60-post-p59-published-clean-descendant-prep` | `D:/zWenbo/AI/wt/p60-post-p59-published-clean-descendant-prep` | older preserved published source | keep preserved for deep lineage and archive packaging |
| preserved local integration base | `wip/p56-main-scratch` | `D:/zWenbo/AI/wt/p56-main-scratch` | local integration ancestry only | keep preserved; do not treat as the live published branch |
| dirty-root quarantine | `wip/root-main-parking-2026-03-24` | `D:/zWenbo/AI/LLMCompute` | operationally dirty root checkout | quarantine only; never use as a clean integration base |

## Historical But Preserved

- the archive-first docs-only chain under `D:/zWenbo/AI/wt/`
  (`wip/h64-post-h63-archive-first-freeze`,
  `wip/f38-post-h62-archive-first-closeout`,
  `wip/f37-post-h61-hygiene-first-reauth-prep`,
  `wip/f36-post-h60-archive-first-consolidation`,
  `wip/f34-post-h59-archive-and-reopen-screen`,
  `wip/f32-post-h56-last-discriminator`) remains read-only historical support
  for the current closeout posture
- older worktrees under `D:/zWenbo/AI/LLMCompute-worktrees/` are preserved
  historical branches; no new active work should start there during this phase
- `wip/r33-next` at `D:/zWenbo/AI/LLMCompute-worktrees/r33-next` remains the
  only preserved tip of the old `p16 -> r32 -> r33` ancestor chain

## Cleanup Status

- the local-only ancestor chain
  `wip/p16-h25-clean -> wip/r32-next -> wip/r33-next` is no longer part of the
  active route
- local pruning has already removed `wip/p16-h25-clean` and `wip/r32-next`
  plus their corresponding worktrees
- `wip/r33-next` is the only retained historical tip from that chain

## Merge Rules

- merge posture remains `clean_descendant_only_never_dirty_root_main`
- `wip/p69-post-h65-hygiene-only-cleanup` is the current hygiene-only cleanup
  execution lane
- `wip/p66-post-p65-published-successor-freeze` is the live published clean
  source for current control wording
- `wip/p64-post-p63-successor-stack` is preserved as the reviewed
  pre-publication lane, not a live execution successor
- `wip/p63-post-p62-tight-core-hygiene` is preserved as the prior published
  clean descendant
- `wip/p56-main-scratch...wip/p66-post-p65-published-successor-freeze = 0/18`
  remains the only admissible later clean-descendant merge-prep topology fact
- `origin/main...wip/p66-post-p65-published-successor-freeze = 0/159` keeps
  dirty-root integration out of bounds
- runtime remains closed
- `F38/R63` remains dormant and non-runtime only
