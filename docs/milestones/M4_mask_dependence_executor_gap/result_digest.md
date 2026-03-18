# Result Digest

Use this file as the short unattended handoff after each batch.

## Batch
- date: 2026-03-18
- code / script snapshot: `scripts/export_m4_mask_dependence_executor_gap.py`
- new family coverage: `flagged_indirect_accumulator`, `selector_checkpoint_bank`

## Core metrics
- structural held-out exact-trace: `0.0`
- opcode-shape held-out exact-trace: `0.0`
- opcode-legal held-out exact-trace: `1.0`
- extra regime held-out exact-trace (if any): not evaluated

## Failure taxonomy shift
- cleaned diagnostic split:
  `structural` held-out is `8` runtime exceptions plus `7` trace mismatches;
  `opcode_shape` held-out is `7` runtime exceptions plus `8` trace mismatches
- dominant attributable `opcode_shape` head: `push_expr_0` (`8/15`)
- remaining `opcode_shape` failures: `step_budget` nontermination (`7/15`)
- representative `push_expr_0` confusions:
  `eq -> read0`, `add -> read1`, and `memory_read_value -> const_arg`

## Decision
- close positive / close negative / continue: close negative
- if continue, exact next experiment: not applicable; move to claim freeze and
  publication sync
