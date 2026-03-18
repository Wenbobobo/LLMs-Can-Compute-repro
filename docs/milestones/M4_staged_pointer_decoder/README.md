# M4 Staged Pointer Decoder

Goal: bridge the gap between the weak direct event-value decoder and the much
stronger induced/opcode-conditioned branches by predicting candidate-source
expressions instead of raw values.

Current outcome:
- The staged checkpoint reaches exact pointer-label accuracy `0.8383` on train
  and `0.7951` on held-out programs.
- Free-running exact-trace rollout is `0.1875 / 0.0` under structural masks,
  `0.875 / 0.5455` under `opcode_shape`, and `1.0 / 1.0` under
  `opcode_legal`.
- The exported train/held-out slice now includes the harder
  `alternating_memory_loop` family alongside countdown, branch,
  indirect-memory, and ping-pong programs.

Interpretation:
- `opcode_shape` recovers a substantial part of the gap, so the learned
  candidate-source predictor is doing real work.
- Exact held-out execution still depends on the stronger `opcode_legal` masks.
- This is a meaningful bridge result, not yet evidence for a fully
  unconstrained neural executor.
