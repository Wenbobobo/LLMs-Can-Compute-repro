# Active Wave Plan

## Current Wave

`P12_manuscript_and_manifest_maintenance`

## Immediate Objectives

1. Treat `H21_refreeze_after_r22_r23` as the current frozen scientific input.
2. Align claim ladders, evidence tables, manifests, and negative-result ledgers
   to the landed `R22/R23/H21` packet without widening scope.
3. Keep `README.md`, `STATUS.md`, and publication-facing summaries downstream of
   the landed mixed systems result.
4. Keep `P13` limited to later outward-sync and commit-split hygiene rather
   than treating it as the immediate next science or writing lane.

## Suggested Worktree Map

Use these after the next path-scoped doc closeout commit:

- `wip/p12-ledger` -> sibling worktree `../LLMCompute-wt-p12`
- `wip/p13-hygiene` -> sibling worktree `../LLMCompute-wt-p13`
- `wip/f2-planning` -> sibling worktree `../LLMCompute-wt-f2`

Suggested ownership:

- main agent: `main`
- worker A: `wt-p12`
- worker B: `wt-p13`
- background worker: `wt-f2`

## Acceptance For This Wave

- `H21` is the frozen handoff anchor for the current wave;
- `P12` documents the post-`R22/R23/H21` claim and manifest impact explicitly;
- `P13` is recorded as downstream-only rather than immediate next priority;
- no widened runtime scope, frontend widening, or softened mixed-systems prose
  is introduced in this wave.

## If Blocked

- first continue with `P12` ledger upkeep if one root/publication doc is
  blocked;
- then tighten the current split map and `P13` hygiene notes rather than
  opening a new science lane early;
- do not start widened runtime, repair, or frontend experiments.
