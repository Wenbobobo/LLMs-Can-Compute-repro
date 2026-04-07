# R50 Case Matrix

| Kernel | Variant | Expected narrow outcome |
| --- | --- | --- |
| `sum_i32_buffer` | `sum_len6_shifted_base` | exact; tiny-`C` lowering remains instruction-identical |
| `sum_i32_buffer` | `sum_len8_dense_mixed_sign` | exact; tiny-`C` lowering remains instruction-identical |
| `count_nonzero_i32_buffer` | `count_sparse_len8_shifted_base` | exact; tiny-`C` lowering remains instruction-identical |
| `count_nonzero_i32_buffer` | `count_dense_len7_shifted_base` | exact; tiny-`C` lowering remains instruction-identical |
| `count_nonzero_i32_buffer` | `count_mixed_len9_shifted_base` | exact; tiny-`C` lowering remains instruction-identical |
| `histogram16_u8` | `histogram_bimodal_len6_shifted_base` | exact; tiny-`C` lowering remains instruction-identical |
| `histogram16_u8` | `histogram_low_bin_skew_len8` | exact; tiny-`C` lowering remains instruction-identical |
| `histogram16_u8` | `histogram_wide_len10_shifted_base` | exact; tiny-`C` lowering remains instruction-identical |
