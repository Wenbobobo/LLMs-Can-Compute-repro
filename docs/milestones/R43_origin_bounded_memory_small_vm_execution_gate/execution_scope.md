# R43 Execution Scope

The fixed future execution families are:

- `bounded_static_sum_loop`
- `bounded_branch_accumulator`
- `bounded_memory_reuse_loop`
- `stack_depth_revisit_loop`
- `single_call_return_accumulator` once the first four stay exact

The fixed execution rules are:

- append-only trace only;
- bounded locals and bounded static memory only;
- exact free-running execution only;
- compare full trace and final state against the reference interpreter;
- record length buckets large enough that linear scanning is visibly nontrivial.
