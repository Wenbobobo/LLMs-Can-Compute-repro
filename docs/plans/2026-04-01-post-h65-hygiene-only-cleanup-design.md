# 2026-04-01 Post-H65 Hygiene-Only Cleanup Design

## Recommended Main Route

The recommended post-`H65` route is:

`P69 -> P70 -> P71`

where `P69` freezes the post-`H65` tight-core keep set and root-main
quarantine facts, `P70` syncs archive/publication/planning indexes plus the
standing large-artifact policy to that hygiene view, and `P71` records the only
admissible later merge-prep readiness route without executing any merge or
changing the active `H65` packet.

## Locked Constraints

- `H65_post_p66_p67_p68_archive_first_terminal_freeze_packet` remains the
  active docs-only packet
- `P66/P67/P68` remain the current frozen successor stack
- `P56/P57/P58/P59` remain the landed follow-through foundation
- `wip/p66-post-p65-published-successor-freeze` remains the live published
  clean descendant
- dirty root `main` remains quarantine-only
- merge posture remains `clean_descendant_only_never_dirty_root_main`
- runtime remains closed
- `F38/R63` remains dormant and non-runtime only
- no same-lane executor-value reopen is admissible
- no broad Wasm, arbitrary `C`, or transformed/trainable entry is reopened
- no dirty-root integration shortcut is admissible

## Waves

### Wave 1

`P69_post_h65_repo_graph_hygiene_inventory`

- inventory the post-`H65` tight-core keep set and the live clean/dirty split
- require `wip/p56-main-scratch`, `wip/p63-post-p62-tight-core-hygiene`,
  `wip/p64-post-p63-successor-stack`, `wip/h64-post-h63-archive-first-freeze`,
  and `wip/p66-post-p65-published-successor-freeze` to stay clean
- require dirty root `main` to remain parked on
  `wip/root-main-parking-2026-03-24`
- record the linear `p56..p66` and `origin/main..p66` divergence facts

### Wave 2

`P70_post_p69_archive_index_and_artifact_policy_sync`

- sync archive/publication/planning indexes to the `H65 + P69` hygiene view
- preserve `H65` as the active docs-only packet rather than minting `H66`
- reaffirm that large raw-row outputs stay out of git by default and that Git
  LFS remains inactive unless a later explicit review-critical packet says
  otherwise

### Wave 3

`P71_post_p70_clean_descendant_merge_prep_readiness_sync`

- record the only admissible later merge-prep readiness route from
  `wip/p56-main-scratch` to `wip/p66-post-p65-published-successor-freeze`
- require the read-only `git merge-tree` probe to stay conflict-free
- refresh the next plan-mode handoff surfaces while keeping merge execution
  absent and the default downstream lane at
  `explicit_archive_stop_or_hygiene_only`
