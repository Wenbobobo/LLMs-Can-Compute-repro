# M6 Typed Bytecode Harness

Goal: define the first compiled frontend as a tiny typed bytecode plus a
differential harness.

Frozen scope:
- translator target is the current `exec_trace` interpreter, with only a narrow
  control-flow widening for static-target non-recursive `call` / `ret`;
- verifier-visible types are `i32`, `addr`, and `flag`;
- unsupported features stay blocked rather than emulated loosely.

Frozen deliverables:
- `BytecodeInstruction` / `BytecodeProgram` IR;
- bytecode verifier with deterministic first-error reports;
- lowering into current `exec_trace` programs;
- control-flow-first widening via static-target non-recursive `call` / `ret`;
- differential harness comparing:
  bytecode reference interpreter,
  lowered `exec_trace` interpreter,
  and later execution branches when explicitly included.
