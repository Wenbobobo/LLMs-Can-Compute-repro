# R49 Case Matrix

| Bucket | Kernel | Variant | Expected narrow outcome |
| --- | --- | --- | --- |
| `bucket_a_2x` | `sum_i32_buffer` | `sum_len16_shift256` | exact; both admitted recovery regimes exact |
| `bucket_a_2x` | `count_nonzero_i32_buffer` | `count_len18_dense_shift256` | exact; `float32_single_head` boundary-bearing; both admitted recovery regimes exact |
| `bucket_a_2x` | `histogram16_u8` | `histogram_len16_lowbin_shift256` | exact; both admitted recovery regimes exact |
| `bucket_b_4x` | `sum_i32_buffer` | `sum_len32_shift1024` | exact; `float32_single_head` boundary-bearing; both admitted recovery regimes exact |
| `bucket_b_4x` | `count_nonzero_i32_buffer` | `count_len36_dense_shift1024` | exact; `float32_single_head` boundary-bearing; both admitted recovery regimes exact |
| `bucket_b_4x` | `histogram16_u8` | `histogram_len32_lowbin_shift1024` | exact; `float32_single_head` boundary-bearing; both admitted recovery regimes exact |
| `bucket_c_8x` | `sum_i32_buffer` | `sum_len64_shift4096` | exact; `float32_single_head` boundary-bearing; both admitted recovery regimes exact |
| `bucket_c_8x` | `count_nonzero_i32_buffer` | `count_len72_dense_shift4096` | exact; `float32_single_head` boundary-bearing; both admitted recovery regimes exact |
| `bucket_c_8x` | `histogram16_u8` | `histogram_len64_lowbin_shift4096` | exact; `float32_single_head` boundary-bearing; both admitted recovery regimes exact |
