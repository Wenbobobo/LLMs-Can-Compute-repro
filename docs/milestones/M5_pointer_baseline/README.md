# M5 Pointer Baseline

Goal: give the standard softmax baseline one last narrow repair by moving it
onto the same pointer-space labels as the staged `M4` branch.

Current outcome:
- Exact pointer-label accuracy is `0.0` on both train and held-out programs.
- Free-running exact-trace rollout remains `0.0 / 0.0` under the valid
  structural regime.
- The intermediate `opcode_shape` diagnostic reaches `0.1875 / 0.0`, which is
  still not a held-out rescue.
- `opcode_legal` exact rollout reappears only as a diagnostic artifact and is
  not counted as valid baseline evidence.

Interpretation:
- Moving to pointer-space labels does not rescue the standard softmax baseline.
- The branch is now most useful as a documented negative control for mask
  strength.
