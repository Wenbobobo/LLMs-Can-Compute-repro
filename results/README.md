# Results

Tracked benchmark summaries and milestone outputs will live here.

- `M2_geometry_core/` for retrieval benchmarks
- `M3_trace_executor/` for trace-level outputs
- `M2_geometry_core/benchmark_geometry.json` is the first recorded geometry benchmark
- `M3_trace_executor/countdown_4_trace.json` is the first exported trace example
- `M3_trace_executor/latest_write_trace.json` demonstrates last-write-wins memory semantics
- `M3_trace_executor/memory_accumulator_trace.json` demonstrates bounded RAM read/write execution
- `M4_exact_hardmax_model/decode_examples.json` demonstrates exact agreement between
  linear-scan and accelerated latest-write decode on real trace examples,
  including dynamic-address memory access
- `M4_exact_hardmax_model/free_running_executor.json` records online exact rollout
  and the current stack-scorer rollout results
- `M4_exact_hardmax_model/precision_stress.json` records finite-precision
  address-range failure sweeps for the current 2D encoding
- `M5_standard_2d_baseline/dataset_preview.json` records the initial structured
  dataset preview for the standard softmax baseline branch
