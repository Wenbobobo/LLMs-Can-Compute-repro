# Claim Evidence Table

## Current evidence

- `C2e` — `results/M4_factorized_event_decoder/summary.json`
  Direct factorized event-value decoder: nontrivial teacher-forced accuracy,
  weak free-running rollout.
- `C2f` — `results/M4_staged_pointer_decoder/summary.json`
  Staged pointer decoder with structural, `opcode_shape`, and `opcode_legal`
  rollout on the harder held-out slice including `alternating_memory_loop`.
- `C2g` — `results/M5_pointer_baseline/training_run.json`
  Pointer-space softmax baseline: structural and `opcode_shape` remain the
  valid comparison regimes; `opcode_legal` stays diagnostic only.
- `C2h` — `results/M4_mask_dependence_executor_gap/summary.json`
  Expanded staged-mask batch: held-out `opcode_shape` collapses on the broader
  suite, while `opcode_legal` remains exact; cleaned failures split between
  `push_expr_0` trace mismatches and `step_budget` nontermination, so no
  fourth regime is justified.
- `C2h` — `results/M4_failure_provenance/summary.json`
  Provenance follow-up: the earlier held-out `opcode_shape` `step_budget` rows
  are downstream nontermination after first semantic divergence, not a third
  root-cause family beside `push_expr_0`.
- `C3c` — `results/M4_precision_scaling_real_traces/summary.json`
  Real offset traces reproduce the single-head precision failure mode.
- `C3d` — `results/M4_precision_scaling_real_traces/horizon_base_sweep.json`
  Horizon/base sweep over loop, ping-pong, and alternating offset streams.
- `C3e` — `results/M4_precision_generalization/screening.json`
  Broader real-trace suite: new high-address memory families fail at `1x`,
  while stack depth remains easier at `64` and begins to fail by `256`.
- `C3e` — `results/M4_precision_generalization/boundary_sweep.json`
  Boundary sweep: decomposition remains strong on the new memory families,
  while the deeper exported stack stream tightens the stable-base story.
- `C3e` — `results/M4_precision_organic_traces/claim_impact.json`
  Dedicated organic-trace bundle: same broadened evidence is now indexed under
  one explicit claim-impact artifact for later paper/README use.
- `C3e` — `results/R1_precision_mechanism_closure/summary.json`
  Unified precision closure: single-head failures are common on the tracked
  suite, decomposition stays useful on current validated rows, and broader
  robustness claims remain blocked.
- `D0` — `results/M6_typed_bytecode_harness/verifier_rows.json`
  Current tiny-bytecode verifier batch: twenty-two valid programs pass, and
  seven negative controls fail deterministically with first-error reports.
- `D0` — `results/M6_typed_bytecode_harness/short_exact_trace.json`
  Current exact-trace harness batch: sixteen short/medium programs, including
  the control-flow-first `call` / `ret` rows, match the lowered `exec_trace`
  path exactly.
- `D0` — `results/M6_typed_bytecode_harness/long_exact_final_state.json`
  Current long-row harness batch: six longer programs also match exactly
  through final state.
- `D0` — `results/M6_memory_surface_followup/summary.json`
  Diagnostic memory-surface follow-up: the same call/ret bytecode slice now
  has six annotated rows and two deterministic negative controls, with
  reference-vs-lowered surface views still matching exactly.
- `D0` — `results/M6_stress_reference_followup/summary.json`
  Stress/reference follow-up: one branch-selected helper checkpoint braid
  family now adds two medium exact-trace positives, one long exact-final-state
  positive, and two matched negatives under a standalone Python spec
  interpreter, while all three positive rows preserve companion
  memory-surface agreement.
- `D0` — `results/M7_frontend_candidate_decision/decision_summary.json`
  Frontend decision bundle: the current endpoint stays on tiny typed bytecode,
  frontend widening is not authorized, and any revisit now requires a fresh
  scope + systems case.

## Planned next evidence targets

No mandatory new evidence target is open on the current paper scope.

Any future reopening of `D0` now requires a successor to the `M7` no-widening
decision plus a stronger systems pass than the current `R2` result.
