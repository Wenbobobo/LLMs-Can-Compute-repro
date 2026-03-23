# `E1c_compiled_boundary_patch` Playbook

Status: dormant protocol. This file does not activate `E1c`.

## Purpose

Use this lane only to repair one evidence conflict around the preserved first
compiled boundary from the old same-endpoint line. The target is the existing
tiny typed-bytecode `D0` slice as preserved historical support inside the
broader current `H43` paper endpoint: verifier parity, lowering equivalence,
exact trace/final-state agreement, one stress/reference follow-up, and
companion memory-surface diagnostics, all without frontend widening.

## Eligible triggers

`E1c` may open only when at least one valid reopen trigger already exists and
the missing evidence class is specifically about the preserved first `D0`
compiled boundary. The lane is appropriate when:

- a locked `D0` sentence or table points to missing or inconsistent compiled
  evidence;
- a required appendix companion for the preserved-first-step `D0` narrative is
  absent or no longer matches the locked paper wording;
- verifier, lowering, exactness, or companion artifacts disagree on the frozen
  typed-bytecode slice and the conflict cannot be solved by wording cleanup
  alone.

If the issue is primarily about systems competitiveness, use `E1b` instead.

## Scope lock

`E1c` is allowed to touch only the preserved first `D0` boundary:

- primary scope: the existing tiny typed-bytecode slice and its preserved
  companion diagnostics;
- dependent read-only context: the `R2` mixed systems gate and the `M7`
  no-widening decision;
- out of scope: new opcode classes, broader bytecode semantics, broader
  frontend/runtime demos, arbitrary C, or any claim that collapses `D0` into a
  general compiler/runtime story.

## Minimum starting bundle

Start from the preserved compiled-boundary package before proposing any new
run:

- `results/M6_typed_bytecode_harness/verifier_rows.json`
- `results/M6_typed_bytecode_harness/lowering_equivalence.json`
- `results/M6_typed_bytecode_harness/short_exact_trace.json`
- `results/M6_typed_bytecode_harness/long_exact_final_state.json`
- `results/M6_memory_surface_followup/summary.json`
- `results/M6_stress_reference_followup/summary.json`
- `results/M7_frontend_candidate_decision/decision_summary.json`
- `results/R2_systems_baseline_gate/summary.json`

Only after the trigger is named should the lane define the smallest new
compiled-boundary artifact needed to answer it.

## Allowed patch shapes

`E1c` may use one of the following bounded repair shapes:

1. one repaired verifier/lowering/exactness export on the frozen `D0` starter
   suite;
2. one companion diagnostic export for the existing memory-surface or
   stress/reference layer when the manuscript already depends on that evidence
   class;
3. one repaired cross-check against the current standalone oracle/reference
   path when the conflict is about agreement, not about widening semantics.

The lane must keep the semantic surface fixed to the current typed-bytecode
slice throughout.

## Execution protocol

1. Quote the triggering compiled-boundary conflict and the exact locked
   sentence/table/appendix pairing it affects.
2. Name the precise `D0` evidence class at issue: verifier, lowering, exact
   trace, exact final state, memory-surface companion, or stress/reference
   companion.
3. Freeze the suite and semantics to the preserved `D0` slice before any
   repair work starts.
4. Produce only the smallest new compiled-boundary artifact bundle required to
   answer the named conflict.
5. Re-state the boundary in narrow form: preserved first-step `D0` supported
   where proven, no broader frontend implication.
6. Record a result digest and return to the locked paper/release lanes.

## Required boundary checks

Before refreezing, `E1c` must confirm all of the following:

- the repaired artifact still describes the same frozen `D0` semantics;
- no new compiled feature is introduced merely to rescue wording;
- any systems interpretation remains gated by `R2` and the existing `M7`
  no-widening decision;
- arbitrary C, wider bytecode coverage, and broader frontend demos remain
  explicitly blocked.

## Failure handling

If the bounded repair does not resolve the conflict, the lane must tighten the
paper wording back to the preserved first `D0` boundary rather than widening
the frontend or assuming that a stronger systems pass authorizes a broader
claim.

## Refreeze rule

`E1c` ends only after a lane-local result digest is recorded, the relevant
audits are rerun, and control returns to the locked paper/release surface with
the same preserved tiny typed-bytecode boundary still in force as historical
support.
