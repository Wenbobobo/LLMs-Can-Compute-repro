# Result Digest

- `results/M4_precision_organic_traces/claim_impact.json` now carries the
  current narrow `C3e` wording explicitly.
- The current organic bundle contains four concrete families:
  `hotspot_memory_rewrite`, `flagged_indirect_accumulator`,
  `selector_checkpoint_bank`, and `stack_fanout_sum`.
- All exported high-address memory families fail at `1x` under float32
  `single_head`; the deeper stack stream first fails at `4x`.
