# Todo

- Add `hotspot_memory_rewrite` memory streams.
- Add `flagged_indirect_accumulator` mixed streams.
- Add `selector_checkpoint_bank` checkpointed mixed streams.
- Add `stack_fanout_sum` stack-only streams.
- Record native horizon, first-failure multiplier, and failure type per stream.
- Run Stage 1 screening at base `64` across horizon multipliers `1/4/16/64`.
- Run Stage 2 base sweeps only on streams that show a real boundary signal.
- Keep `single_head`, `radix2`, and `block_recentered` as the only active
  schemes until the broader taxonomy exists.
- Avoid adding more decomposition ideas before the current schemes are fully
  mapped across the broader stream set.
- Update the claim boundary to exactly the validated suite.
