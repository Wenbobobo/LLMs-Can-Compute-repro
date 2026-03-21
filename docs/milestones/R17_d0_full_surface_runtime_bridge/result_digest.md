# Result Digest

`R17` completed the full admitted same-endpoint runtime bridge on the merged
`R8 + R15` surface and produced a negative bridge result together with one
bounded repair target.

## What `R17` closed

- profiled all `8/8` admitted runtime rows across `8` families and `2` source
  lanes after the `R16` handoff;
- kept exactness intact on the full surface, with `0` contradiction candidates;
- measured a median accelerated-versus-linear speedup of only about `1.0019x`,
  so decode gain remained immaterial on the same endpoint;
- measured a median accelerated-versus-lowered bridge ratio of about
  `1257.48x`, so the current exact executor remained far from the lowered
  endpoint;
- bounded deeper attribution to the unique boundary-bearing `R8` row
  `bytecode_helper_checkpoint_braid_long_180_a312_s0` and the heaviest
  admitted `R15` row `bytecode_stack_memory_braid_100_a112`;
- found retrieval to dominate both focused rows, with median retrieval share of
  exact runtime about `0.9968`;
- named one explicit `R18` target because
  `helper_checkpoint_braid_long` was also the worst full-surface bridge row and
  concentrated about `99.83%` of exact runtime in `retrieval_total`.

## What `R17` did not do

- did not produce a positive same-endpoint runtime bridge result;
- did not reopen a broader systems claim, unseen-family generalization, or
  arbitrary compiled-language support;
- did not justify skipping the repair decision: the packet now points to a
  bounded `R18` counterfactual rather than directly to `H17`.
