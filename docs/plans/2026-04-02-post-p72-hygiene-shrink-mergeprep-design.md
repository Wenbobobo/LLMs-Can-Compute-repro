# 2026-04-02 Post-P72 Hygiene Shrink Mergeprep Design

`P72` already froze the archive-facing default as explicit stop or no further
action. The next route should not reopen science. The only productive follow-on
is local hygiene: tighten the current keep-set, move live guidance fully onto
`D:/zWenbo/AI/wt`, aggressively classify legacy local worktrees for safe
shrink, and leave any merge work as dossier-only.

## Recommended Main Route

Prefer hygiene/shrink first, then a non-executing merge-prep dossier. This
dominates archive-only polish because the repo still carries a large legacy
local worktree footprint and the current branch/worktree guidance is not yet as
sharp as the archive freeze posture. It also dominates explicit stop because it
reduces operational drag without reopening any scientific lane.

## Wave 1

- objective:
  export a machine-readable inventory of legacy local worktrees and sync the
  current keep-set
- required inputs:
  `P72` summary, current branch/worktree registry, current stage driver, live
  README/STATUS surfaces, live worktree list
- expected outputs:
  `P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync`,
  `keep_set.md`, `shrink_runbook.md`
- stop conditions:
  any live keep branch still sits under the legacy prefix, or inventory cannot
  classify every legacy worktree
- go/no-go:
  go only if this remains non-runtime, non-merge, and clean-descendant-only
- expected commits:
  docs/scripts/tests for `P73`, then exported `results/P73...`
- worktree/subagent:
  use a clean descendant worktree; explorers may audit candidate shrink sets in
  parallel

## Wave 2

- objective:
  rebaseline live docs so current and future execution points to
  `D:/zWenbo/AI/wt`
- required inputs:
  `P73` inventory, live docs routers, branch registry
- expected outputs:
  updated README/STATUS/router docs with explicit preferred-path policy
- stop conditions:
  a live router still recommends the legacy prefix for new work
- go/no-go:
  go only if historical documents remain factual rather than rewritten
- expected commits:
  docs-only rebaseline folded into the `P73` docs commit or landed immediately
  after
- worktree/subagent:
  same clean descendant worktree; explorer can audit live-doc path drift

## Wave 3

- objective:
  safely remove local legacy worktree directories that are clean and outside
  the preserved keep-set
- required inputs:
  `P73` inventory, shrink runbook, per-path cleanliness checks
- expected outputs:
  reduced local legacy footprint; preserved branch refs remain untouched
- stop conditions:
  dirty candidate, missing path, or ambiguity about whether a branch is still
  needed locally
- go/no-go:
  go only on clean legacy paths; never touch `D:/zWenbo/AI/LLMCompute` or
  anything under `D:/zWenbo/AI/wt`
- expected commits:
  no code changes required; if recorded, land only doc/result refreshes in a
  separate commit
- worktree/subagent:
  same worktree; no parallel destructive actions

## Wave 4

- objective:
  write a non-executing clean-descendant merge-prep dossier rooted at
  `wip/p56-main-scratch`
- required inputs:
  `P71` merge-readiness fact, `P72` stop handoff, current keep-set after shrink
- expected outputs:
  a dossier that states the only admissible later route and keeps merge
  execution out of scope
- stop conditions:
  any path suggests dirty-root integration or reclassifies `P72` as the
  published branch
- go/no-go:
  go only if the dossier stays read-only and conditional on a new external
  integration need
- expected commits:
  docs/results-only packet after shrink is stable
- worktree/subagent:
  same clean descendant worktree; optional reviewer subagent
