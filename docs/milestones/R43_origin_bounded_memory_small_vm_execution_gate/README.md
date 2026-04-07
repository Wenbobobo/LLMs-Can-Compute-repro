# R43 Origin Bounded-Memory Small-VM Execution Gate

Executed the bounded-memory small-VM exact gate authorized by
`H41_post_r42_aggressive_long_arc_decision_packet`.

`R43` asks one bounded question:

- can fixed bounded-memory bytecode families preserve exact source/spec,
  source/lowered, and accelerated free-running behavior before any
  restricted-Wasm useful-case widening?

The lane executes five fixed families:

- `bounded_static_sum_loop`
- `bounded_branch_accumulator`
- `bounded_memory_reuse_loop`
- `stack_depth_revisit_loop`
- `single_call_return_accumulator`

The landed result is narrow and positive:

- all `5/5` families stay exact end-to-end, including `4/4` core families plus
  the gated optional single-call/return family;
- the stop rule never triggers and no family is skipped after prior failure;
- admissible layoutless fixed-memory families rely on surface-literal
  validation rather than full layout verification, without admitting heap
  regions or a widened substrate; and
- exact evidence now reaches the bounded-memory small-VM surface while leaving
  coequal model work to `R45` and useful-case route selection to later `H42`.
