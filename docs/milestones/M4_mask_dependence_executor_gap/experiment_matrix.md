# Experiment Matrix

| Experiment | New family? | Regimes | Primary metric | Secondary outputs | Decision use |
| --- | --- | --- | --- | --- | --- |
| Baseline regime replay | no | `structural`, `opcode_shape`, `opcode_legal` | exact trace accuracy | first-error field/class | establish current gap |
| `flagged_indirect_accumulator` | yes | `structural`, `opcode_shape`, `opcode_legal` | held-out exact trace accuracy | per-program failure digest | test branch-heavy indirect memory reuse |
| `selector_checkpoint_bank` | yes | `structural`, `opcode_shape`, `opcode_legal` | held-out exact trace accuracy | first-error head/class histogram | test checkpointed target-address reuse plus 3-way branching |
| Optional extra regime | conditional | one added regime plus baseline ladder | held-out exact trace delta vs `opcode_shape` | failure family shrinkage | decide whether one more learned-skeleton step is justified |
