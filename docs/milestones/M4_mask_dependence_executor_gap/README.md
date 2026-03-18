# M4 Mask Dependence and Executor Gap

Goal: explain the staged-pointer result mechanistically instead of reporting it
as a single exact-rollout headline.

This milestone asks a narrower question than the existing staged-pointer export:
when the same trained model is decoded under different legality regimes, how
much of the current success survives because the model predicts the right
candidate sources, and how much disappears because the stronger legality mask is
removing most of the remaining ambiguity?

This milestone is also where the project decides whether the current staged
result is already scientifically “closed enough” or whether one more
learned-skeleton step is justified.

Current closure:
- on the expanded held-out suite, `structural` and `opcode_shape` exact-trace
  rollout are both `0.0`, while `opcode_legal` remains `1.0`;
- `opcode_shape` no longer looks like a nearly-solved bridge problem: cleaned
  failures split between `push_expr_0` memory-value mismatches and
  `step_budget` nontermination;
- the dominant attributable mode reaches only `8/15`, so no narrower fourth
  compatibility regime is justified.

Historical entry conditions:
- the smaller staged slice had held-out `opcode_shape` exact-trace rollout
  `0.5455`;
- the expanded suite adds `flagged_indirect_accumulator` and
  `selector_checkpoint_bank`, plus the already-added harder
  `alternating_memory_loop` family;
- the purpose of this milestone was to decide whether the staged bridge still
  supported a fairer positive claim after that expansion. It does not.
