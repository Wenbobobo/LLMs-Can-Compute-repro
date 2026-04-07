# Post-R46 H45 Surface Decision Design

## Objective

`H45_post_r46_surface_decision_packet` is the required docs-only interpretation
packet after landed `R46`. Its job is not to widen the project to broader
Wasm/C or model-side narrative. Its job is only to decide whether the positive
`R46` result is strong enough to admit one exact restricted frontend bridge as
the next runtime candidate.

## Locked Inputs

- preserved paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`;
- preserved prior docs-only route packet:
  `H44_post_h43_route_reauthorization_packet`;
- preserved active routing/refreeze packet:
  `H36_post_r40_bounded_scalar_family_refreeze`;
- completed gates:
  `R42`, `R43`, `R44`, `R45`, and `R46`;
- preserved planning bundle:
  `F21_post_h43_exact_useful_case_expansion_bundle`;
- preserved explicit merge packet:
  `P27_post_h41_clean_promotion_and_explicit_merge_packet`.

## Decision

Selected outcome:

- `authorize_r47_origin_restricted_frontend_translation_gate`

Non-selected alternatives:

- `freeze_r46_as_mixed_inside_surface_and_stop`
- `freeze_r46_as_fixed_suite_only_and_stop`

The reason is simple: `R46` already returned `surface_generalizes_narrowly` on
`8/8` held-out in-surface variants across the fixed `3/3` useful-case kernels,
without raising the claim ceiling above `bounded_useful_cases_only`.

## Consequences

- `H45` becomes the current active docs-only decision packet.
- `H43` remains the current paper-grade endpoint.
- `R47_origin_restricted_frontend_translation_gate` becomes the only
  authorized next runtime candidate.
- `F22_post_r46_useful_case_model_bridge_bundle` is saved only as a blocked
  future comparator bundle.
- `R48_origin_dual_mode_useful_case_model_gate` remains blocked until later
  exact frontend evidence survives and `H46` interprets it explicitly.
- `merge_executed = false` remains unchanged.

## Acceptance

- `H45` reads `R46` exactly as landed rather than re-running it.
- The packet stays docs-only and does not move the claim ceiling.
- Control surfaces update to `H45 active`, `H43 endpoint`, `R47 next required`.
- `R41`, broader Wasm/C, hybrid model work, and merge-to-`main` remain
  non-active.
