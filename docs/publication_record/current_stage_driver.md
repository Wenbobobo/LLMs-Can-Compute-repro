# Current Stage Driver

## Active Driver

The current active stage is:

- `H66_post_p90_archive_replace_terminal_stop_packet`

The current next-planmode handoff sync wave is:

- `P91_post_h66_next_planmode_handoff_sync`

The current archive-replace screen and replacement-decision wave is:

- `P90_post_p89_archive_replace_screen_and_replacement_decision`

The current docs-consolidation and live-router sync wave is:

- `P89_post_p88_docs_consolidation_and_live_router_sync`

The current salvage-screen and no-import decision wave is:

- `P88_post_p87_salvage_screen_and_no_import_decision`

The current paper-spine refresh and salvage shortlist wave is:

- `P87_post_p86_paper_spine_refresh_and_salvage_shortlist`

The current dirty-root inventory and archive-replace map wave is:

- `P86_post_p85_dirty_root_inventory_and_archive_replace_map`

The current merged-main rebaseline and control-resync wave is:

- `P85_post_p84_main_rebaseline_and_control_resync`

The current keep-set contraction and closeout wave is:

- `P84_post_p83_keep_set_contraction_and_closeout`

The current promotion branch and PR handoff wave is:

- `P83_post_p82_promotion_branch_and_pr_handoff`

The current live convergence and handoff stack is:

- `P91_post_h66_next_planmode_handoff_sync`
- `H66_post_p90_archive_replace_terminal_stop_packet`
- `P90_post_p89_archive_replace_screen_and_replacement_decision`
- `P89_post_p88_docs_consolidation_and_live_router_sync`
- `P88_post_p87_salvage_screen_and_no_import_decision`
- `P87_post_p86_paper_spine_refresh_and_salvage_shortlist`
- `P86_post_p85_dirty_root_inventory_and_archive_replace_map`
- `P85_post_p84_main_rebaseline_and_control_resync`
- `P84_post_p83_keep_set_contraction_and_closeout`
- `P83_post_p82_promotion_branch_and_pr_handoff`
- `P77_post_p76_keep_set_and_provenance_normalization`
- `P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`
- `P79_post_p78_archive_claim_boundary_and_reopen_screen`
- `P80_post_p79_next_planmode_handoff_sync`

The current clean rebaseline branch is:

- `wip/p85-post-p84-main-rebaseline`

The current local execution-side control stack is:

- `P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync`
- `P72_post_p71_archive_polish_and_explicit_stop_handoff`
- `P71_post_p70_clean_descendant_merge_prep_readiness_sync`
- `P70_post_p69_archive_index_and_artifact_policy_sync`
- `P69_post_h65_repo_graph_hygiene_inventory`

The current mounted keep branches are:

- `wip/p85-post-p84-main-rebaseline`
- `wip/p83-post-p82-promotion-branch-and-pr-handoff`
- `wip/p75-post-p74-published-successor-freeze`
- `wip/p74-post-p73-successor-publication-review`
- `wip/p73-post-p72-hygiene-shrink-mergeprep`
- `wip/p72-post-p71-archive-polish-stop-handoff`
- `wip/p69-post-h65-hygiene-only-cleanup`
- `wip/p56-main-scratch`

The quarantined dirty survivors are:

- `wip/root-main-parking-2026-03-24`
- `wip/h27-promotion`

The preserved immediate publication lineage is:

- `P74_post_p73_successor_publication_review`
- `P75_post_p74_published_successor_freeze`
- `P76_post_p75_release_hygiene_and_control_rebaseline`

The preserved prior lineage is:

- `P66_post_p65_successor_publication_review`
- `P67_post_p66_published_successor_freeze`
- `P68_post_p67_release_hygiene_and_control_rebaseline`
- `P63_post_p62_published_successor_promotion_prep`
- `P64_post_p63_release_hygiene_rebaseline`
- `P65_post_p64_merge_prep_control_sync`

The current dormant future dossier is:

- `F38_post_h62_r63_dormant_eligibility_profile_dossier`

The default downstream lane is:

- `explicit_stop_or_no_further_action_archive_first`

## Current Machine-State Meaning

- `H66` promotes the completed archive-replace screen into the current
  terminal-stop packet, preserves `H65` as the prior active docs-only state,
  and defaults the downstream route to explicit stop, archive polish, or no
  further action.
- `P91` synchronizes the next planning prompts to the `H66` terminal-stop
  posture and keeps any later `R63` discussion strictly non-runtime.
