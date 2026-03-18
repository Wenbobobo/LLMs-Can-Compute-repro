# M6 Compiled Programs and Demos

Future milestone: restricted compiled-program path and optional presentation
material once the core execution substrate is better closed.

Current stance:

- the first frontend boundary now lives in `docs/milestones/M6_frontend_spec/`
  and is fixed to a tiny typed bytecode;
- the first typed-bytecode harness now has a frozen verifier / lowering /
  differential-testing contract in `docs/milestones/M6_typed_bytecode_harness/`;
- the memory-surface follow-up in `docs/milestones/M6_memory_surface_followup/`
  is treated as a diagnostic layer on the same `D0` claim row, not a new
  frontend claim;
- the current `D0` slice is now effectively frozen at typed-bytecode harness +
  memory-surface companion + stress/reference follow-up;
- the next gating stages now live in
  `docs/milestones/P3_paper_freeze_and_evidence_mapping/`,
  `docs/milestones/R2_systems_baseline_gate/`, and
  `docs/milestones/M7_frontend_candidate_decision/`;
- no compiled demo work should outrun the tiny-bytecode harness, the paper
  evidence bundle, or the system/baseline gate;
- flashy demos remain secondary to compiler/runtime boundary clarity.
