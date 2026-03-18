# Result Digest

Use this file as the short unattended handoff after each batch.

## Batch
- date: 2026-03-18
- new stream families: `hotspot_memory_rewrite`, `flagged_indirect_accumulator`, `selector_checkpoint_bank`, `stack_fanout_sum`
- script / config snapshot: `scripts/export_m4_precision_generalization.py`

## Core metrics
- single-head failures added: all three new high-address memory streams fail at
  `1x`; `stack_fanout_sum_256` first fails at `4x`
- radix2 base-64 stable suite: all exported new memory streams through `64x`
- block-recentered base-64 stable suite: all exported new memory streams
  through `64x`

## Failure taxonomy shift
- tie-collapse cases: all observed failures on the expanded suite
- wrong-address inversion cases: none in the exported screening/boundary rows
- other cases: none

## Claim update
- broaden / narrow / unchanged: narrow and clarify
- exact new claim boundary: high-address memory remains the sharpest failure
  surface; stack streams are easier at depth `64` but no longer unconditionally
  easy by depth `256`
