# `E1a_precision_patch` Playbook

Status: dormant protocol. This file does not activate `E1a`.

## Purpose

Use this lane only to repair one precision-specific evidence conflict inside
the current bounded paper scope. The target is the existing `C3d` / `C3e`
story: partial positive results on the validated suites with an explicit
boundary against broad long-horizon robustness claims.

## Eligible triggers

`E1a` may open only when at least one valid reopen trigger already exists and
the missing evidence class is specifically about bounded precision. Typical
examples are:

- a locked sentence or caption overstates what `C3d` or `C3e` supports;
- a review/release requirement asks for one bounded precision artifact that is
  still missing on the current trace families;
- a required appendix companion for a precision statement is absent or no
  longer matches the frozen manuscript wording.

If the issue can be solved by tightening wording without new evidence, do not
open `E1a`.

## Scope lock

`E1a` is allowed to touch only the bounded precision story:

- primary rows: `C3d` and `C3e`;
- frozen context reused as read-only background: `A1`, `B1`, and the current
  paper bundle;
- out of scope: systems competitiveness, frontend widening, arbitrary C,
  general robustness, or any attempt to relabel the current partial positives
  as universal positives.

## Minimum starting bundle

Start from the current precision package before proposing any new run:

- `results/M4_precision_scaling_real_traces/horizon_base_sweep.json`
- `results/M4_precision_generalization/screening.json`
- `results/M4_precision_generalization/boundary_sweep.json`
- `results/M4_precision_organic_traces/claim_impact.json`
- `results/R1_precision_mechanism_closure/summary.json`

Only after the trigger is written down should the lane define the smallest new
artifact needed to answer the exact conflict.

## Allowed patch shapes

`E1a` may use one of the following bounded repair shapes:

1. one additional horizon/base sweep on the already validated trace families;
2. one appendix-level companion export on the current organic/real-trace
   families when the manuscript already depends on that evidence class;
3. one regeneration pass for an existing current-scope precision artifact when
   the conflict came from drift, corruption, or an incomplete export.

The lane should prefer the earliest option in that list that resolves the
conflict.

## Execution protocol

1. Quote the triggering manuscript/release/review conflict verbatim in the lane
   notes.
2. Name the affected row (`C3d`, `C3e`, or both) and the exact sentence/table
   that depends on it.
3. Freeze the evaluation surface to the current trace families and the smallest
   missing precision dimension.
4. Produce only the minimal new artifact bundle required to answer the named
   conflict.
5. Re-state the claim in bounded form: current-suite positive where supported,
   current-suite boundary where unsupported.
6. Record a result digest and return to the locked paper/release lanes.

## Required boundary checks

Before refreezing, `E1a` must confirm all of the following:

- no new wording claims universal base/horizon robustness;
- no unseen trace family is promoted into the paper without a separate scope
  decision;
- the existing negative or caveated precision boundary remains explicit if the
  new artifact does not overturn it on the current suite;
- the systems gate and `D0` boundary remain unchanged.

## Failure handling

If the bounded repair does not resolve the conflict, the lane must tighten the
paper wording back to the currently supported boundary rather than widening the
precision claim or activating another `E1` lane by default.

## Refreeze rule

`E1a` ends only after a lane-local result digest is recorded, the relevant
audits are rerun, and control returns to the locked paper/release surface on
the same bounded precision story.
