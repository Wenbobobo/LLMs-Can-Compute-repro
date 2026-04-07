# `E1b_systems_patch` Playbook

Status: dormant protocol. This file does not activate `E1b`.

## Purpose

Use this lane only to answer one systems-specific evidence conflict on the
preserved same-endpoint scope. The target is the preserved mixed `R2` systems
gate: geometry asymptotics are positive, but the lowered same-scope execution
path is not yet end-to-end competitive on the preserved positive `D0` suites
from that earlier line.

## Eligible triggers

`E1b` may open only when at least one valid reopen trigger already exists and
the missing evidence class is specifically about the current systems gate. The
lane is appropriate when:

- a locked sentence or release summary promises a systems conclusion that the
  current `R2` artifacts do not actually support;
- a review or release requirement demands one stronger systems artifact on the
  preserved `D0` scope from that stage and cannot be satisfied by wording
  cleanup alone;
- a current manuscript-to-artifact pairing for the systems gate is missing or
  inconsistent.

If the conflict is really about compiled correctness rather than systems
competitiveness, use `E1c` instead.

## Scope lock

`E1b` is allowed to reason only about the preserved mixed systems gate:

- primary scope: preserved `R2` and its role in blocking automatic frontend
  widening;
- dependent read-only context: the preserved `D0` suites from that earlier
  line and the `M7` no-widening decision;
- out of scope: new frontends, arbitrary C, new language/runtime coverage,
  demo-first narratives, or any shortcut from geometry asymptotics to broad
  end-to-end superiority.

## Minimum starting bundle

Start from the current systems evidence before proposing any new run:

- `results/M2_geometry_core/benchmark_geometry.json`
- `results/R2_systems_baseline_gate/summary.json`
- `results/R2_systems_baseline_gate/baseline_matrix.json`
- `results/R2_systems_baseline_gate/runtime_profile_rows.csv`
- `results/M6_typed_bytecode_harness/short_exact_trace.json`
- `results/M6_typed_bytecode_harness/long_exact_final_state.json`
- `results/M6_stress_reference_followup/summary.json`
- `results/M7_frontend_candidate_decision/decision_summary.json`

Only after the trigger is named should the lane define the smallest new
systems artifact needed to answer it.

## Allowed patch shapes

`E1b` may use one of the following bounded repair shapes:

1. one rerun of the preserved same-scope runtime profile bundle on the already
   positive `D0` suites from that earlier line;
2. one missing cost-attribution slice across the existing interpreter/lowered/
   spec paths when that exact comparison is what the locked text depends on;
3. one repaired systems export when the existing gate artifact drifted or no
   longer matches the frozen wording.

The lane must keep the comparison surface identical to the preserved
same-endpoint scope unless an explicit new scope decision is recorded
elsewhere.

## Execution protocol

1. Quote the triggering systems conflict and the exact sentence/table/review
   request that depends on it.
2. State the gate question in yes/no form on the preserved same-endpoint
   scope, for example whether the lowered path is competitive enough to
   justify a narrower wording change.
3. Freeze the comparison surface to the preserved positive `D0` suites from
   that earlier line and the existing geometry/interpreter/lowered/spec paths.
4. Produce only the smallest new systems artifact bundle required to answer the
   gate question.
5. Update the wording in bounded form: either the gate remains mixed, or one
   current-scope statement becomes better supported without authorizing
   widening.
6. Record a result digest and return to the locked paper/release lanes.

## Required boundary checks

Before refreezing, `E1b` must confirm all of the following:

- geometry asymptotic advantage and end-to-end competitiveness are still kept
  separate conceptually;
- no current-scope systems result is rewritten into a broad superiority claim;
- frontend widening remains blocked unless a separate explicit scope decision
  and claim/evidence remap are opened later;
- the precision story and `D0` correctness bundle remain unchanged except where
  they are merely cited as inputs.

## Failure handling

If the bounded repair does not resolve the conflict, the lane must preserve or
tighten the mixed-gate wording rather than opening a broader systems campaign
or silently widening the frontend.

## Refreeze rule

`E1b` ends only after a lane-local result digest is recorded, the relevant
audits are rerun, and control returns to the locked paper/release surface with
the systems gate still expressed on the same bounded scope.
