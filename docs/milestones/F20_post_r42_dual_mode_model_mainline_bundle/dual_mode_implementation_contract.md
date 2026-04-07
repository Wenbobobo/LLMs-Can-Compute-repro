# Dual-Mode Implementation Contract

The admitted model implementations are:

1. `compiled_weight_executor`
2. `trainable_2d_executor`

Required contract:

- both modes must target the same bounded task families as the exact lane once
  the exact contract is fixed;
- both modes must report exact-versus-approximate behavior explicitly;
- both modes are evaluated against exact baselines rather than against each
  other alone;
- neither mode may rely on hidden mutable state that the exact route forbids.
