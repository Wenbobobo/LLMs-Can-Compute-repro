# R46 Case Matrix

| Kernel | Variant | Axis tags | Expected narrow outcome |
| --- | --- | --- | --- |
| `sum_i32_buffer` | `sum_len6_shifted_base` | `buffer_length_shift`, `base_address_shift`, `value_distribution_shift` | exact |
| `sum_i32_buffer` | `sum_len8_dense_mixed_sign` | `buffer_length_shift`, `base_address_shift`, `value_distribution_shift` | exact |
| `count_nonzero_i32_buffer` | `count_sparse_len8_shifted_base` | `buffer_length_shift`, `base_address_shift`, `sparsity_shift` | exact |
| `count_nonzero_i32_buffer` | `count_dense_len7_shifted_base` | `buffer_length_shift`, `base_address_shift`, `density_shift` | exact |
| `count_nonzero_i32_buffer` | `count_mixed_len9_shifted_base` | `buffer_length_shift`, `base_address_shift`, `value_distribution_shift` | exact |
| `histogram16_u8` | `histogram_bimodal_len6_shifted_base` | `buffer_length_shift`, `base_address_shift`, `distribution_shape_shift` | exact |
| `histogram16_u8` | `histogram_low_bin_skew_len8` | `buffer_length_shift`, `distribution_shape_shift` | exact |
| `histogram16_u8` | `histogram_wide_len10_shifted_base` | `buffer_length_shift`, `base_address_shift`, `distribution_shape_shift` | exact |
