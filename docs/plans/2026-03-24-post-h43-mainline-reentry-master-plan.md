# Post-H43 Mainline Reentry Master Plan

This plan defines the next explicit post-`H43` mainline without inflating the
scientific claim ceiling.

The current paper-grade endpoint remains the preserved
`H43_post_r44_useful_case_refreeze` line until later exact widening survives.
The current stack already supports:

- append-only traces as the execution substrate;
- exact `2D` hard-max retrieval on the fixed semantic-boundary contract;
- exact bounded-memory small-vm execution on the fixed `R43` family set;
- exact restricted useful-case support on the fixed `R44` three-kernel ladder;
- a coequal model lane on the landed `R43` contract family only.

The next mainline therefore does **not** jump directly into broader Wasm/C,
hybrid planner-executor claims, or merge-to-`main`. It reenters through one
explicit exact-first route.

## Locked Decisions

- default route choice: `exact_first_post_h43_reentry`
- preserved current paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- current low-priority docs wave remains:
  `P31_post_h43_blog_guardrails_refresh`
- merge posture remains:
  `explicit_merge_wave`
- `main` remains untouched during this reentry wave
- `R41`, `F11`, `R29`, and `F3` remain non-active here

## Why This Route

`H43` closed the prior useful-case packet by recording claim `D` as
`supported_here_narrowly` and returning the stack to
`no_active_downstream_runtime_lane`. That result is strong, but it is still
bounded to the fixed three-kernel useful-case ladder.

The next scientifically meaningful question is narrower than “arbitrary C” and
narrower than “models now run Wasm/C end to end”:

1. does the current exact useful-case surface generalize inside the same
   restricted envelope rather than only on the fixed `R44` rows;
2. if it does, can one extremely narrow restricted frontend translate into that
   same exact useful-case surface without excluded features;
3. only after those exact gates survive, can the admitted model lanes be
   compared on the same useful-case contract.

Rejected: jump directly from `H43` into broader Wasm/C or hybrid model work.

## Wave Structure

### Wave 0: Save, Fork, And Reindex

Save this plan, refresh `tmp/active_wave_plan.md`, create a clean worktree for
the post-`H43` route, and scaffold the next planning/decision/runtime folders.

### Wave 1: `F21_post_h43_exact_useful_case_expansion_bundle`

Planning-only bundle that fixes the exact-first reentry ladder.

`F21` must:

- preserve `H43` as the preserved prior useful-case refreeze packet and
  current paper-grade endpoint;
- preserve `H36` as the underlying routing/refreeze packet;
- preserve completed `R42/R43/R44/R45`, `F20`, and `P27`;
- define `R46_origin_useful_case_surface_generalization_gate` as the only
  first admissible next runtime candidate;
- define `R47_origin_restricted_frontend_translation_gate` as conditional on a
  positive `R46` plus later explicit packet;
- define `R48_origin_dual_mode_useful_case_model_gate` as comparator-only and
  conditional on surviving exact frontend evidence.

Required bundle tables:

- `surface_extension_matrix`
- `frontend_boundary_matrix`
- `model_bridge_scoreboard`

### Wave 2: `H44_post_h43_route_reauthorization_packet`

Docs-only packet that interprets the preserved `H43` state plus completed
`F21`.

Selected outcome:

- `authorize_r46_origin_useful_case_surface_generalization_gate`

Non-selected alternative:

- `hold_at_h43_and_continue_planning_only`

Machine-readable consequences:

- `current_paper_grade_endpoint = h43_post_r44_useful_case_refreeze`
- `authorized_next_runtime_candidate = r46_origin_useful_case_surface_generalization_gate`
- `deferred_future_runtime_candidate = r47_origin_restricted_frontend_translation_gate`
- `deferred_future_model_candidate = r48_origin_dual_mode_useful_case_model_gate`
- `later_explicit_packet_required_before_scope_widening = true`

### Wave 3: `R46_origin_useful_case_surface_generalization_gate`

Objective:

- test whether the landed `R44` useful-case ladder generalizes inside the same
  restricted surface rather than only on the fixed suite.

Allowed changes:

- buffer-length variation
- base-address shifts
- value-distribution shifts
- branch-density shifts
- histogram-skew shifts

Not allowed:

- new opcodes
- heap
- alias-heavy pointers
- recursion
- float
- IO
- hidden mutable state

Verdicts:

- `surface_generalizes_narrowly`
- `mixed_inside_surface`
- `fixed_suite_only`

### Wave 4: `H45_post_r46_surface_decision_packet`

Interpret `R46`.

- If `R46 = surface_generalizes_narrowly`, authorize `R47` and save planning
  bundle `F22_post_r46_useful_case_model_bridge_bundle`.
- If `R46 = mixed_inside_surface` or `fixed_suite_only`, refreeze and stop
  before frontend/model widening.

### Wave 5: `R47_origin_restricted_frontend_translation_gate`

Objective:

- test one tiny restricted frontend bridge onto the current useful-case
  contract.

Allowed surface:

- bounded `i32`
- bounded locals
- structured loop/branch
- static memory only
- no heap
- no alias-heavy pointers
- no recursion
- no float
- no IO

Verdicts:

- `restricted_frontend_supported_narrowly`
- `lowering_requires_excluded_feature`
- `exactness_break_inside_frontend_surface`

### Wave 6: `H46_post_r47_frontend_bridge_decision_packet`

Interpret `R47`.

- Only if `R47 = restricted_frontend_supported_narrowly` may the repo advance
  to `R48_origin_dual_mode_useful_case_model_gate`.
- Otherwise refreeze and stop.

### Wave 7: `R48_origin_dual_mode_useful_case_model_gate`

Comparator-only model lane on the exact preserved useful-case contract.

Modes:

- `compiled_weight_executor`
- `trainable_2d_executor`

Rules:

- exact evidence remains decisive;
- model positives do not replace exact failures;
- held-out useful-case family remains explicit;
- first-error position and failure class are mandatory outputs.

### Wave 8: `H47_post_r48_useful_case_bridge_refreeze`

Interpret `R48` without widening beyond bounded useful cases.

### Wave 9: Low-Priority Rollup And Future Storage

- `P35_post_h47_research_record_rollup`
- `F23_post_h47_numeric_scaling_bundle`
- `F24_post_h47_hybrid_executor_growth_bundle`

These remain subordinate to the exact reentry ladder.

## Stop Rules

This project is still materially short of a high-impact reproduction/falsifier.
The two strongest remaining exact gates are `R46` and `R47`.

Stop early if either of the following happens:

- `R46 = fixed_suite_only`
- `R47` needs excluded features, hidden mutable state, or breaks exactness on
  the declared narrow frontend bridge

Either outcome is strong enough to count as a practical falsifier of the near-
term “useful-case mainline extends cleanly toward Wasm/tiny-C” story.

## Execution Rules

Before each wave:

1. save the plan and current handoff first;
2. use clean worktrees, not dirty root `main`;
3. keep commits wave-scoped;
4. keep docs-only packets, runtime gates, model comparators, and publication
   syncs in separate commits;
5. push every green wave before starting the next one.

Do not merge back to `main` during this plan. Merge only through a later
explicit operational packet after the chosen wave range is internally coherent.
