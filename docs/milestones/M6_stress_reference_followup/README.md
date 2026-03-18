# M6 Stress and Reference Follow-up

Goal: add exactly one serious stress family and exactly one external reference
comparison without widening beyond the current tiny typed-bytecode surface.

Scope:

- keep the current type system (`i32`, `addr`, `flag`) and frozen opcode set;
- keep static-target non-recursive control flow;
- allow longer, denser interactions among loop, branch, helper call, frame, and
  heap touches;
- add a third oracle path that does not depend on the lowering pipeline.

Deliverables:

- one stress-family spec with deterministic positive/negative cases;
- one external-reference strategy and acceptance rule;
- a stop/go decision about whether broader compiled demos remain blocked.

Chosen planning defaults:

- stress family: branch-selected helper checkpoint braid;
- external reference: standalone Python spec interpreter with no lowering reuse;
- minimum suite shape:
  `3` positives (`2` medium exact-trace rows covering distinct helper/checkpoint
  paths, `1` long exact-final-state row),
  plus `2` matched negatives (`1` control-flow/typed-branch contract
  violation, `1` memory-surface contract violation).

Current implementation status:

- implemented under `src/bytecode/spec_oracle.py`,
  `src/bytecode/stress_reference.py`,
  and `scripts/export_m6_stress_reference_followup.py`;
- exported under `results/M6_stress_reference_followup/`;
- broader compiled demos remain blocked until the next planning cycle decides
  whether any frontend widening is justified at all.
