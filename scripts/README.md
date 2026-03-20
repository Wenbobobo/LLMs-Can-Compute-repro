# Scripts

- `benchmark_geometry.py` — compare brute-force hard-max lookup with
  `HullKVCache`
- `export_runtime_environment.py` — record the current Python/Torch/CUDA runtime
- `export_m4_free_running.py` — export the exact free-running executor artifact
- `export_m4_induced_causal.py` — export the induced structured transition
  executor artifact
- `export_m4_factorized_event_decoder.py` — export the richer direct
  event-value decoder artifact
- `export_m4_precision_stress.py` — export finite-precision addressing sweeps
- `export_m4_real_trace_precision.py` — export finite-precision checks over
  real trace streams
- `export_m5_dataset_preview.py` — export the softmax-baseline dataset preview
- `export_m5_training_run.py` — train and export the first runnable softmax
  baseline checkpoint
- `export_m5_event_level_baseline.py` — train and export the final event-level
  standard softmax baseline
- `export_p3_paper_freeze.py` — export the paper-freeze claim/artifact map
- `export_h0_release_hygiene.py` — export the current release-hygiene audit
  and preferred commit split
- `export_m7_frontend_candidate_decision.py` — export the post-`P3/R1/R2`
  frontend no-go / candidate decision bundle
- `export_p4_blog_release_gate.py` — export the outward blog/README release
  gate and public-claim audit
- `export_p5_public_surface_sync.py` — export the current `P5` public-surface
  sync audit for README / STATUS / release-summary / manuscript alignment
- `export_p5_callout_alignment.py` — export the current `P5` manuscript
  callout/caption alignment audit for main-text artifact pairs
- `export_release_preflight_checklist_audit.py` — export the machine-readable
  outward release-preflight audit for release-facing docs, frozen paper-facing
  ledgers, and standing result summaries
- `export_release_worktree_hygiene_snapshot.py` — export the current git
  worktree cleanliness snapshot for release-facing commit decisions
- `export_h14_core_first_reopen_guard.py` — export the single-file active-stage
  guard for the current `H14` core-first reopen plan, preserved handoff, and
  standing guard chain
- `export_h13_post_h12_governance_stage_health.py` — export the preserved
  governance/runtime handoff summary for the `H13/V1` stack underneath active
  `H14`
- `export_r1_precision_mechanism_closure.py` — export the unified precision
  boundary closure bundle
- `export_r2_systems_baseline_gate.py` — profile the current systems gate and
  emit a stop/go baseline bundle
- `export_h6_mainline_rollover_guard.py` — audit whether the repo control docs
  preserve the completed `H6/R3/R4/(inactive R5)/H7` packet as the deeper
  baseline under the current packet
- `export_h8_driver_replacement_guard.py` — audit whether the repo control docs
  preserve the completed `H8/R6/R7/H9` packet as the direct baseline under the
  current packet
- `export_h10_r7_reconciliation_guard.py` — audit whether `R7` wording is
  reconciled to the artifact-backed top-`4` profile result
- `export_h11_post_h9_mainline_rollover_guard.py` — audit whether the repo
  control docs match the bounded `H10/H11/R8/R9/R10/H12` packet
- `export_r3_d0_exact_execution_stress_gate.py` — export the bounded harder
  `D0` exact-execution gate with explicit linear-vs-Hull parity and the narrow
  precision companion screen
- `export_r4_mechanistic_retrieval_closure.py` — export the bounded
  source-event mechanistic-closure bundle on the current positive `D0` suites
- `export_r6_d0_long_horizon_scaling_gate.py` — export the fixed-multiplier
  long-horizon exactness gate on current scalable `D0` families
- `export_r7_d0_same_endpoint_runtime_bridge.py` — export the same-endpoint
  runtime bridge on the full exact-admitted `R6` family set
- `export_r8_d0_retrieval_pressure_gate.py` — export the bounded heavier-family
  same-endpoint retrieval-pressure gate on the preserved direct baseline
- `export_r9_d0_real_trace_precision_boundary_companion.py` — export the
  bounded real-trace precision companion on exact-admitted `R8` memory streams
- `export_r10_d0_same_endpoint_cost_attribution.py` — export the bounded
  representative-row same-endpoint cost attribution companion
- `export_r11_geometry_fastpath_reaudit.py` — export the reopened exact-geometry
  parity / benchmark / wording gate audit on the current codebase
- `export_r12_append_only_executor_long_horizon.py` — export the reopened
  append-only executor long-horizon baseline, harder-slice inventory, and
  bounded failure taxonomy contract
- `export_h15_refreeze_and_decision_sync.py` — export the machine-readable
  direct-refreeze completion decision after the `R11/R12` reopen outputs
- `export_v1_full_suite_validation_runtime_audit.py` — export the bounded
  collect-only inventory and heavy-file shortlist for the full-suite
  validation-runtime gate
- `export_v1_full_suite_validation_runtime_timing_followup.py` — export the
  bounded per-file timing follow-up that classifies the current full-suite
  validation-runtime gate
- `setup_unattended_worktrees.ps1` — create the default unattended worktree
  layout after the tree is clean enough to branch
