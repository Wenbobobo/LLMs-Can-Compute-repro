# R40 Acceptance

- the admitted and boundary rows each remain exact across source reference,
  lowering, and accelerated free-running execution;
- the positive rows pass memory-surface verification and family-scope checks;
- the positive rows use explicit typed `FLAG` slots rather than `I32` branch
  surrogates;
- at least one negative control is rejected by verifier/spec, at least one by
  memory-surface typing, and at least one by the bounded-family scope guard;
- no new opcode appears relative to the current compiled line.
