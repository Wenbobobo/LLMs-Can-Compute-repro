# Post-R50 H49 Tiny-C Lowering Decision Design

## Objective

`H49_post_r50_tinyc_lowering_decision_packet` is the only admissible
docs-only interpretation packet after landed `R50`.

This packet must decide whether positive `R50` evidence is enough to widen the
scientific story, or whether the correct reading is a narrow refreeze.

## Locked Inputs

- current active docs-only packet before this decision:
  `H48_post_r49_numeric_scaling_decision_packet`
- current post-`H48` planning bundle:
  `F25_post_h48_restricted_tinyc_lowering_bundle`
- current paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- preserved exact frontend bridge gate:
  `R47_origin_restricted_frontend_translation_gate`
- completed current restricted tiny-`C` lowering gate:
  `R50_origin_restricted_tinyc_lowering_gate`

`R50` is positive, but positive on a deliberately narrow admitted surface
only: one single-function static tiny-`C` lowering contract, fixed `3/3`
kernel ladder, `8/8` exact admitted variants, and
`claim_ceiling = bounded_useful_cases_only`.

## Admissible Outcomes

Exactly two outcomes are admissible:

- `freeze_r50_as_narrow_exact_tinyc_support_only`; or
- `treat_r50_as_scope_widening_authorization`.

No third “momentum” route is allowed here.

## Selected Route

The selected route is
`freeze_r50_as_narrow_exact_tinyc_support_only`.

`R50` demonstrates that one explicitly bounded tiny-`C` lowering surface can
target the preserved useful-case kernels exactly. It does not justify broader
Wasm, arbitrary `C`, heap, multi-function lowering, dynamic interfaces, or a
general compiler claim. There is also no saved downstream runtime placeholder
authorized beyond this packet.

`H49` therefore:

- preserves `H48` as the prior docs-only decision packet;
- preserves `H43` as the paper-grade endpoint;
- records `F25` and `R50` as completed evidence rather than active future work;
- rejects `treat_r50_as_scope_widening_authorization`; and
- restores `next_required_lane = no_active_downstream_runtime_lane`.

## Acceptance

- `H49` reads completed `R50` exactly as landed;
- `H49` selects exactly one of the two saved outcomes;
- the selected outcome keeps the claim ceiling bounded to useful cases only;
- no new downstream runtime lane is authorized by this packet; and
- any later scope lift still requires a fresh explicit packet beyond `H49`.
