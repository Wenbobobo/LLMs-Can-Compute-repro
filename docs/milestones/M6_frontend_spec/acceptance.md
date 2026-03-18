# Acceptance

This spec milestone is complete when all of the following are true:

- the first frontend boundary is fixed to a tiny typed bytecode;
- the type discipline is fixed to `i32`, `addr`, and `flag`;
- the opcode set is frozen;
- the lowering rules into `exec_trace` are frozen;
- verifier and harness outputs are frozen;
- unsupported cases are explicit;
- short programs require exact trace matching;
- longer programs require at least exact final-state matching plus
  first-divergence diagnostics;
- the first stress-program suite is written down before implementation starts.
