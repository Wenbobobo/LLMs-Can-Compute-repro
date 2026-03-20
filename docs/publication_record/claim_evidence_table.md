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
- `D0` — `results/R3_d0_exact_execution_stress_gate/summary.json`
  Harder-suite exact-execution gate: seven additional bounded `D0` rows stay
  exact under bytecode, lowered `exec_trace`, and standalone spec agreement;
  linear versus accelerated Hull decode parity stays exact on all admitted
  lowered rows; four longer memory streams enter the immediate precision
  companion screen; and `E1c` remains inactive.
- `D0` — `results/R4_mechanistic_retrieval_closure/summary.json`
  Mechanistic retrieval closure: all `32` current positive `D0` programs are
  explainable using latest-write, stack, control, and deterministic
  local-transition primitives; `4290` source-event observations keep exact
  linear-versus-Hull parity; `R5` is not justified; and `E1c` remains
  inactive.
- `D0` — `results/H8_driver_replacement_guard/summary.json`
  Driver replacement guard: the repo control docs now treat `H8/R6/R7/H9` as
  the active packet while preserving `H6/R3/R4/(inactive R5)/H7` as the
  completed baseline on the same endpoint.
- `D0` — `results/R6_d0_long_horizon_scaling_gate/summary.json`
  Long-horizon scaling gate: current scalable `D0` families are pushed to fixed
  longer horizons without widening semantics; all `24` rows remain admitted,
  `8/8` longer-row decode-parity checks stay exact, growth reaches about
  `7.81x` over baseline seeds, and the narrow multiplier-`8` precision
  companion finds `4/8` boundary-bearing streams with the weaker control
  failing on `2/4` of them.
- `D0` — `results/R7_d0_same_endpoint_runtime_bridge/summary.json`
  Same-endpoint runtime bridge: the full `8`-family exact-admitted surface is
  preserved, but only the top `4` heaviest representatives are profiled and
  remain exact; accelerated Hull decode reaches only about `0.973x` of linear
  on median, remains about `1980.3x` slower per step than the lowered path,
  and therefore stops at
  `stop_decode_gain_not_material`.
- `D0` — `results/H10_r7_reconciliation_guard/summary.json`
  Reconciliation guard: the public and paper-facing ledgers now restate the
  completed `R7` stop result as a bounded top-`4` profile on the preserved
  `8`-family admitted surface.
- `D0` — `results/H11_post_h9_mainline_rollover_guard/summary.json`
  Mainline rollover guard: the repo control docs now treat
  `H10/H11/R8/R9/R10/H12` as the active packet while preserving
  `H8/R6/R7/H9` as the completed direct baseline.
- `D0` — `results/R8_d0_retrieval_pressure_gate/summary.json`
  Retrieval-pressure gate: the same fixed endpoint survives one bounded
  heavier-family pressure raise with `4/4` admitted exact rows, `2/2` bounded
  decode-parity probe matches, and no routed contradiction candidates.
- `D0` — `results/R9_d0_real_trace_precision_boundary_companion/summary.json`
  Precision companion: the admitted `R8` memory streams stay bounded and
  companion-only, with all `4/4` screened streams still `effective_here` and
  no weak negative-control failure.
- `D0` — `results/R10_d0_same_endpoint_cost_attribution/summary.json`
  Cost-attribution companion: representative admitted `R6/R8` rows keep the
  systems question narrow and show current exact runtime still dominated by
  retrieval cost rather than by harness or transition overhead.
- `D0` — `results/R11_geometry_fastpath_reaudit/summary.json`
  Geometry fast-path re-audit: the current exact `2D` parity slice stays exact
  on `5/5` audited cases and the preserved standalone cache-vs-bruteforce gain
  remains strong, but same-endpoint speedup wording stays blocked.
- `D0` — `results/R12_append_only_executor_long_horizon/summary.json`
  Append-only executor re-audit: current exported executor modes remain exact,
  heldout countdown still reaches `104` steps, the preserved harder `R3`
  baseline stays contradiction-free, and the next harder-slice inventory is
  explicit across staged `R6/R8` rows.
- `D0` — `results/H15_refreeze_and_decision_sync/summary.json`
  Refreeze-and-decision sync: the repo is now explicitly refrozen after the
  bounded reopen wave, with `R13` inactive, `R14` unjustified, and no new
  active science lane authorized without a later explicit plan.
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

## Current bounded mainline state

- `H4` completed the bounded reproduction return packet, and `E1a/E1b/H5`
  remain the immediate evidence baseline for current precision/systems wording.
- `H15` is the current refrozen stage after one bounded `H14/R11/R12` reopen
  packet on the same endpoint.
- `H14` completed one explicit core-first reopen without widening: `R11`
  re-audited exact geometry, `R12` re-audited append-only/latest-write
  executor closure, `R13` stayed inactive, and `R14` stayed unjustified.
- `H8/R6/R7/H9` remains the completed direct same-endpoint baseline for the
  current packet.
- `H6/R3/R4/(inactive R5)/H7` remains the deeper completed
  exactness/mechanism baseline underneath it.
- `H10` reconciles the prior packet to the artifact-backed `R7` top-`4`
  profile wording and records that correction machine-readably.
- `H11` moved the repo into the completed retrieval-pressure follow-up packet,
  which is now preserved rather than active.
- `R8` is the completed retrieval-pressure gate on the same fixed `D0`
  endpoint and now hands the packet forward to `R9` and `R10`.
- `R9` is the completed bounded precision companion lane and stays limited to
  admitted `R8` same-endpoint memory streams only.
- `R10` is the completed same-endpoint cost-attribution lane and remains
  narrower than a reopened systems packet.
- `H12` has now rerun the standing audits, synchronized the ledgers, and left
  the current packet refrozen on the same endpoint.
- `R11` is the completed exact-geometry re-audit lane and keeps the same-endpoint
  performance story explicitly negative.
- `R12` is the completed append-only executor re-audit lane and remains
  bounded to the current staged `R6/R8` families.
- `H15` has now synchronized the ledgers again and leaves the repo refrozen on
  the same endpoint with `R13` inactive and `R14` unjustified.
- `E1c` remains inactive unless the active packet exposes a concrete frozen-`D0`
  contradiction that wording alone cannot repair.
- `H3` / `P10` / `P11` / `F1` remain the documentation/archive baseline while
  `H4/E1a/E1b/H5` remain the completed bounded return baseline.
