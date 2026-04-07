Current locked facts:

- Active docs-only packet:
  `H66_post_p90_archive_replace_terminal_stop_packet`.
- Preserved prior active packet:
  `H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`.
- Current archive-replace screen wave:
  `P90_post_p89_archive_replace_screen_and_replacement_decision`.
- Current handoff-sync wave:
  `P91_post_h66_next_planmode_handoff_sync`.
- Current clean execution branch:
  `wip/p85-post-p84-main-rebaseline`.
- Dirty root remains quarantine-only.
- Runtime remains closed.

Please in plan mode:

1. Recommend one main next route first: `explicit stop`, `archive polish`,
   `hygiene-only cleanup`, or `no further action`.
2. Do not reopen runtime, same-lane executor-value work, broad Wasm,
   arbitrary `C`, transformed/trainable entry, or dirty-root integration.
3. Only discuss r63 if it remains strictly non-runtime and does not become
   a runtime authorization.
4. Write the next phase as explicit waves with objective, inputs, outputs,
   stop conditions, go/no-go, expected commits, and whether a new worktree or
   subagent is needed.
