# H47 Post-R48 Useful-Case Bridge Refreeze

Completed docs-only useful-case bridge refreeze packet after landed
comparator-only `R48` and preserved prior `H46`.

`H47` does not replace `H36` as the preserved active routing/refreeze packet,
and it does not displace `H43` as the current paper-grade endpoint. Instead,
it reads the landed `R48` result explicitly and chooses exactly one of two
outcomes:

- selected outcome:
  `freeze_r48_as_narrow_comparator_support_only`;
- non-selected alternative:
  `treat_r48_as_scope_widening_authorization`.

The packet records that `R48` already returned
`useful_case_model_lane_supported_without_replacing_exact` with both admitted
modes exact on the preserved `8/8` useful-case variants across the same `3/3`
kernels, while the trainable mode also stayed exact on the explicit held-out
`histogram16_u8` family (`3/3`). The scientifically honest consequence is
therefore to freeze `R48` as narrow comparator-only support, keep exact
`R46/R47` evidence decisive, keep
`F22_post_r46_useful_case_model_bridge_bundle` as the current
comparator-planning bundle, and restore
`no_active_downstream_runtime_lane`.
