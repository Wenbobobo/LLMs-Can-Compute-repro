# Post-R47 H46 Frontend Bridge Decision Design

## Objective

`H46_post_r47_frontend_bridge_decision_packet` interprets the landed exact
frontend bridge result from `R47`.

The decision stays deliberately narrow:

- the paper-grade endpoint remains `H43_post_r44_useful_case_refreeze`;
- the preserved active routing/refreeze packet remains
  `H36_post_r40_bounded_scalar_family_refreeze`;
- only one comparator-only model lane may follow from a positive `R47`; and
- no broader Wasm/C, arbitrary `C`, hybrid model scope lift, or merge
  promotion may occur by momentum.

## Locked Inputs

- current active docs-only packet before interpretation:
  `H45_post_r46_surface_decision_packet`;
- preserved prior route packet:
  `H44_post_h43_route_reauthorization_packet`;
- current paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`;
- preserved prior exact runtime gate:
  `R46_origin_useful_case_surface_generalization_gate`;
- current exact frontend bridge gate:
  `R47_origin_restricted_frontend_translation_gate`;
- current exact-first planning bundle:
  `F21_post_h43_exact_useful_case_expansion_bundle`;
- saved comparator bundle:
  `F22_post_r46_useful_case_model_bridge_bundle`; and
- explicit merge posture:
  `P27_post_h41_clean_promotion_and_explicit_merge_packet`.

## Decision Rule

`H46` evaluates exactly two outcomes:

- `authorize_r48_origin_dual_mode_useful_case_model_gate`; or
- `freeze_r47_as_frontend_only_and_stop`.

The first outcome is admissible only if `R47` already proves all of the
following on the preserved fixed useful-case contract:

- `lane_verdict = restricted_frontend_supported_narrowly`;
- `exact_variant_count = 8`;
- `exact_kernel_count = 3`; and
- `translation_identity_exact_count = 8`.

Otherwise the line must freeze `R47` as a narrow frontend-only result and stop.

## Control-Surface Consequences

If `R47` survives exactly as landed, `H46` must:

- become the current active docs-only decision packet;
- preserve `H45` as the prior docs-only decision packet;
- keep `R47` visible as the completed current exact frontend bridge gate;
- turn `F22` into the current comparator-planning bundle;
- authorize exactly `R48_origin_dual_mode_useful_case_model_gate`; and
- keep claim ceilings bounded to useful cases only.

## Acceptance

- the packet stays docs-only;
- `H43` remains the current paper-grade endpoint;
- `H36` remains the preserved active routing/refreeze packet;
- `R48` becomes the next required comparator-only model lane;
- model evidence remains explicitly downstream of exact evidence; and
- broader Wasm/C, broader hybrid model work, and merge remain non-active here.
