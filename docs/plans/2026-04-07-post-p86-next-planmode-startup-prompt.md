Current locked facts:

- Active docs-only packet:
  `H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`.
- Current root inventory wave:
  `P86_post_p85_dirty_root_inventory_and_archive_replace_map`.
- Preserved merged-main rebaseline wave:
  `P85_post_p84_main_rebaseline_and_control_resync`.
- Current clean execution branch:
  `wip/p85-post-p84-main-rebaseline`.
- Dirty root branch:
  `wip/root-main-parking-2026-03-24`.
- Dirty root remains quarantine-only and has now been classified into
  `duplicate_or_obsolete`, `salvage_candidate`, and `archive_only`.
- Runtime remains closed.

Please in plan mode:

1. Recommend one main next route first: docs consolidation, selective
   salvage-only import, paper spine refresh, archive-then-replace closeout, or
   explicit stop.
2. Do not reopen runtime, same-lane executor-value work, broad Wasm,
   arbitrary `C`, transformed/trainable entry, or dirty-root integration.
3. Treat the dirty root only as an external salvage source. Any import must be
   selective, clean-descendant-only, and justified against the current live
   control surfaces.
4. Write the next phase as explicit waves with objective, inputs, outputs,
   stop conditions, go/no-go, expected commits, and whether a new worktree or
   subagent is needed.
