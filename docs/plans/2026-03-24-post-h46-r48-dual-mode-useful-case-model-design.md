# Post-H46 R48 Dual-Mode Useful-Case Model Design

## Objective

`R48_origin_dual_mode_useful_case_model_gate` executes the first
comparator-only model lane admitted by `H46`.

The gate remains deliberately narrow:

- the exact useful-case contract stays fixed to the `8` landed `R47`
  variants across the same `3/3` kernels;
- exact `R46/R47` evidence remains decisive;
- model positives do not replace exact failures; and
- broader Wasm/C, arbitrary `C`, hybrid model expansion, and merge posture stay
  out of scope.

## Locked Inputs

- current active docs-only packet:
  `H46_post_r47_frontend_bridge_decision_packet`;
- preserved prior decision packet:
  `H45_post_r46_surface_decision_packet`;
- current paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`;
- preserved prior exact runtime gate:
  `R46_origin_useful_case_surface_generalization_gate`;
- current exact frontend bridge gate:
  `R47_origin_restricted_frontend_translation_gate`;
- current exact-first planning bundle:
  `F21_post_h43_exact_useful_case_expansion_bundle`; and
- current comparator-planning bundle:
  `F22_post_r46_useful_case_model_bridge_bundle`.

## Contract

Run the comparator on the preserved `R47` useful-case contract:

- `2` `sum_i32_buffer` variants;
- `3` `count_nonzero_i32_buffer` variants; and
- `3` `histogram16_u8` variants.

The admitted modes remain:

- `compiled_weight_executor`; and
- `trainable_2d_executor`.

The trainable mode fits only on the explicit core kernel families
`sum_i32_buffer` and `count_nonzero_i32_buffer`. The held-out useful-case
family stays explicit as `histogram16_u8`.

## Outputs

Export:

- per-mode summaries;
- per-variant verdict rows;
- per-kernel rollups;
- first-error position; and
- failure class.

## Acceptance

- both admitted modes stay exact on the preserved useful-case contract;
- the trainable mode stays exact on the explicit held-out
  `histogram16_u8` family;
- `lane_verdict` remains comparator-only rather than substitutive; and
- the next required lane becomes
  `H47_post_r48_useful_case_bridge_refreeze`.
