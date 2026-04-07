# Post-R42 F20/H41 Control Override Design

This design lands the first explicit post-`R42` control override on top of the
completed `H40 -> R42` semantic-boundary activation wave.

## Objective

Land two docs-only artifacts in order:

1. `F20_post_r42_dual_mode_model_mainline_bundle`
2. `H41_post_r42_aggressive_long_arc_decision_packet`

The purpose is to make the user-selected aggressive long-arc posture explicit
without losing the narrow Origin-core scientific framing. This wave does not
yet execute `R43`, `R45`, `R44`, `R41`, or merge `main`.

## Packet Order

1. `F20_post_r42_dual_mode_model_mainline_bundle`
2. `H41_post_r42_aggressive_long_arc_decision_packet`

The order matters. `F20` must fix the exact-versus-model evidence boundary
before `H41` can authorize a coequal model lane.

## F20 Scope

`F20` is planning-only. It must:

- preserve `H40` as the preserved prior semantic-boundary activation packet;
- preserve `H36` as the underlying routing/refreeze packet;
- preserve `R42` as the completed first semantic-boundary gate;
- record `Coequal Mainline` as the model posture without replacing exact
  evidence;
- fix `Dual Mode` as the implementation posture:
  `compiled_weight_executor` plus `trainable_2d_executor`;
- state explicitly that exact `R43` evidence is decisive for the main
  scientific route;
- state explicitly that `R45` is a coequal comparator/operator lane, not a
  substitute for exact `R43`;
- keep `R44` deferred until a later post-`R43` route-selection packet.

`F20` must not:

- authorize execution by itself;
- let model-only positives count as exact bounded-memory execution evidence;
- widen the thesis to arbitrary `C`, unrestricted Wasm, or general computer
  rhetoric.

## H41 Scope

`H41` is docs-only. It must:

- preserve `H40`, `H36`, `R42`, `P26`, `F18`, and `F19`;
- incorporate `F20` as the current model-mainline bundle;
- select
  `authorize_r43_exact_mainline_and_coequal_r45_model_lane`;
- keep
  `hold_at_r42_and_continue_planning_only`
  as the non-selected alternative;
- authorize exactly
  `R43_origin_bounded_memory_small_vm_execution_gate`
  as the next exact runtime gate;
- authorize exactly
  `R45_origin_dual_mode_model_mainline_gate`
  as the coequal model lane;
- keep `R41` deferred;
- keep `R44` deferred until a later explicit `H42_post_r43_route_selection_packet`;
- record that merge still requires an explicit `P27` wave.

`H41` must not:

- treat `R42` as already proving bounded-memory small-VM execution;
- activate `R44`, `R41`, `F11`, `R29`, or `F3`;
- authorize merge-by-momentum into dirty `main`.

## Required Outputs

- `docs/plans/2026-03-24-post-r42-aggressive-long-arc-master-plan.md`
- `docs/plans/2026-03-24-post-r42-f20-h41-control-override-design.md`
- `docs/milestones/F20_post_r42_dual_mode_model_mainline_bundle/`
- `docs/milestones/H41_post_r42_aggressive_long_arc_decision_packet/`
- `scripts/export_f20_post_r42_dual_mode_model_mainline_bundle.py`
- `scripts/export_h41_post_r42_aggressive_long_arc_decision_packet.py`
- `tests/test_export_f20_post_r42_dual_mode_model_mainline_bundle.py`
- `tests/test_export_h41_post_r42_aggressive_long_arc_decision_packet.py`
- `results/F20_post_r42_dual_mode_model_mainline_bundle/summary.json`
- `results/H41_post_r42_aggressive_long_arc_decision_packet/summary.json`

Refresh the shared control surfaces once the artifacts land:

- `README.md`
- `STATUS.md`
- `docs/claims_matrix.md`
- `docs/milestones/README.md`
- `docs/plans/README.md`
- `docs/publication_record/current_stage_driver.md`
- `docs/publication_record/experiment_manifest.md`
- `tmp/active_wave_plan.md`

## Post-Wave State

If `F20` and `H41` land cleanly, the next saved order becomes:

`F20 -> H41 -> P27 -> R43 -> R45 -> H42 -> conditional R44`

Interpretation rules after landing:

- `R43` is the decisive exact next gate;
- `R45` is allowed as a coequal comparator/operator lane, but it cannot outrun
  the exact claim boundary;
- `R44` still requires a later post-`R43` route-selection packet;
- `R41` remains a deferred contradiction lane only.

## Non-Goals

This wave does not:

- merge `main`;
- execute `R43`, `R45`, or `R44`;
- reopen same-substrate contradiction work;
- change the bounded restricted-Wasm surface fixed by `F19`;
- widen the repo's public claim beyond the narrow Origin-core ladder.
