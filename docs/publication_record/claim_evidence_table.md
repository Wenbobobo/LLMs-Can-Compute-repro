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
  one explicit claim-impact artifact for paper/README use.
- `C3e` — `results/R1_precision_mechanism_closure/summary.json`
  Unified precision closure: single-head failures are common on the tracked
  suite, decomposition stays useful on current validated rows, and broader
  robustness claims remain blocked.
- `C3d/C3e` — `results/E1a_precision_patch/summary.json`
  Patch-level precision bundle: the denser `1/2/4/8/16/32/64` horizon grid
  stays on the same 25-stream / 7-family tracked suite, with `12/25`
  single-head failure streams, `7/25` already failing at `1x`, and `194`
  fully passing decomposition configs.
- `C3d/C3e` — `results/E1a_precision_patch/first_failure_rows.csv`
  Stream-level companion rows for the bounded patch: first-failure
  multipliers, full-horizon survivors, and control-vs-active scheme outcomes
  now live in one compact machine-readable table.
- `C3d/C3e` — `results/E1a_precision_patch/family_boundary_rows.csv`
  Family-level companion rows for the bounded patch: earliest failures,
  fail-at-`1x` counts, and decomposition coverage are summarized per family.
- `C3d/C3e` — `results/E1a_precision_patch/negative_control_rows.json`
  Weaker coarse-bucket control rows: the diagnostic control fails broadly on
  the same tracked suite, so it sharpens the mechanism story but is not a
  positive alternative.
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
- `R2` — `results/E1b_systems_patch/summary.json`
  Patch-level systems bundle: the mixed gate is restated with same-scope
  component attribution, `25` component rows, `5` suite bridges, `4` history
  bridges, and lowered execution still about `1.824x` slower than the best
  current reference path, while frontend widening remains blocked.
- `R2` — `results/E1b_systems_patch/component_cost_rows.csv`
  Program-level attribution companion: the current runtime gap is decomposed
  across verification, bytecode, lowered, and spec paths on the existing
  positive `D0` suites.
- `R2` — `results/E1b_systems_patch/suite_bridge_rows.csv`
  Suite-level bridge companion: the current mixed gate is broken out by suite
  rather than left as one median-only statement.
- `R2` — `results/E1b_systems_patch/history_bridge_rows.csv`
  History bridge companion: asymptotic geometry wins are tied back to current
  `D0` step counts without treating beyond-scope histories as end-to-end
  runtime evidence.

## Active bounded patch state

- `H4` sets the active phase to `h4_reproduction_mainline_return_active`, with
  lane order `e1a_then_e1b_then_optional_e1c_then_h5`.
- `E1a` is active only for bounded `C3d/C3e` sharpening on the current
  validated suites.
- `E1b` is active only for same-scope systems attribution on the current
  positive `D0` suites.
- `E1c` remains inactive unless `E1a` or `E1b` exposes a concrete frozen-`D0`
  contradiction that wording alone cannot repair.
- `H3` / `P10` / `P11` / `F1` remain the completed baseline while the bounded
  return packet is active.
