# Scripts

- `benchmark_geometry.py` — compare brute-force hard-max lookup with
  `HullKVCache`
- `export_runtime_environment.py` — record the current Python/Torch/CUDA runtime
- `export_m4_free_running.py` — export the exact free-running executor artifact
- `export_m4_induced_causal.py` — export the induced structured transition
  executor artifact
- `export_m4_factorized_event_decoder.py` — export the richer direct
  event-value decoder artifact
- `export_m4_precision_stress.py` — export finite-precision addressing sweeps
- `export_m4_real_trace_precision.py` — export finite-precision checks over
  real trace streams
- `export_m5_dataset_preview.py` — export the softmax-baseline dataset preview
- `export_m5_training_run.py` — train and export the first runnable softmax
  baseline checkpoint
- `export_m5_event_level_baseline.py` — train and export the final event-level
  standard softmax baseline
