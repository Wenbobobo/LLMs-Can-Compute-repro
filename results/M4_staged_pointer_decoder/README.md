# M4 Staged Pointer Decoder

- `summary.json` records the staged pointer checkpoint.
- Current exact pointer-label accuracy is `0.8383` on train and `0.7951` on
  held-out programs.
- Free-running exact-trace rollout is `0.1875 / 0.0` under structural masks,
  `0.875 / 0.5455` under `opcode_shape`, and `1.0 / 1.0` under
  `opcode_legal`.
- The held-out suite includes the harder `alternating_memory_loop` family.
- Read this artifact as a bridge result, not as final proof of a fully
  unconstrained neural executor.
