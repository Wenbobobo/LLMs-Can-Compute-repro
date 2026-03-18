# Claim Ladder

| Claim layer | Current status | Best evidence | Next evidence target |
| --- | --- | --- | --- |
| A1 Append-only trace substrate | validated on current toy programs | `docs/claims_matrix.md`, `results/` existing M2/M3/M4 artifacts | maintain under future frontends |
| B1 Exact 2D hard-max retrieval | validated on current geometry core | `results/M2_geometry_core/benchmark_geometry.json`, current M2 artifacts | preserve as baseline |
| C2f Staged pointer bridge | partial positive with caveat | `results/M4_staged_pointer_decoder/summary.json` | `results/M4_mask_dependence_executor_gap/` |
| C2g Pointer-space softmax negative control | validated negative control | `results/M5_pointer_baseline/training_run.json` | freeze unless label space changes |
| C2h Staged mask-dependence closure | negative closure with provenance separation | `results/M4_mask_dependence_executor_gap/summary.json`, `results/M4_failure_provenance/summary.json` | maintain wording discipline only |
| C3d Real-trace horizon/base precision | partial positive on current suite | `results/M4_precision_scaling_real_traces/horizon_base_sweep.json` | `results/M4_precision_organic_traces/` |
| C3e Broader real-trace precision taxonomy | partial positive with sharper boundary and dedicated organic bundle | `results/M4_precision_generalization/screening.json`, `results/M4_precision_organic_traces/claim_impact.json`, `results/R1_precision_mechanism_closure/summary.json` | maintain wording discipline; no broader robustness claim beyond the current suite |
| D0 First compiled frontend boundary | current tiny typed bytecode remains the compiled endpoint; the frozen slice is implemented, survives one stress/reference follow-up with a standalone spec oracle and synced companion memory-surface diagnostics, and is explicitly not widened by `M7` | `results/M6_typed_bytecode_harness/verifier_rows.json`, `results/M6_typed_bytecode_harness/short_exact_trace.json`, `results/M6_typed_bytecode_harness/long_exact_final_state.json`, `results/M6_memory_surface_followup/summary.json`, `results/M6_stress_reference_followup/summary.json`, `results/M7_frontend_candidate_decision/decision_summary.json` | maintain current endpoint; any reopening now requires a stronger systems pass plus an explicit new scope decision |
