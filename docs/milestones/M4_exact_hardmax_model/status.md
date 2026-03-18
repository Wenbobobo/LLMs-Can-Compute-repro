# Status

`M4` now has three implemented checkpoints:

- exact latest-write decode over extracted read events,
- a narrow trainable stack latest-write scorer,
- and a free-running online executor that recovers value state through
  latest-write retrieval during rollout.

Current scope:

- exact 2D hard-max latest-write encoding,
- linear-scan reference decode,
- `HullKVCache` accelerated decode,
- validation against real `exec_trace` memory and stack examples,
- a two-parameter trainable scorer fitted on short countdown stack traces,
- free-running exact linear and accelerated executors,
- finite-precision stress checks for parabolic 2D addressing.

Current exported results:

- the trainable scorer still selects `quadratic_scale=0.25` and
  `time_scale=0.0005`,
- exact linear and accelerated free-running executors both match the reference
  trace on current countdown, branch, and bounded-RAM program families,
- the trainable stack scorer also reaches exact trace accuracy `1.0` on
  countdown train, countdown held-out, branch, and current memory program
  families, while memory reads remain exact in that checkpoint,
- finite-precision stress shows local identity retrieval staying stable to
  address limit `8192` in `float64`, to `4096` in `float32`, failing by `64` in
  `float16`, and by `32` in `bfloat16`,
- latest-write time bias is much more fragile: the first local failure appears
  by `512` in `float32`, by `16` in `float16`, and immediately in small ranges
  for `bfloat16`.

This is still not yet a token-level learned executor branch. The learned slice
is causal only at the stack-read selection level, not at the event-generation
level.
