# Program Suite

The first bytecode stress suite is fixed before implementation.

## Short exact-trace programs

- `const_add_halt`
  Push two constants, add, halt.
- `eq_branch_true` / `eq_branch_false`
  Exercise `eq_i32` plus `jz_zero` on both branch outcomes.
- `static_store_reload`
  Write one static address and read it back.
- `indirect_store_reload`
  Compute an address on the stack, write through it, then read it back.

## Medium exact-trace programs

- `countdown_loop`
  Bytecode version of the current countdown family.
- `dynamic_latest_write`
  Bytecode version of the indirect latest-write family.
- `alternating_memory_loop`
  Bytecode version of the harder branch-heavy mixed-memory family.
- `selector_checkpoint_bank`
  Bytecode version of a branch-controlled checkpoint selection pattern.

## Long exact-final-state programs

- `indirect_counter_bank`
  Long indirect write/read loop where final accumulator and memory bank must
  match exactly.
- `stack_memory_braid`
  Alternates stack arithmetic and indirect memory traffic over a longer horizon.
- `checkpoint_replay_long`
  Repeated branch-controlled reload/write program where trace divergence may be
  tolerated only if final state and divergence digest are recorded.
