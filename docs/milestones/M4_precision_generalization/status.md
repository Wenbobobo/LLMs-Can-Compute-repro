# Status

Batch complete on the reduced unattended core suite.

Current blocker summary:
- high-address memory streams now fail immediately under float32 single-head on
  all three new memory families:
  `hotspot_memory_rewrite`, `flagged_indirect_accumulator`,
  `selector_checkpoint_bank`;
- `stack_fanout_sum_64` stays stable through the exported screening sweep, but
  `stack_fanout_sum_256` first fails at `4x`;
- observed failure type remains `tie_collapse` on the expanded suite;
- decomposition stays strong on the new memory streams, while the deeper stack
  stream is stricter: at `64x`, only base `32` stays stable for the exported
  stack-256 boundary rows.
