# E1 Conditional Evidence Reopen Protocol Design

## Context

The repo now has a frozen scope plus a freeze-candidate checkpoint. The missing
piece is an explicit protocol for what counts as a legitimate reopen, so later
automation does not silently drift back into open-ended experimentation.

## Goal

Define the only allowed path for reopening precision, systems, or compiled
boundary evidence after `P7`.

## Required Outputs

- one milestone scaffold under
  `docs/milestones/E1_conditional_evidence_reopen_protocol/`;
- one publication-facing protocol document naming valid triggers, patch lanes,
  and refreeze requirements;
- one dormant handoff that later agents can follow without reconstructing
  intent.

## Acceptance

- any future reopen must name a trigger and one bounded patch lane;
- no reopen can occur by wording drift alone;
- every reopen ends by returning control to the locked paper/release lanes.
