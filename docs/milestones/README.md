# Milestones Index

This directory stores landed milestone packets, sidecars, and preserved prior
decision points.

## Current Live Stack

- `P84_post_p83_keep_set_contraction_and_closeout/`
  current keep-set contraction and closeout wave
- `P83_post_p82_promotion_branch_and_pr_handoff/`
  current promotion branch and PR handoff wave
- `P81_post_p80_locked_fact_rebaseline_and_route_sync/`
  preserved locked-fact and route-sync wave
- `P82_post_p81_clean_main_promotion_probe/`
  preserved clean-main promotion probe wave
- `P77_post_p76_keep_set_and_provenance_normalization/`
  current keep-set and provenance normalization wave
- `P78_post_p77_legacy_worktree_convergence_and_quarantine_sync/`
  current legacy worktree convergence and quarantine sync wave
- `P79_post_p78_archive_claim_boundary_and_reopen_screen/`
  current archive claim boundary and reopen screen wave
- `P80_post_p79_next_planmode_handoff_sync/`
  current next-planmode handoff sync wave
- `P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync/`
  current local hygiene and shrink wave
- `P72_post_p71_archive_polish_and_explicit_stop_handoff/`
  current archive polish and explicit stop handoff wave
- `H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/`
  current active docs-only packet
- `P71_post_p70_clean_descendant_merge_prep_readiness_sync/`
  current clean-descendant merge-prep readiness sync wave
- `P70_post_p69_archive_index_and_artifact_policy_sync/`
  current archive index and artifact policy sync wave
- `P69_post_h65_repo_graph_hygiene_inventory/`
  current repo graph hygiene inventory wave
- `P56_post_h64_clean_merge_candidate_packet/`
  landed clean merge-candidate foundation wave
- `P57_post_h64_paper_submission_package_sync/`
  landed paper/submission package sync foundation wave
- `P58_post_h64_archive_release_closeout_sync/`
  landed archive/release closeout sync foundation wave
- `P59_post_h64_control_and_handoff_sync/`
  landed control/handoff sync foundation wave
- `F38_post_h62_r63_dormant_eligibility_profile_dossier/`
  current dormant future dossier

## Preserved Immediate Publication Lineage

- `P74_post_p73_successor_publication_review/`
  preserved immediate successor publication review wave
- `P75_post_p74_published_successor_freeze/`
  preserved immediate published successor freeze wave
- `P76_post_p75_release_hygiene_and_control_rebaseline/`
  preserved immediate release hygiene and control rebaseline wave
- `P68_post_p67_release_hygiene_and_control_rebaseline/`
  preserved prior release hygiene and control rebaseline wave
- `P67_post_p66_published_successor_freeze/`
  preserved prior published successor freeze wave
- `P66_post_p65_successor_publication_review/`
  preserved prior successor publication review wave

## Preserved Immediate Promotion-Prep Lineage

- `P81_post_p80_locked_fact_rebaseline_and_route_sync/`
  preserved locked-fact rebaseline and route-sync wave immediately below `P83`
- `P82_post_p81_clean_main_promotion_probe/`
  preserved clean-main probe that opened the clean promotion route for `P83`

## Deeper Preserved History

- `P65_post_p64_merge_prep_control_sync/`
  preserved prior merge-prep control sync wave
- `P64_post_p63_release_hygiene_rebaseline/`
  preserved prior release hygiene rebaseline wave
- `P63_post_p62_published_successor_promotion_prep/`
  preserved prior published successor promotion-prep wave
- `H64_post_p53_p54_p55_f38_archive_first_freeze_packet/`
  preserved prior active docs-only packet
- `P62_post_p61_merge_prep_control_sync/`
  preserved older merge-prep control sync wave
- `P61_post_p60_release_hygiene_rebaseline/`
  preserved older release hygiene rebaseline wave
- `P60_post_p59_published_clean_descendant_promotion_prep/`
  preserved older published clean-descendant promotion-prep wave

## Reading Rule

- treat `publication_record/current_stage_driver.md` as the canonical live
  router for which milestone is current;
- treat `P84` as the current keep-set contraction and closeout wave;
- treat `P83` as the current promotion-ready branch handoff wave above the
  published `p75` branch;
- treat `P81/P82` as preserved immediate promotion-prep lineage, not current
  live control;
- treat `P77/P78/P79/P80` as the current archive-first convergence and handoff
  stack underneath `P84/P83`;
- treat `P73` as the current local hygiene and shrink wave above `P72`;
- treat `P72` as the current archive polish and explicit stop handoff wave
  above `H65`;
- treat `P74/P75/P76` as the preserved immediate publication lineage that
  produced the current `p75` branch;
- treat `P69/P70/P71` as hygiene/control sidecars underneath `P72`;
- treat `P66/P67/P68`, `P63/P64/P65`, and `P60/P61/P62` as preserved prior
  live control, not current; and
- treat `F38` as dormant future only, not a live scientific route.
