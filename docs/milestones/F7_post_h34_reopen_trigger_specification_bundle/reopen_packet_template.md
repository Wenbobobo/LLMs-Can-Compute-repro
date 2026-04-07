# Reopen Packet Template

This template is for a future explicit contradiction packet only. Filling it
out in planning prose does not authorize execution by itself.

## Header

- packet kind: `same_substrate_contradiction_packet`
- current routing packet: `H32_post_r38_compiled_boundary_refreeze`
- current docs-only control packet:
  `H34_post_r39_later_explicit_scope_decision_packet`
- current saved reopen state: `no active downstream runtime lane`

## Required fields

1. Named contradiction
   - one concrete contradiction, failure mode, or sharper unresolved
     dependency;
   - tied directly to the current admitted row and/or named same-family
     boundary probe;
   - no broader family drift.
2. Comparator set
   - one predeclared same-substrate comparator set;
   - fixed before execution;
   - no hidden host evaluator and no opcode-surface widening.
3. Measurement rule
   - one exact success/failure criterion;
   - one explicit artifact list to compare;
   - one statement of what result would count as "still no reopen case."
4. Stop condition
   - one explicit stop rule preventing open-ended repair or exploratory drift.
5. Scope statement
   - explicit statement that the packet does not by itself authorize scope
     lift, arbitrary `C`, Wasm-like widening, or headline expansion.

## Required non-fields

The following must not appear as sufficient justification:

- "the headline still feels overstated";
- "we should probably test one more runtime batch";
- "we need broader demos";
- "the old same-endpoint systems route was unsatisfying";
- "maybe this leads to `H35`."

## Exit rule

If any required field is missing, the correct outcome is:

- do not create a runtime batch;
- do not infer an `H35`;
- preserve `no_reopen_candidate_survives` as the current saved interpretation.
