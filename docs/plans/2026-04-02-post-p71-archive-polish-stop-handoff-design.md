# 2026-04-02 Post-P71 Archive Polish Stop Handoff Design

## Recommended Main Route

Archive polish and explicit stop handoff.

This route dominates because the live evidence boundary is already frozen at
`H65 + P66/P67/P68 + H58 + H43`, standing audits are green, runtime remains
closed, and `P71` already captured the only admissible later clean-descendant
merge-prep fact without authorizing merge execution. `P72` therefore stays
strictly on docs/export/control surfaces.

## Wave 1

- objective:
  add a narrow `P72_post_p71_archive_polish_and_explicit_stop_handoff` sidecar
- inputs:
  `P71`, standing green preflight, standing `P10`, live routers
- outputs:
  `P72` exporter, milestone docs, handoff docs, startup prompts
- stop conditions:
  any text surface would require evidence-boundary widening
- go/no-go:
  go only if `P72` remains hygiene-only and non-runtime
- expected commits:
  docs/scripts/tests commit
- worktree or subagent:
  existing clean `p72` worktree only

## Wave 2

- objective:
  re-anchor standing release-facing exporters on the `P72` handoff wording
- inputs:
  updated publication and archive surfaces
- outputs:
  refreshed `release_preflight_checklist_audit` and `P10_submission_archive_ready`
- stop conditions:
  blocked standing audits after wording refresh
- go/no-go:
  go only if audits remain green without new science
- expected commits:
  included in docs/scripts/tests commit
- worktree or subagent:
  existing clean `p72` worktree only

## Wave 3

- objective:
  regenerate machine-readable `P72` plus refreshed standing summaries
- inputs:
  clean docs/scripts/tests tree
- outputs:
  `results/P72...`, refreshed preflight summary, refreshed `P10` summary
- stop conditions:
  any summary turns blocked
- go/no-go:
  go only if outputs remain green and explicit-stop framed
- expected commits:
  results-only commit
- worktree or subagent:
  existing clean `p72` worktree only
