# R40 Origin Bounded Scalar Locals And Flags Gate

Executed the first post-`P23` same-substrate runtime gate authorized by
`H35_post_p23_bounded_scalar_family_runtime_decision_packet`.

`R40` asks one bounded question:

- can explicit bounded frame locals plus explicit typed `FLAG` slots stay exact
  on the current append-only / exact-retrieval / small-VM substrate, without
  widening the opcode surface?

The lane executes:

- one admitted row:
  `bounded_scalar_flag_loop_program(6, base_address=320)`;
- one same-family boundary row:
  `bounded_scalar_flag_loop_long_program(12, base_address=336)`;
- three negative controls that separately target non-flag branch operands,
  flag/layout mismatch, and heap escape.

The landed result is narrow and positive:

- both positive rows stay exact at source reference, lowered execution, and
  accelerated free-running execution;
- both positive rows pass memory-surface verification and family-scope checks;
- the negative controls are rejected by the intended gate surfaces;
- no new opcode is introduced.
