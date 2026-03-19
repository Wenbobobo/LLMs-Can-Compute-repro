# Manuscript Section Map

This map follows the fixed main-text sequence in
`docs/publication_record/main_text_order.md` and records which sections own
which claim-bearing artifacts.

| Section | Purpose | Primary artifacts | Placement |
| --- | --- | --- | --- |
| Abstract | State the narrow reproduction target, the surviving mechanism result, the mixed systems gate, and the explicit no-go boundary. | `results/P3_paper_freeze_and_evidence_mapping/summary.json`, `results/R1_precision_mechanism_closure/summary.json`, `results/R2_systems_baseline_gate/summary.json`, `results/M7_frontend_candidate_decision/decision_summary.json` | main text |
| Introduction | Explain why the source field note was directionally interesting but rhetorically too broad, and define the paper's narrower claim ladder. | `docs/publication_record/claim_ladder.md`, `results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json` | main text |
| Methods: trace substrate and retrieval | Define append-only traces, exact latest-write retrieval, and the reference execution setting. | `docs/claims_matrix.md`, `results/M2_geometry_core/benchmark_geometry.json`, `src/exec_trace/` | main text |
| Executor branches | Summarize exact, induced, opcode-conditioned, and staged-neural branches, emphasizing which ones are positive, caveated, or negative. | `results/M4_staged_pointer_decoder/summary.json`, `results/M4_mask_dependence_executor_gap/summary.json`, `results/M4_failure_provenance/summary.json`, `results/M5_pointer_baseline/training_run.json` | main text |
| Precision boundary | State where single-head fails, where decomposition helps, and what remains unsupported. | `results/R1_precision_mechanism_closure/summary.json`, `results/P1_paper_readiness/m4_real_trace_boundary_figure.svg` | main text |
| Systems gate | Separate mechanism-level asymptotic value from current-scope end-to-end system value. | `results/R2_systems_baseline_gate/summary.json`, `results/R2_systems_baseline_gate/baseline_matrix.json` | main text |
| Compiled boundary | Explain why the first compiled step is the tiny typed-bytecode `D0` boundary and why widening was explicitly rejected. In the frozen order, the frontend boundary diagram precedes the exact-trace / final-state table. | `results/P1_paper_readiness/m6_frontend_boundary_diagram.svg`, `results/P1_paper_readiness/exact_trace_final_state_table.md`, `results/M7_frontend_candidate_decision/decision_summary.json` | main text |
| Negative results and threats | Consolidate unsupported claims, failed baselines, mask-dependence closure, and mixed systems limits. | `docs/publication_record/negative_results.md`, `docs/publication_record/threats_to_validity.md`, `results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json` | main text |
| Reproducibility appendix | Collect regeneration commands, figure/table source paths, memory-surface diagnostics, and artifact ledgers. | `docs/publication_record/experiment_manifest.md`, `docs/milestones/P2_public_research_packaging/artifact_release_ledger.md`, `results/P1_paper_readiness/`, `results/M6_memory_surface_followup/summary.json` | appendix |
