# Experiment Matrix

| Stream family | Space | Schemes | Primary metric | Secondary outputs | Decision use |
| --- | --- | --- | --- | --- | --- |
| `hotspot_memory_rewrite` | memory | `single_head`, `radix2`, `block_recentered` | first-failure multiplier | failure type | test repeated overwrites on a tiny bank |
| `flagged_indirect_accumulator` | memory + stack | `single_head`, `radix2`, `block_recentered` | first-failure multiplier | native-vs-inflated gap | test branch-heavy indirect reuse |
| `selector_checkpoint_bank` | memory + stack | `single_head`, `radix2`, `block_recentered` | first-failure multiplier | failure type | test checkpointed target-address reuse |
| `stack_fanout_sum` | stack | `single_head`, `radix2`, `block_recentered` | max stable multiplier | stack-vs-memory boundary | test whether stack remains easier |
