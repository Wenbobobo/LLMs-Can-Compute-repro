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
- `M4_exact_hardmax_model/induced_causal_executor.json` records the induced
  structured event-generation branch and its held-out rollout results
- `M4_neural_event_executor/summary.json` records the neural structured-event
  decoder branch and its held-out rollout results
- `M4_factorized_event_decoder/summary.json` records the richer direct
  event-value decoder; this is the current teacher-forced-vs-rollout gap
  checkpoint for `M4`
- `M4_precision_scaling/summary.json` records single-head vs decomposition
  precision sweeps for the current 2D addressing family
- `M4_precision_scaling_real_traces/summary.json` records real-trace precision
  checks on offset loop and mixed stack-memory programs
- `M5_standard_2d_baseline/dataset_preview.json` records atomic vs factorized
  vs event-grouped serialization statistics for the standard softmax baseline
  branch
- `M5_standard_2d_baseline/training_run.json` records the atomic vs factorized
  vs event-grouped CUDA baseline training runs and rollout evaluation
- `M5_event_level_baseline/training_run.json` records the final event-level
  standard softmax baseline on the shared factorized event target
- `runtime_environment.json` records the Python, Torch, and CUDA runtime used
  for the current exported checkpoints
