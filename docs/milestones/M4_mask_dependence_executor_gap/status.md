# Status

Batch complete. Current result is a negative closure with a cleaned failure
taxonomy.

Current blocker summary:
- train / held-out exact-trace rollout is `0.1 / 0.0` for `structural`;
- train / held-out exact-trace rollout is `0.2 / 0.0` for `opcode_shape`;
- train / held-out exact-trace rollout remains `1.0 / 1.0` for
  `opcode_legal`;
- held-out `structural` failures split across `control_flow`,
  `rollout_nontermination`, `memory_value`, and one `memory_address` case;
- held-out `opcode_shape` failures split across `memory_value` / `push_expr_0`
  trace mismatches (`8/15`) and `rollout_nontermination` / `step_budget`
  runtime failures (`7/15`);
- the fourth-regime decision remains negative because the dominant support
  ratio is only `0.5333`, below the `0.7` threshold.
