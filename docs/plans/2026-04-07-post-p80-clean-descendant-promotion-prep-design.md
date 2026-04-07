# Post-P80 Clean-Descendant Promotion-Prep Design

## Summary

Current state is already scientifically closed and publication-facing green:
`H65` remains the active packet, `P80` is the current handoff wave,
`results/release_preflight_checklist_audit/summary.json` is
`docs_and_audits_green`, and
`results/P10_submission_archive_ready/summary.json` is `archive_ready`.
The live clean branch is `wip/p75-post-p74-published-successor-freeze`; it is
the source for the next clean-descendant integration work.

Recommended main route: keep the scientific conclusion at `explicit stop`, and
use the next phase for hygiene-first clean-descendant promotion/merge-prep.
Do not reopen runtime or same-lane value work. The phase should end with a
verified clean promotion branch plus PR-ready handoff artifacts; actual PR
opening can happen in the same phase only if everything stays green.

## Interfaces And Outputs

- No runtime, model, or public product API changes are in scope.
- New repo-facing outputs are limited to the next control packets/results for
  `P81` to `P84`, plus refreshed control docs and PR/promotion handoff
  artifacts.
- The main control surfaces that must stay aligned are the top-level
  status/router docs, the three post-`P80` plan-entry docs, and the
  publication-record handoff surfaces.
- Default toolchain remains `uv`; all integration work must happen on clean
  descendant worktrees, never on dirty root `main`.

## Wave Plan

### Wave 1: `P81_post_p80_locked_fact_rebaseline_and_route_sync`

- refresh locked facts to the true current state before any promotion-prep
  work;
- update the post-`P80` entry docs, top-level control surfaces, and
  publication-control surfaces so they agree on the live branch head, current
  route, and archive-ready state;
- stop if any control doc can only be reconciled by depending on dirty root
  `main`.

### Wave 2: `P82_post_p81_clean_main_promotion_probe`

- establish a fresh clean `main`-based integration worktree and prove whether
  `p75` can be promoted without touching dirty root `main`;
- capture ahead/behind counts, merge-base, merge viability, and the exact
  verification matrix required for promotion;
- stop if the probe conflicts, if `p75` is behind `origin/main`, or if any
  publication-facing audit regresses.

### Wave 3: `P83_post_p82_promotion_branch_and_pr_handoff`

- turn the successful probe into a promotion-ready branch and PR-ready handoff
  package;
- refresh handoff docs to state whether PR opening is ready now or deferred to
  the next phase;
- stop if promotion introduces verification regressions or widens the
  scientific claim.

### Wave 4: `P84_post_p83_keep_set_contraction_and_closeout`

- shrink the mounted keep set after promotion-prep so the repo is cheaper to
  operate;
- preserve only the branches still needed for live work, keeping dirty root
  `main` plus `h27` explicitly quarantined;
- stop if any targeted branch still holds unpublished or unverified state.

## Test And Acceptance Plan

- Re-run the exporter tests for any touched `P81-P84` scripts plus the standing
  `release_preflight` and `P10` tests.
- Re-run the real exporters so
  `results/release_preflight_checklist_audit/summary.json` stays
  `docs_and_audits_green` and
  `results/P10_submission_archive_ready/summary.json` stays `archive_ready`.
- Verify clean integration facts with `git rev-list --left-right --count`,
  `git merge-base`, merge or fast-forward checks, and `git worktree list`.
- Verify the promotion branch worktree remains clean before any PR/open-remote
  step.

## Assumptions And Defaults

- The true live head at plan start is `53962ca`; any older head value in locked
  facts is stale and must be corrected.
- Dirty root `main` remains quarantine-only throughout.
- Default landing mode is promotion/PR, but actual PR opening is conditional on
  the promotion branch remaining fully green.
- Any future `R63` discussion is out of scope for this phase unless opened by a
  separate plan that proves a materially different non-runtime cost structure.
