# Current Stage Driver

## Active Driver

The current active stage is:

- `H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`

The current archive polish and explicit stop handoff wave is:

- `P72_post_p71_archive_polish_and_explicit_stop_handoff`

The current repo graph hygiene inventory wave is:

- `P69_post_h65_repo_graph_hygiene_inventory`

The current archive index and artifact policy sync wave is:

- `P70_post_p69_archive_index_and_artifact_policy_sync`

The current merge-prep readiness sync wave is:

- `P71_post_p70_clean_descendant_merge_prep_readiness_sync`

The current successor publication review wave is:

- `P66_post_p65_successor_publication_review`

The current published successor freeze wave is:

- `P67_post_p66_published_successor_freeze`

The current release hygiene and control rebaseline wave is:

- `P68_post_p67_release_hygiene_and_control_rebaseline`

The current hygiene-only cleanup branch is:

- `wip/p69-post-h65-hygiene-only-cleanup`

The current archive polish and explicit stop handoff branch is:

- `wip/p72-post-p71-archive-polish-stop-handoff`

The current published clean descendant branch is:

- `wip/p66-post-p65-published-successor-freeze`

The current docs router is:

- `docs/README.md`

The current branch/worktree registry is:

- `docs/branch_worktree_registry.md`

The preserved prior successor stack is:

- `P63_post_p62_published_successor_promotion_prep`
- `P64_post_p63_release_hygiene_rebaseline`
- `P65_post_p64_merge_prep_control_sync`

The preserved prior published clean-descendant branch is:

- `wip/p63-post-p62-tight-core-hygiene`

The preserved prior successor review branch is:

- `wip/p64-post-p63-successor-stack`

The preserved older published clean-descendant stack is:

- `P60_post_p59_published_clean_descendant_promotion_prep`
- `P61_post_p60_release_hygiene_rebaseline`
- `P62_post_p61_merge_prep_control_sync`

The preserved local integration branch is:

- `wip/p56-main-scratch`

The landed `H64` follow-through foundation is:

- `P56_post_h64_clean_merge_candidate_packet`
- `P57_post_h64_paper_submission_package_sync`
- `P58_post_h64_archive_release_closeout_sync`
- `P59_post_h64_control_and_handoff_sync`

The preserved prior active packet is:

- `H64_post_p53_p54_p55_f38_archive_first_freeze_packet`

The current dormant future dossier is:

- `F38_post_h62_r63_dormant_eligibility_profile_dossier`

The default downstream lane is:

- `explicit_archive_stop_or_hygiene_only`

## Current Machine-State Meaning

- `P56/P57/P58/P59` remain the landed follow-through foundation under the
  preserved `H64` packet.
- `P66` reviews the exact `p63..p64` successor delta and keeps the publication
  decision scoped to docs/export/control/release surfaces.
- `P67` promotes `wip/p66-post-p65-published-successor-freeze` into the live
  published clean descendant above the preserved `P63/P64/P65` stack.
- `P68` reanchors release hygiene, preflight, archive-ready posture, and
  current control on `wip/p66-post-p65-published-successor-freeze` while
  expecting `clean_worktree_ready_if_other_gates_green`.
- `P69` inventories the post-`H65` keep set, records root-main quarantine,
  and freezes the `p56..p66` plus `origin/main..p66` topology facts.
- `P70` syncs archive/publication/planning indexes and the standing artifact
  policy to the `H65 + P69` hygiene-only cleanup state.
- `P71` records the only admissible later merge-prep readiness route from
  `wip/p56-main-scratch` to `wip/p66-post-p65-published-successor-freeze`
  without executing any merge.
- `P72` normalizes archive-facing and plan-facing surfaces around explicit
  stop, no further action, and later clean-descendant merge-prep planning only
  if a new external integration need appears.
- `wip/p63-post-p62-tight-core-hygiene` is preserved as the prior published
  clean descendant, not the live control branch.
- `wip/p64-post-p63-successor-stack` is preserved as the reviewed
  pre-publication successor lane, not the live control branch.
- `wip/p69-post-h65-hygiene-only-cleanup` is the current hygiene-only cleanup
  branch, not the live published clean descendant.
- `wip/p72-post-p71-archive-polish-stop-handoff` is the current archive polish
  and explicit stop handoff branch.
- `docs/README.md` and `docs/branch_worktree_registry.md` separate live routing
  from preserved history and quarantine posture.
- merge posture remains `clean_descendant_only_never_dirty_root_main`.
- dirty root `main` remains quarantine-only.
- `F38` records the only surviving future family as a dormant no-go dossier and
  leaves the key cost-profile fields unresolved.
- `H65` is the current active docs-only packet and selects
  `archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop`.
- explicit stop or no further action is now the recommended downstream route.
- later clean-descendant merge-prep planning only if a new external
  integration need appears.
