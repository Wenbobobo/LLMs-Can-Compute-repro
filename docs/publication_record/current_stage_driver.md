# Current Stage Driver

## Active Driver

The current active stage is:

- `H64_post_p53_p54_p55_f38_archive_first_freeze_packet`

The current published successor promotion-prep wave is:

- `P63_post_p62_published_successor_promotion_prep`

The current release hygiene rebaseline wave is:

- `P64_post_p63_release_hygiene_rebaseline`

The current merge-prep control sync wave is:

- `P65_post_p64_merge_prep_control_sync`

The current published clean descendant branch is:

- `wip/p63-post-p62-tight-core-hygiene`

The current docs router is:

- `docs/README.md`

The current branch/worktree registry is:

- `docs/branch_worktree_registry.md`

The preserved prior published clean-descendant stack is:

- `P60_post_p59_published_clean_descendant_promotion_prep`
- `P61_post_p60_release_hygiene_rebaseline`
- `P62_post_p61_merge_prep_control_sync`

The preserved prior published clean-descendant branch is:

- `wip/p60-post-p59-published-clean-descendant-prep`

The preserved local integration branch is:

- `wip/p56-main-scratch`

The landed `H64` follow-through foundation is:

- `P56_post_h64_clean_merge_candidate_packet`
- `P57_post_h64_paper_submission_package_sync`
- `P58_post_h64_archive_release_closeout_sync`
- `P59_post_h64_control_and_handoff_sync`

The preserved prior active packet is:

- `H63_post_p50_p51_p52_f38_archive_first_closeout_packet`

The current dormant future dossier is:

- `F38_post_h62_r63_dormant_eligibility_profile_dossier`

The default downstream lane is:

- `archive_or_hygiene_stop`

## Current Machine-State Meaning

- `P56/P57/P58/P59` remain the landed follow-through foundation under `H64`.
- `P63` promotes `wip/p63-post-p62-tight-core-hygiene` into the live published
  successor clean descendant above the preserved `P60/P61/P62` stack.
- `P64` reanchors release hygiene, preflight, and archive-ready posture on
  `wip/p63-post-p62-tight-core-hygiene` while allowing execution from the
  registered successor work branch `wip/p64-post-p63-successor-stack`, and it
  expects `clean_worktree_ready_if_other_gates_green`.
- `P65` keeps the driver, indexes, active-wave file, and next handoff in sync
  with the successor merge-prep posture.
- `wip/p60-post-p59-published-clean-descendant-prep` is preserved as the prior
  published clean descendant, not the live control branch.
- `docs/README.md` and `docs/branch_worktree_registry.md` separate live routing
  from preserved history and local cleanup posture.
- merge posture remains `clean_descendant_only_never_dirty_root_main`.
- dirty root `main` remains quarantine-only.
- `F38` records the only surviving future family as a dormant no-go dossier and
  leaves the key cost-profile fields unresolved.
- `H64` is the current active docs-only packet and selects
  `archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant`.
- archive-first freeze remains the active route.
