# `E1` Patch Playbook Matrix

This matrix is a dormant downstream aid for future evidence maintenance. No
`E1` lane is active on the current repo state.

## Shared activation rules

Every future `E1` lane must satisfy all of the following before any evidence
work starts:

- a valid trigger from `docs/publication_record/conditional_reopen_protocol.md`
  is recorded explicitly;
- exactly one lane is active at a time;
- the triggering conflict, affected claim row, and smallest artifact bundle are
  named in advance;
- the lane ends by refreezing through the locked paper/release surface rather
  than opening a new broad research phase.

## Lane matrix

| Lane | Use only when | Primary frozen scope | Minimum starting bundle | Hard limits | Stop condition |
| --- | --- | --- | --- | --- | --- |
| `E1a_precision_patch` | one locked sentence, table, or review/release requirement demands one missing precision evidence class that cannot be resolved by wording alone | bounded precision rows `C3d` and `C3e` on the current validated trace families | `results/M4_precision_scaling_real_traces/horizon_base_sweep.json`, `results/M4_precision_generalization/screening.json`, `results/M4_precision_generalization/boundary_sweep.json`, `results/M4_precision_organic_traces/claim_impact.json`, `results/R1_precision_mechanism_closure/summary.json` | no new trace-family program, no universal robustness claim, no systems or compiled widening | the precision conflict is answered on the current suite, or the locked wording is tightened back to the existing boundary |
| `E1b_systems_patch` | one locked sentence or review/release demand requires one missing systems evidence class on the current scope | the mixed `R2` systems gate and its role as a prerequisite for any later frontend revisit | `results/M2_geometry_core/benchmark_geometry.json`, `results/R2_systems_baseline_gate/summary.json`, `results/R2_systems_baseline_gate/baseline_matrix.json`, `results/R2_systems_baseline_gate/runtime_profile_rows.csv`, `results/M6_typed_bytecode_harness/short_exact_trace.json`, `results/M6_typed_bytecode_harness/long_exact_final_state.json`, `results/M6_stress_reference_followup/summary.json`, `results/M7_frontend_candidate_decision/decision_summary.json` | no frontend widening, no arbitrary-C/runtime-generalization claim, no end-to-end superiority shortcut | the named systems question is answered on the current positive `D0` suites, while the gate remains explicitly bounded to current scope |
| `E1c_compiled_boundary_patch` | one locked `D0` sentence, artifact pairing, or appendix companion is missing or contradicted and cannot be repaired by wording alone | the tiny typed-bytecode `D0` boundary only | `results/M6_typed_bytecode_harness/verifier_rows.json`, `results/M6_typed_bytecode_harness/lowering_equivalence.json`, `results/M6_typed_bytecode_harness/short_exact_trace.json`, `results/M6_typed_bytecode_harness/long_exact_final_state.json`, `results/M6_memory_surface_followup/summary.json`, `results/M6_stress_reference_followup/summary.json`, `results/M7_frontend_candidate_decision/decision_summary.json`, `results/R2_systems_baseline_gate/summary.json` | no new frontend surface, no opcode/language widening beyond current `D0`, no arbitrary C | the `D0` conflict is closed on the frozen typed-bytecode slice, or the locked wording is tightened back to the present boundary |

## Cross-lane non-rules

- wording drift by itself is not enough to activate any lane;
- curiosity-driven strengthening is not enough to activate any lane;
- a positive result in one lane does not auto-activate another lane;
- no lane may silently convert bounded precision, the mixed systems gate, or
  the tiny `D0` boundary into a broader “LLMs are computers” claim.

## Refreeze output

Any future activated lane must produce a lane-local result digest, rerun the
relevant standing audits, and return control to the same locked paper/release
surface unless a separate deliberate scope decision says otherwise.
