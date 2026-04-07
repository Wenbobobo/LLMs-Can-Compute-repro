# F21 Surface Extension Matrix

| wave | objective | preserved contract | allowed variation | stop rule |
| --- | --- | --- | --- | --- |
| `R46_origin_useful_case_surface_generalization_gate` | test whether landed `R44` useful-case support generalizes inside the same restricted surface | fixed `R44` three-kernel family: `sum_i32_buffer`, `count_nonzero_i32_buffer`, `histogram16_u8` | buffer-length shifts, base-address shifts, value-distribution shifts, zero-density shifts, histogram-skew shifts | stop at `fixed_suite_only`, first exactness break, or any need for excluded features |
| `H45_post_r46_surface_decision_packet` | interpret `R46` and decide whether exact widening remains admissible | preserved `H43` paper-grade endpoint plus completed `R42/R43/R44/R45` stack | route choice only; no new runtime work | stop if `R46` is not `surface_generalizes_narrowly` |
