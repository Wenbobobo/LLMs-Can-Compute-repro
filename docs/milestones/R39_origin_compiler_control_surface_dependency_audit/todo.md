# R39 Todo

- keep the primary case set anchored to
  `subroutine_braid_program(6, base_address=80)` and
  `subroutine_braid_long_program(12, base_address=160)`;
- define one predeclared semantics-preserving control-surface perturbation that
  stays inside the current verifier and opcode contract;
- keep verifier/spec parity, lowering parity, exact trace, and exact final
  state as separate checks;
- reject any design that introduces a new opcode, hidden host evaluator, or
  new program-family breadth;
- treat broader compiler, same-endpoint, and frontier stories as blocked
  regardless of local outcome.
