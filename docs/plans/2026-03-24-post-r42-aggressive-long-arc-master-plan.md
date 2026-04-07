# Post-R42 Aggressive Long-Arc Master Plan

This plan turns the completed `H40 -> R42` activation wave into one explicit
multi-wave execution program. It is a routing aid, not claim-bearing evidence.
The current source of truth remains the landed `H40/H36/R42/P26/F15/F16/F17/
F18/F19` stack until later packets land.

## Locked Decisions

The current implementation adopts the following already-selected choices:

- execution posture: `aggressive_long_arc`
- merge posture: `explicit_merge_wave`
- model posture: `coequal mainline`
- implementation posture: `dual mode`
- admitted model implementations:
  `trainable_2d_executor` and `compiled_weight_executor`

These choices intentionally accelerate the semantic-boundary line without
changing the narrow scientific thesis:

- append-only execution traces remain the primary mechanistic object;
- geometric / sublinear retrieval remains a required contract, not an optional
  convenience;
- exact execution evidence remains distinct from model-only positive results;
- restricted Wasm / tiny-`C` stays bounded and useful-case scoped, not
  arbitrary `C` or general-computer rhetoric.

## Control Rule Before Execution

`R42` does not authorize `R43` by momentum. The current control stack still
requires one later explicit post-`R42` packet before any aggressive mainline
execution work can become canonical. Therefore the first execution wave must
land docs-only override surfaces that make the new route explicit.

Before each execution wave:

1. save the current plan and branch state first;
2. prefer clean git worktrees over the dirty root `main` checkout;
3. keep commits wave-scoped and machine-state aligned;
4. use subagents only for bounded parallel sidecar work;
5. avoid blurring exact-gate evidence with trainable-comparator evidence.

## Wave Structure

### Wave 0: Save, Push, Fork

Objective:

- save this master plan;
- push the clean `wip/h40-r42-exec` baseline to `origin`;
- create clean execution worktrees for the next three lanes.

Required outputs:

- `origin/wip/h40-r42-exec`
- clean worktree: `wip/h41-r43-mainline`
- clean worktree: `wip/p27-promotion-merge`
- clean worktree: `wip/r45-dualmode-model`

Acceptance:

- the saved plan is indexed under `docs/plans/README.md`;
- `wip/h40-r42-exec` remains reproducible and recoverable remotely;
- future wave branches start from the same saved baseline.

### Wave 1: Explicit Control Override

Objective:

- land one planning bundle,
  `F20_post_r42_dual_mode_model_mainline_bundle`;
- land one docs-only packet,
  `H41_post_r42_aggressive_long_arc_decision_packet`.

`F20` must:

- promote the dual-mode model route from saved option to authorized mainline
  comparator track;
- keep exact executor evidence and model evidence on separate scoreboards;
- define the two coequal model surfaces:
  `trainable_2d_executor` and `compiled_weight_executor`;
- preserve the restricted semantic boundary fixed by `F19`;
- keep dirty `main` unmerged until an explicit promotion packet lands.

`H41` must:

- preserve `H40` and `H36` underneath the stack;
- interpret positive `R42` as sufficient to open the bounded-memory exact lane;
- authorize `R43_origin_bounded_memory_small_vm_execution_gate`;
- authorize `R45_origin_dual_mode_model_mainline_gate` as a coequal comparator lane;
- keep `R41` deferred;
- keep `R44` deferred until a later explicit post-`R43` / post-`R45` packet.

Required outputs:

- milestone docs, exporter scripts, tests, and `results/.../summary.json` for
  `F20` and `H41`;
- refreshed control surfaces:
  `docs/publication_record/current_stage_driver.md`,
  `tmp/active_wave_plan.md`,
  `docs/milestones/README.md`,
  `docs/plans/README.md`,
  and the minimal shared indexes they affect.

Acceptance:

- `H41` becomes the current active docs-only packet;
- the next admissible execution order becomes:
  `H41 -> R43` and parallel `H41 -> R45`;
- `R44` remains blocked pending a later explicit route-selection packet.

### Wave 2: Promotion And Merge Hygiene

Objective:

- land `P27_post_h41_clean_promotion_and_explicit_merge_packet`.

`P27` must:

- record the clean source branch for the aggressive long-arc line;
- stage an explicit merge wave rather than drifting into `main`;
- define when `wip/h41-r43-mainline` is mature enough to merge;
- keep large derived artifacts and oversized probes outside accidental
  promotion.

Acceptance:

- merge posture changes only through `P27`;
- no ad hoc merge back to `main` occurs outside the packet.

### Wave 3: Exact Bounded-Memory Mainline

Objective:

- execute `R43_origin_bounded_memory_small_vm_execution_gate`.

Scope:

- extend the current exact append-only substrate from retrieval-only tasks to a
  bounded-memory small-VM execution lane;
- preserve exactness and explicit memory-retrieval semantics;
- stop on any need for hidden mutable state, retrieval ambiguity that changes
  machine semantics, or loss of exact replay.

Target evidence:

- exact small-VM execution on bounded local/static memory cases;
- stable replay and state equivalence against the spec/oracle harness;
- negative controls that reject unsupported boundary widens.

### Wave 4: Dual-Mode Model Mainline

Objective:

- execute `R45_origin_dual_mode_model_mainline_gate`.

Scope:

- implement two coequal comparator paths:
  `trainable_2d_executor` and `compiled_weight_executor`;
- evaluate them on the same bounded-memory execution tasks authorized by
  `H41`;
- keep reporting separate from `R43`.

Acceptance:

- exact executor and model executors produce directly comparable manifests;
- model wins never relabel an exact failure as a route success.

### Wave 5: Post-R43 Route Selection

Objective:

- land `H42_post_r43_route_selection_packet`.

Decision options:

- continue to `R44` if `R43` is exact enough and the useful-case kernel ladder
  is still justified;
- refreeze on `R43` if exact small-VM support lands but useful-case lowering is
  not yet ready;
- narrow or downgrade the model lane if `R45` underperforms or drifts from the
  exact substrate.

### Wave 6: Restricted Wasm / Tiny-C Useful Case

Objective:

- execute `R44_origin_restricted_wasm_useful_case_execution_gate`.

Scope:

- lower or translate the bounded allowed surface fixed by `F19`;
- run one useful-case kernel ladder such as
  `sum_i32_buffer`, `count_nonzero_i32_buffer`, and `histogram16_u8`;
- keep the claim at bounded useful cases, not arbitrary `C`.

### Wave 7: Low-Priority Closeout

Objective:

- finish low-priority paper/blog/README sync,
  experiment-manifest cleanup, and branch hygiene after the scientific gates
  stabilize.

This wave stays subordinate to the execution program until the exact or useful
case evidence catches up with the long-arc claim ladder.

## Execution Order

The intended near-term order is:

1. `Wave 0`
2. `Wave 1`
3. `Wave 2`
4. `Wave 3` and `Wave 4` in parallel where feasible
5. `Wave 5`
6. conditional `Wave 6`
7. low-priority `Wave 7`

## Merge Rule

Do not merge back to `main` merely because `wip/h27-promotion` is ahead or
because a worktree is clean. Merge only after:

- `P27` defines the explicit promotion target and artifact posture; and
- the selected wave commit range is internally coherent on a clean branch.

Until then, `main` remains a target of planned promotion, not the control
surface for active execution.

## Immediate Next Action

Implement `Wave 0` first, then land `F20` and `H41` before attempting `R43`,
`R45`, or any merge wave.
