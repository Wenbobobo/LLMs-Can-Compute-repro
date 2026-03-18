# M5 Pointer Baseline

- `training_run.json` records the final narrow pointer-space baseline repair.
- Exact pointer-label accuracy is `0.0` on both train and held-out programs.
- The valid baseline result is the structural rollout section, which remains at
  `0.0 / 0.0` exact rollout on the exported train/held-out slice.
- The `opcode_shape` section improves only to `0.1875 / 0.0` and is still a
  failed held-out rescue.
- The `opcode_legal` section is diagnostic only and should not be cited as
  baseline success.
