# Decision Log

- Freeze the first compiled frontend to a tiny typed bytecode.
- Use a reference interpreter plus differential tests as the first correctness
  oracle.
- Reuse current `exec_trace` semantics as the first lowering target.
- Freeze the first typed discipline to `i32`, `addr`, and `flag`.
- Freeze the first opcode set to arithmetic, static memory, indirect memory,
  branch, and halt only.
- Defer implementation until the spec and paper-grade evidence bundle are both
  explicit enough that no semantic guesswork remains.
