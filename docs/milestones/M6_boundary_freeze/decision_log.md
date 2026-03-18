# Decision Log

- Freeze rule:
  treat the current `D0` slice as frozen if, and only if, the existing tiny
  typed-bytecode suite remains unchanged in semantics and continues to satisfy
  all three conditions:
  deterministic verifier behavior on the current positive/negative rows,
  exact agreement between the bytecode reference path and the lowered
  `exec_trace` path on the current comparison targets,
  and memory-surface diagnostics that remain appendix-level on the same slice
  rather than forcing a broader runtime claim.
- Interpretation of “frozen”:
  later work may add pressure and extra oracles, but not new semantics.
- Handoff rule:
  once the freeze rule and contradiction triggers are written into the
  milestone docs and publication ledgers, the next stage may add exactly one
  serious stress family and exactly one independent external reference path.
  It may not add new opcodes, new types, recursion, dynamic call targets, heap
  allocation, syscalls, or broader compiled-demo claims.
- Reopen condition:
  reopen `M6` widening only if verifier behavior changes on the frozen suite,
  bytecode-reference vs lowered-`exec_trace` agreement breaks on the frozen
  suite, memory-surface diagnostics require new semantics rather than
  diagnostic metadata, or the downstream external reference oracle disagrees on
  the same frozen slice.
