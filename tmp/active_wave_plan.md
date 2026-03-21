# Active Wave Plan

## Current Wave

`R24_d0_boundary_localization_zoom_followup` + `R25_d0_same_endpoint_systems_recovery_hypotheses`

## Immediate Objectives

1. Treat `H21_refreeze_after_r22_r23` as the current frozen scientific input.
2. Keep `P12_manuscript_and_manifest_maintenance` preserved as the completed
   post-`H21` ledger/manuscript closeout packet rather than reopening it.
3. Pre-lay `R24_d0_boundary_localization_zoom_followup` as the boundary-first
   planning package for a later explicit reopen decision.
4. Park `R25_d0_same_endpoint_systems_recovery_hypotheses` as same-endpoint
   systems notes without treating it as an active repair lane.
5. Leave `P13` downstream-only until any later outward-sync pass is actually
   needed.

## Suggested Worktree Map

Use these if the next planning-only batch needs isolated write sets:

- `wip/p12-ledger` -> sibling worktree `../LLMCompute-wt-p12`
- `wip/r24-boundary-plan` -> sibling worktree `../LLMCompute-wt-r24`
- `wip/r25-systems-notes` -> sibling worktree `../LLMCompute-wt-r25`
- `wip/p13-hygiene` -> sibling worktree `../LLMCompute-wt-p13`

Suggested ownership:

- main agent: `main`
- worker A: `wt-r24`
- worker B: `wt-r25`
- background worker: `wt-p12` if any post-closeout paper sync still appears
- later downstream worker: `wt-p13`

## Acceptance For This Wave

- `H21` is the frozen handoff anchor for the current wave;
- `P12` is already closed out and preserved as the completed post-`H21`
  manuscript / manifest maintenance batch;
- `R24` exists as a planning-only boundary-first reopen package with explicit
  axes and stop rules;
- `R25` exists as a parked same-endpoint systems hypotheses package with
  explicit thresholds and disconfirmers;
- `P13` is recorded as downstream-only rather than immediate next priority;
- no widened runtime scope, frontend widening, or softened mixed-systems prose
  is introduced in this wave.

## If Blocked

- first continue `R24` and `R25` planning-only writeups rather than opening a
  new runtime lane early;
- then return to `P12` only if one later outward/publication doc exposes a real
  post-`H21` ledger mismatch;
- only after that, tighten the current split map and `P13` hygiene notes;
- do not start widened runtime, repair, or frontend experiments.
