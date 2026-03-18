# Status

- Implemented on 2026-03-18.
- Held-out `opcode_shape` remains a full failure slice, but the earlier
  `step_budget` rows are now separated from their first semantic causes.
- Current exported held-out split is:
  - `8/15` direct `memory_value_root_cause`
  - `7/15` `downstream_nontermination_after_semantic_error`
