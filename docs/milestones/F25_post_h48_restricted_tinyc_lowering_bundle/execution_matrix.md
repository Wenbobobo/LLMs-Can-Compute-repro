# F25 Execution Matrix

| preserved kernel family | admitted restricted tiny-`C` shape | fixed runtime target | required first-pass outcome |
| --- | --- | --- | --- |
| `sum_i32_buffer` | one canonical counted loop over a declared `i32` buffer with one scalar accumulator | same held-out `R47` useful-case variants for `sum_i32_buffer` | exact on the preserved variant set before any wider numeric experiment |
| `count_nonzero_i32_buffer` | one canonical counted loop with one structured predicate branch and one scalar count | same held-out `R47` useful-case variants for `count_nonzero_i32_buffer` | exact on the preserved variant set without hidden side channels |
| `histogram16_u8` | one canonical counted loop over a declared byte buffer with updates into a predeclared `hist[16]` window | same held-out `R47` useful-case variants for `histogram16_u8` | exact on the preserved variant set with the fixed 16-bin boundary unchanged |

The first `R50` pass must:

- start from the preserved `R47` `8/8` useful-case variants across the fixed
  `3/3` kernel ladder;
- keep `claim_ceiling = bounded_useful_cases_only`;
- reuse the same substrate rather than introducing a new evaluator; and
- avoid fusing further numeric widening into the first tiny-`C` lowering gate.
