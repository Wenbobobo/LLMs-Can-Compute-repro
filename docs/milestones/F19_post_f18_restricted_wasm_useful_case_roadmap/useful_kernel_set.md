# Useful Kernel Set

The useful-case ladder is fixed in increasing pressure order.

1. `sum_i32_buffer`
   - read-heavy and control-light;
   - first bounded static-memory kernel;
   - failure here means do not proceed to richer kernels.

2. `count_nonzero_i32_buffer`
   - adds data-dependent branching without changing the bounded memory surface;
   - must stay exact under free-running execution and final-state comparison.

3. `histogram16_u8`
   - first explicit latest-write-by-address pressure kernel;
   - bounded address reuse is the point, not raw throughput;
   - this is the earliest kernel that can count as exceeding the current
     article-level substrate evidence.

The kernel ladder remains useful-case evidence, not a general benchmark claim.
