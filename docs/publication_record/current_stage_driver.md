# Current Stage Driver

## Active Driver

The current active stage is:

- `H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`

The current keep-set contraction and closeout wave is:

- `P84_post_p83_keep_set_contraction_and_closeout`

The current promotion branch and PR handoff wave is:

- `P83_post_p82_promotion_branch_and_pr_handoff`

The current live convergence and handoff stack is:

- `P84_post_p83_keep_set_contraction_and_closeout`
- `P83_post_p82_promotion_branch_and_pr_handoff`
- `P77_post_p76_keep_set_and_provenance_normalization`
- `P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`
- `P79_post_p78_archive_claim_boundary_and_reopen_screen`
- `P80_post_p79_next_planmode_handoff_sync`

The current promotion-ready branch is:

- `wip/p83-post-p82-promotion-branch-and-pr-handoff`

The current local execution-side control stack is:

- `P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync`
- `P72_post_p71_archive_polish_and_explicit_stop_handoff`
- `P71_post_p70_clean_descendant_merge_prep_readiness_sync`
- `P70_post_p69_archive_index_and_artifact_policy_sync`
- `P69_post_h65_repo_graph_hygiene_inventory`

The current mounted keep branches are:

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
- `wip/p83-post-p82-promotion-branch-and-pr-handoff` remains the current
  promotion-ready branch above the published `p75` branch.
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
- `H65` remains the current active docs-only packet and still selects
  `archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop`.
- explicit stop and no further action are now the recommended downstream route.
