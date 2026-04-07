# Post-P76 Hygiene-First Convergence Design

Recommended main route: archive-first convergence and explicit-stop packaging.
This dominates speculative science because runtime remains closed, same-lane
executor-value work is inadmissible, and the only honest future gate is a
strictly non-runtime screen.

## Wave 1: P77 Keep-Set And Provenance Normalization

- objective: normalize the active keep set and remote provenance around the live
  `p75` branch
- inputs: `P76`, `README.md`, `STATUS.md`, current stage driver, branch
  registry, plan router
- outputs: `P77` results, updated control surfaces, explicit upstream facts
- stop conditions: keep set or upstream mapping is ambiguous
- go/no-go: go only if `p75`, `p74`, `p73`, `p72`, `p69`, and `p56` are the
  intended tracked keep branches
- expected commits: docs/scripts/tests plus `P77` result export
- new worktree or subagent: no

## Wave 2: P78 Legacy Worktree Convergence And Quarantine Sync

- objective: reduce mounted worktrees to the balanced keep set plus quarantines
- inputs: `P77`, `git worktree list`, branch registry, dirty-count audit
- outputs: `P78` results, updated registry, removed clean legacy mounts
- stop conditions: a supposedly removable legacy mount is dirty or otherwise
  ambiguous
- go/no-go: go only if root dirty checkout and `h27` are the only dirty
  survivors
- expected commits: worktree convergence notes plus `P78` result export
- new worktree or subagent: no

## Wave 3: P79 Archive Claim Boundary And Reopen Screen

- objective: freeze the strongest honest claim boundary and future reopen gate
- inputs: `P78`, publication router, partial-falsification boundary draft,
  future reopen screen draft
- outputs: `P79` results, `partial_falsification_boundary.md`,
  `future_reopen_screen.md`
- stop conditions: claim wording widens beyond narrow mechanism support or
  implies runtime authorization
- go/no-go: go only if the future screen stays strictly non-runtime and
  materially different in cost structure
- expected commits: publication docs plus `P79` result export
- new worktree or subagent: no

## Wave 4: P80 Next-Planmode Handoff Sync

- objective: sync all next-phase prompts to explicit stop or no further action
- inputs: `P79`, plans router, handoff/startup/brief prompt drafts
- outputs: `P80` results and post-`P80` handoff prompts
- stop conditions: prompts accidentally reopen runtime, same-lane
  executor-value work, broad Wasm, arbitrary `C`, transformed/trainable entry,
  or dirty-root integration
- go/no-go: go only if the default prompt route is explicit stop, no further
  action, or hygiene/archive-only work
- expected commits: plan docs plus `P80` result export
- new worktree or subagent: no
