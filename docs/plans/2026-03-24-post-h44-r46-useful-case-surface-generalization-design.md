# Post-H44 R46 Useful-Case Surface Generalization Design

## Objective

`R46_origin_useful_case_surface_generalization_gate` is the first exact
post-`H44` runtime lane. Its job is not to widen the project to arbitrary
`C`, broader Wasm, frontend translation, or model-side substitution. Its job
is only to answer one narrower question: does the landed `R44` useful-case
support remain exact on held-out variants that stay inside the same declared
restricted useful-case surface?

Success means the fixed three-kernel useful-case ladder is no longer merely a
three-row fixed-suite result. Failure still remains scientifically useful
because it would justify an early stop at fixed-suite support only.

## Locked Scope

- same append-only substrate as `R43/R44`;
- same restricted opcode surface as the landed useful-case kernels;
- same static-memory discipline with no heap admission;
- same three fixed kernels:
  `sum_i32_buffer`, `count_nonzero_i32_buffer`, `histogram16_u8`;
- only held-out in-surface variation across buffer length, base address, and
  value-distribution shape;
- no frontend widening, no unrestricted compiler claims, no arbitrary `C`, and
  no model lane replacing exact evidence.

## Fixed Variant Set

The gate is fixed before execution and does not adapt to intermediate results.
The held-out matrix is:

1. `sum_len6_shifted_base`
2. `sum_len8_dense_mixed_sign`
3. `count_sparse_len8_shifted_base`
4. `count_dense_len7_shifted_base`
5. `count_mixed_len9_shifted_base`
6. `histogram_bimodal_len6_shifted_base`
7. `histogram_low_bin_skew_len8`
8. `histogram_wide_len10_shifted_base`

## Execution Contract

Run the lane in a clean isolated worktree, keep the dirty root `main`
untouched, and preserve wave-local edits only. The exporter must validate:

- verifier pass;
- source/spec agreement;
- source/lowered agreement;
- free-running exact trace agreement;
- free-running exact final-state agreement;
- scope guard pass for every row.

The stop rule is immediate scientific failure on the first broken held-out
variant. If all eight held-out variants remain exact, the lane verdict is
`surface_generalizes_narrowly`.

## Acceptance

- all `8/8` held-out variants execute;
- all `8/8` held-out variants stay exact;
- all `3/3` kernels remain exact under held-out in-surface variation;
- the claim ceiling stays `bounded_useful_cases_only`;
- the result requires `H45_post_r46_surface_decision_packet` before any
  frontend, model, or broader compiled-surface interpretation.

## Follow-On Rule

`R46` does not widen the paper-grade endpoint by itself. Even a positive
result still keeps:

- `H44` as the current active docs-only packet;
- `H43` as the current paper-grade endpoint;
- `R47/R48` conditional only; and
- `H45` as the next required interpretation packet.
