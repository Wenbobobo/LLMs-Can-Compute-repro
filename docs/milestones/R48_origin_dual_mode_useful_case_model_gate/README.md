# R48 Origin Dual-Mode Useful-Case Model Gate

Completed current comparator-only model gate under active docs-only `H46`.

`R48` compares `compiled_weight_executor` and `trainable_2d_executor` against
the preserved exact useful-case contract admitted by exact `R47`.

The landed gate stays deliberately narrow:

- both admitted modes remain subordinate to exact evidence rather than
  substituting for it;
- the preserved contract stays fixed to the same `8/8` useful-case variants
  across the same `3/3` kernels already preserved by `R46/R47`;
- the `trainable_2d_executor` fits only on the explicit core kernel families
  `sum_i32_buffer` and `count_nonzero_i32_buffer`; and
- the held-out useful-case family remains explicit as
  `histogram16_u8`.

The landed result records
`lane_verdict = useful_case_model_lane_supported_without_replacing_exact`.
Both admitted modes stay exact on all `8/8` variants, and the trainable mode
also stays exact on the explicit held-out `histogram16_u8` family (`3/3`
variants). First-error position and failure class remain mandatory outputs if a
later rerun ever breaks.
