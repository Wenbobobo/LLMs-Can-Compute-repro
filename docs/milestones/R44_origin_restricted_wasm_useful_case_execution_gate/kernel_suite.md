# R44 Kernel Suite

The fixed kernel order is:

1. `sum_i32_buffer`
2. `count_nonzero_i32_buffer`
3. `histogram16_u8`

The stop rule is strict:

- do not advance to the next kernel after any exactness break;
- do not replace the kernel with a friendlier demo;
- do not claim restricted Wasm / tiny-`C` support unless all earlier kernels
  in the fixed order survive exactly.
