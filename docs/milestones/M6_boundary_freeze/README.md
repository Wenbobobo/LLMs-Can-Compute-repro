# M6 Boundary Freeze

Goal: decide whether the current `D0` slice should be treated as the last
pre-demo widening.

Scope:

- evidence source is limited to `M6_typed_bytecode_harness`,
  `M6_memory_surface_followup`, and the synchronized `P1` bundle;
- no new opcode, type, control-flow, or memory-surface feature is introduced
  here;
- the outcome is a stop/go boundary decision, not a new implementation branch.

Deliverables:

- explicit freeze criteria for the current tiny typed-bytecode boundary;
- contradiction triggers that would reopen `M6` widening;
- synchronized wording across milestone docs, root docs, and publication
  ledgers.

Boundary-freeze rule:

- freeze the current `D0` slice if, and only if, the existing tiny
  typed-bytecode suite remains unchanged in semantics and continues to satisfy
  all three conditions:
  deterministic verifier behavior on the current positive/negative rows,
  exact agreement between the bytecode reference path and the lowered
  `exec_trace` path on the current comparison targets,
  and memory-surface diagnostics that remain appendix-level on the same slice
  rather than forcing a broader runtime claim;
- under this rule, “frozen” means later work may add pressure or extra oracles,
  but may not widen semantics.
