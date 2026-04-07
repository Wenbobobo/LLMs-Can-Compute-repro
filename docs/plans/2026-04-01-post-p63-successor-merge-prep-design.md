# 2026-04-01 Post-P63 Successor Merge-Prep Design

## Recommended Main Route

The recommended post-`P63` route is:

`P63 -> P64 -> P65`

where `P63` promotes the clean successor branch above the preserved
`P60/P61/P62` stack, `P64` reanchors stateful release hygiene on that branch,
and `P65` refreshes current control and next-entrypoint surfaces.

## Locked Facts

- `H64_post_p53_p54_p55_f38_archive_first_freeze_packet` remains the active
  docs-only packet.
- `P56/P57/P58/P59` remain the landed follow-through beneath the new wave.
- `P60/P61/P62` remain preserved as the prior published clean-descendant stack.
- dirty root `main` remains quarantine-only.
- merge posture remains `clean_descendant_only_never_dirty_root_main`.
- runtime remains closed.
- `F38` / `R63` remain dormant and non-runtime only.

## Waves

### Wave 1

`P63_post_p62_published_successor_promotion_prep`

- promote `wip/p63-post-p62-tight-core-hygiene` into the live published clean
  descendant
- preserve `wip/p60-post-p59-published-clean-descendant-prep` as the prior
  published clean descendant
- keep merge execution absent

### Wave 2

`P64_post_p63_release_hygiene_rebaseline`

- refresh stateful hygiene and outward-release audits from the published
  successor branch
- require `clean_worktree_ready_if_other_gates_green`,
  `docs_and_audits_green`, and `archive_ready`

### Wave 3

`P65_post_p64_merge_prep_control_sync`

- refresh current driver, indexes, active-wave state, and next startup prompt
- terminate at review/merge-prep or explicit archive-first stop
