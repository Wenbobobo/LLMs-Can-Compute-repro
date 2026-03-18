# Status

Still gated. Compiled demos themselves have not started, but the relevant
pre-demo mechanism work for the current `D0` slice is now in place.

Current blocker summary:
- the current tiny typed-bytecode slice is frozen at verifier/lowering/harness
  + memory-surface companion + stress/reference follow-up;
- the next blocker is no longer “implement the harness” or “add one more
  stress/reference check”; it is to freeze wording and value through
  `P3_paper_freeze_and_evidence_mapping` and `R2_systems_baseline_gate`;
- later demo work now requires an explicit `M7_frontend_candidate_decision`;
- no Wasm-like or arbitrary-C widening is justified by the current evidence.
