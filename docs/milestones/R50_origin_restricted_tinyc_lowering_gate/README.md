# R50 Origin Restricted Tiny-C Lowering Gate

Completed restricted tiny-`C` lowering gate after landed `F25`.

`R50` keeps the post-`H48` mainline deliberately small:

- it preserves `H48` as the current active docs-only packet and `H43` as the
  paper-grade endpoint;
- it reuses the preserved `R47` useful-case contract first rather than opening
  a broader frontend/runtime surface;
- it executes only one single-function static tiny-`C` source surface; and
- it does not fuse further numeric widening, heap, pointers, float, IO, or
  arbitrary `C` into the first pass.

The landed gate records `restricted_tinyc_lowering_supported_narrowly` with:

- `8/8` admitted tiny-`C` variants exact across the fixed `3/3` useful-case
  kernels;
- `8/8` translation-identity matches against the canonical bytecode kernels;
- `8/8` exact free-running executions on the same substrate; and
- `claim_ceiling = bounded_useful_cases_only`.

The next required packet is
`H49_post_r50_tinyc_lowering_decision_packet`.
