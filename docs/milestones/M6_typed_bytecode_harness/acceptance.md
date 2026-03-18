# Acceptance

- Complete only when all of the following are true:
- the first bytecode translator can be implemented without semantic guesswork;
- the verifier contract fixes stack typing and first-error reporting;
- lowering into `exec_trace` is one-to-one for the frozen opcode set;
- the differential harness output schema is frozen;
- short exact-trace and long exact-final-state comparison rules are explicit.
