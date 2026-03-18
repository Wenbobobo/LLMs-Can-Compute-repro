# Brainstorm Log

- The main question was whether `M5` was failing because of raw tokenization or
  because the standard softmax branch itself drifted during rollout.
- Pointer-space labels were chosen as the last fair repair because they align
  with the staged `M4` target while keeping the baseline architecture intact.
- `opcode_shape` was exported as an additional diagnostic so the comparison is
  not only “fair structural” versus “too-strong opcode-legal”.
- The branch is now valuable mainly as a cleaner negative control.
