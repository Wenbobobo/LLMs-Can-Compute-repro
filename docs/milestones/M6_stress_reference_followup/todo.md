# Todo

- [x] Freeze the stress-family selection criteria before inventing concrete
  programs.
- [x] Choose one stress family that combines loop, branch, helper call, and
  frame/heap interaction without adding new runtime features.
- [x] Define the minimum positive and negative suite size for that family.
- [x] Choose the external-reference strategy.
- [x] Define the comparison schema across:
  verifier,
  current bytecode interpreter,
  lowered `exec_trace` path,
  external reference path.
- [x] Write the stop/go rule for broader compiled demos after this follow-up.
- [x] Implement the standalone Python spec interpreter without lowering reuse.
- [x] Implement the branch-selected helper checkpoint braid suite.
- [x] Export the dedicated `M6-E` result bundle under
  `results/M6_stress_reference_followup/`.
- [x] Sync `P1` / `P2` ledgers so the new bundle is tracked as `D0` evidence,
  not as a new claim layer.
