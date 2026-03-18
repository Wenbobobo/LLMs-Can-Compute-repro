# M6 Frontend Spec

This milestone remains spec-only, but the first frontend boundary is now
decision-complete.

Chosen boundary:
- first frontend: tiny typed bytecode;
- first goal: stress the existing execution substrate, not market a broad demo;
- first comparison: exact differential testing against a reference interpreter.
- first runtime target: current `exec_trace` semantics, not a new VM;
- first typed discipline: `i32`, `addr`, and `flag`.

Frozen bytecode opcodes:
- `const_i32`
- `const_addr`
- `dup`
- `pop`
- `add_i32`
- `sub_i32`
- `eq_i32`
- `load_static`
- `store_static`
- `load_indirect`
- `store_indirect`
- `jmp`
- `jz_zero`
- `halt`

Frozen lowering contract:
- `const_i32` and `const_addr` lower to `PUSH_CONST`; type identity is enforced
  by the verifier, not by the runtime opcode.
- `load_static` / `store_static` lower to `LOAD` / `STORE`.
- `load_indirect` / `store_indirect` lower to `LOAD_AT` / `STORE_AT`.
- `jz_zero` preserves the current zero-is-false branch semantics of `JZ`.
- first version has no calls, returns, locals, heap, floats, host effects, or
  concurrency.

Frozen success contract:
- short programs must match the reference trace exactly;
- longer programs must match final state exactly and emit first-divergence
  diagnostics if trace-level exactness breaks.

Explicitly out of scope for the first frontend:
- floating point;
- heap allocation;
- aliasing and undefined behavior;
- syscalls or host effects;
- threads or concurrency;
- any claim of arbitrary C support.
