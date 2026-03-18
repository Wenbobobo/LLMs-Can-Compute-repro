# Status

- Implemented and exported `results/M5_pointer_baseline/training_run.json`.
- Matched the staged `M4` pointer label space and added the harder
  `alternating_memory_loop` family to the export.
- Current checkpoint:
  - train exact-label accuracy `0.0`
  - held-out exact-label accuracy `0.0`
  - structural exact-trace rollout `0.0` train / `0.0` held-out
  - `opcode_shape` diagnostic rollout `0.1875` train / `0.0` held-out
  - `opcode_legal` diagnostic rollout `1.0` train / `1.0` held-out

- Milestone state: negative control strengthened, not rescued.
