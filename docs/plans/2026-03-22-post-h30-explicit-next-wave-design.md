# 2026-03-22 Post-H30 Explicit Next-Wave Design

## Summary

`H30_post_r36_r37_scope_decision_packet` closes the current Origin-core wave in
a scientifically useful but still narrow state:

1. append-only traces remain exact on the active substrate;
2. exact `2D` hard-max retrieval remains exact on the active primitive suite;
3. the small append-only stack/VM executor remains exact on the current bundle;
4. one tiny admitted lowered/compiled bytecode subset stays exact across source
   reference, lowered interpreter, and accelerated free-running execution.

That is enough to justify docs/hygiene closeout plus one new saved planning
packet. It is not enough to justify automatic scope lift, arbitrary-language
claims, or any new compiler-boundary execution from momentum.

## Save Rule

Save this plan before any future compiler-boundary work.

Do not treat `R37` or `H30` as authorization for a broader compiled/lowered
wave by default. Any later extension must begin from a clean worktree and must
be explicitly reauthorized against the current `H30` machine state.

## Standing State After `H30`

- At the time this design was written,
  `H30_post_r36_r37_scope_decision_packet` was the live routing packet. It is
  now preserved historical context under
  `H32_post_r38_compiled_boundary_refreeze`.
- `H29_refreeze_after_r34_r35_origin_core_gate` remains the preserved upstream
  positive refreeze packet.
- `R36_origin_long_horizon_precision_scaling_gate` remains the preserved narrow
  precision-boundary audit.
- `R37_origin_compiler_boundary_gate` remains the preserved tiny
  compiled-boundary gate.
- `H27_refreeze_after_r32_r33_same_endpoint_decision` remains the preserved
  negative closeout of the old same-endpoint `D0` recovery route.
- `R29_d0_same_endpoint_systems_recovery_execution_gate` remains blocked.
- `F3_post_h23_scope_lift_decision_bundle` remains blocked.
- `F2_future_frontier_recheck_activation_matrix` remains planning-only.

## Recommended Near-Term Order

1. docs-only `H30` closeout sweep:
   remove stale `H25/H23` "current stage" wording from the current-facing
   entrypoints while preserving those packets as historical controls.
2. save and link this plan:
   make the later explicit packet concrete as a documented prerequisite rather
   than an implied future possibility.
3. `P17_h30_commit_hygiene_and_clean_worktree_promotion`:
   isolate the `H28/R34/R35/H29/R36/R37/H30` bundle plus the current control
   doc sweep in a reviewable subset without touching dirty `main`.
4. only after that, consider one later explicit packet:
   either a clarification-only packet with no new runtime execution, or one
   tightly bounded extension packet inside the same active substrate.

No new runtime experiment is required to close the present wave.

## Contract For The Later Explicit Packet

The later explicit packet must answer the following before any new execution is
started:

1. Is there still one scientifically useful compiler-boundary question left
   inside the current append-only / exact-retrieval / small-VM substrate?
2. Can that question be answered without widening the opcode surface
   materially, adding a hidden host evaluator, or relabeling the result as
   same-endpoint systems recovery?
3. If execution is still justified, what is the one admitted extension slice,
   its required rows, and its no-go stop rules?

Allowed outcomes:

- `clarification_only_no_extension`
- `execute_one_more_tiny_extension`
- `freeze_compiled_boundary_as_complete_for_now`

## If A Tiny Extension Is Later Reauthorized

Keep the scope narrower than the old `D0` rhetoric:

- prefer existing lowering/execution machinery only;
- prefer one additional source-shape or control-shape family rather than a
  broader language surface;
- keep source reference, lowered interpreter, accelerated free-running result,
  exact-final-state, and exact-trace checks explicit and separate;
- stop immediately if the work pressures the repo toward arbitrary `C`, demo
  rhetoric, or same-endpoint systems recovery claims.

No-go triggers:

- material opcode-surface widening;
- hidden host-side execution or hidden side channels;
- treating one extra admitted slice as arbitrary compiler support;
- softening `R29` or `F3` blockers by wording alone.

## Worktree And Delegation Rule

Before any later execution wave:

- save this plan and the active routing docs first;
- create a clean worktree from `wip/h27-promotion` or a clean successor branch;
- keep one thread on source/lowering/reference rows;
- keep one thread on exporters/tests/results;
- keep the integrating thread responsible for driver/claim wording and final
  handoff;
- do not merge back into dirty `main` during execution.

## Low-Risk Closeout Tasks For The Current Wave

- sync `README.md`, `STATUS.md`, `docs/publication_record/README.md`,
  `docs/publication_record/current_stage_driver.md`, and
  `tmp/active_wave_plan.md` to one `H30`-first wording set;
- mark `P15` as preserved prior same-endpoint handoff context rather than the
  current active handoff;
- create and keep one clean `P17` worktree scaffold for future packet copying;
- keep the historical `H25/H23` record intact, but stop presenting it as the
  current mainline state;
- verify doc consistency with search-based checks and `git diff --check`.
