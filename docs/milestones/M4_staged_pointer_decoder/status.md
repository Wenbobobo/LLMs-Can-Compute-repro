# Status

- Implemented `src/model/staged_pointer_event_models.py`.
- Exported `results/M4_staged_pointer_decoder/summary.json`.
- Added the harder `alternating_memory_loop` family to both train and held-out
  staged exports.
- Current checkpoint:
  - train exact-label accuracy `0.8383`
  - held-out exact-label accuracy `0.7951`
  - structural exact-trace rollout `0.1875` train / `0.0` held-out
  - `opcode_shape` exact-trace rollout `0.875` train / `0.5455` held-out
  - `opcode_legal` exact-trace rollout `1.0` train / `1.0` held-out

- Milestone state: partially complete with a stronger ablation story and a
  still-important caveat about mask strength.
