# R49 Origin Useful-Case Numeric Scaling Gate

Completed narrow numeric-scaling gate after landed `H47`.

`R49` keeps the post-`H47` mainline deliberately small:

- it preserves `H47` as the current active docs-only packet and `H43` as the
  paper-grade endpoint;
- it keeps the fixed useful-case kernel ladder from `R46/R47`;
- it widens only buffer length, preserved absolute base span, and exact step
  budget inside the saved `F23` envelope; and
- it evaluates only the admitted float32 recovery regimes plus sampled
  `float64` reference rows.

The landed gate records `numeric_scaling_survives_through_bucket_c` with:

- `9/9` widened cases exact across the fixed `3/3` useful-case kernels;
- `7/9` `float32_single_head` failures by explicit `tie_collapse`; and
- `9/9` recovery under both `float32_radix2` and
  `float32_block_recentered` across all three buckets.

The next required packet is
`H48_post_r49_numeric_scaling_decision_packet`.
