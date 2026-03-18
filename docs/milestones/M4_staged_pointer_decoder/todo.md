# Todo

- Test whether one more learned-skeleton step can improve beyond
  `opcode_shape` without requiring the full `opcode_legal` collapse.
- Extend the held-out slice beyond `alternating_memory_loop` into less templated
  branch-heavy or longer mixed-memory families.
- Record per-head failure patterns when moving from `opcode_legal` to
  `opcode_shape` and then to structural rollout.