- `P90` screens the remaining dirty-root publication docs still marked as
  salvage-later in `P86`, closes them as keep-clean/archive-root-only
  decisions, and narrows the next route to the archive-then-replace closeout
  packet `H66_post_p90_archive_replace_terminal_stop_packet` unless a later
  file-specific salvage case appears.
- `P89` consolidates the live router surfaces around the clean `p85` branch,
  makes docs consolidation the current control wave, and narrows the next
  route to archive-then-replace closeout or explicit stop unless a later
  file-specific salvage case appears.
- `P88` screens the first-tier selective-salvage candidates and lands a
  no-import decision for the four highest-value remaining publication docs,
  because the dirty-root versions are stale or not materially better than the
  clean-branch versions.
- `P87` refreshes the paper-facing spine on the clean branch, aligns the
  release summary and paper bundle status to the live `H65 + P86 + P85`
  posture, and records the current salvage shortlist for dirty-root
  publication docs.
- `P86` inventories the dirty root as a quarantine-only external source,
  classifies parked root paths into duplicate/obsolete, salvage-candidate, and
  archive-only buckets, and narrows follow-through to docs consolidation,
  selective salvage-only import, paper spine refresh, and only then
  archive-then-replace closeout.
- `P85` rebaselines current control onto merged `main`, preserving `p83` only
  as short-term merged-source lineage while shifting the active engineering
  route into root archive/replace, docs consolidation, and paper spine
  refresh.
- `P84` contracts the mounted keep set around `p83`, `p75`, `p74`, `p73`,
  `p72`, `p69`, and `p56`, while preserving `p81` and `p82` as unmounted
  immediate promotion-prep lineage.
- `P83` materializes the clean promotion branch and PR handoff from the
  successful `P82` clean-main probe without using dirty root `main`.
- `P81` rebaselines the locked facts to the published `p75` head `53962ca`,
  keeps `release_preflight` at `docs_and_audits_green`, keeps `P10` at
  `archive_ready`, and opens clean-descendant promotion-prep without reopening
  runtime.
- `P77` normalizes the active keep set around `p75`, `p74`, `p73`, `p72`,
  `p69`, and `p56`, and requires explicit upstream provenance.
- `P78` converges mounted worktrees to that balanced set and preserves only the
  dirty root checkout plus `wip/h27-promotion` as quarantined survivors.
- `P79` packages the strongest honest archive-facing statement: narrow
  mechanism support remains, the executor-value lane is closed, and any future
  gate must remain strictly non-runtime and cost-structure-different.
- `P80` synchronizes all next-planmode prompts to default to explicit stop, no
  further action, archive polish, hygiene-only cleanup, or merge-prep
  documentation work only.
- `P74/P75/P76` remain the preserved immediate publication lineage that
  produced the live `wip/p75-post-p74-published-successor-freeze` branch.
- `wip/p74-post-p73-successor-publication-review` remains the current review
  branch.
- `wip/p85-post-p84-main-rebaseline` remains the current clean rebaseline
  branch above merged `main`.
- `wip/p83-post-p82-promotion-branch-and-pr-handoff` remains preserved
  merged-source branch lineage after the landed PR #12 merge.
- `wip/p64-post-p63-successor-stack` remains the preserved deeper review
  lineage, not a live control branch.
- `wip/p73-post-p72-hygiene-shrink-mergeprep` remains the current local hygiene
  and shrink branch.
- `wip/p72-post-p71-archive-polish-stop-handoff` remains the current archive
  polish and explicit stop handoff branch.
- `wip/p69-post-h65-hygiene-only-cleanup` remains the current hygiene-only
  cleanup branch.
- `wip/p56-main-scratch` remains the preserved local integration branch.
- `docs/README.md` and `docs/branch_worktree_registry.md` separate live routing
  from preserved history and quarantine posture.
- merge posture remains `clean_descendant_only_never_dirty_root_main`.
- dirty root `main` remains quarantine-only.
- runtime remains closed.
- `F38` records the only surviving future family as a dormant dossier; any
  later `R63` discussion must stay strictly non-runtime.
- `H65_post_p66_p67_p68_archive_first_terminal_freeze_packet` remains the
  preserved prior active packet immediately below `H66`.
- `explicit_stop_or_no_further_action_archive_first` remains the default
  downstream lane label.
- `H66` remains the current active docs-only packet and selects
  `archive_replace_terminal_stop_becomes_current_active_route_and_defaults_to_explicit_stop`.
- `H66_post_p90_archive_replace_terminal_stop_packet`, then explicit stop or
  no further action, are now the recommended downstream routes after the
  archive-then-replace closeout screen, unless a later file-specific salvage
  case appears.
