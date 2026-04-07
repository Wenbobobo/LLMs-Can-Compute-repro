# Post-P23 H35-R40 Bounded Scalar Runtime Design

This design executes the first post-`P23` runtime reopen on the narrowed
Origin-core line.

## Objective

Answer one sharper same-substrate question left open by `F13`:

- can explicit `bounded scalar locals and flags` stay exact on the current
  append-only / exact-retrieval / small-VM substrate;
- without adding a new opcode surface;
- without introducing heap-like aliasing, indirect address payloads, richer
  aggregate values, or broader compiler rhetoric.

## Packet Order

1. `H35_post_p23_bounded_scalar_family_runtime_decision_packet`
   authorizes exactly one runtime lane:
   `R40_origin_bounded_scalar_locals_and_flags_gate`.
2. `R40_origin_bounded_scalar_locals_and_flags_gate`
   executes one admitted row, one same-family boundary row, and explicit
   negative controls.
3. `H36_post_r40_bounded_scalar_family_refreeze`
   interprets the local result and either freezes it narrowly or records a
   mixed local outcome without widening scope.
4. `P24_post_h36_bounded_scalar_runtime_sync`
   aligns the driver, wave plan, and milestone indexes to the landed state.

## Runtime Scope

Admitted positive rows must satisfy all of the following:

- frame-only memory layout;
- scalar-only cells typed as `I32` or `FLAG`;
- at least one explicit `FLAG` slot loaded and stored through
  `LOAD_STATIC` / `STORE_STATIC`;
- branch visibility only through `EQ_I32 -> FLAG -> JZ_ZERO`;
- same opcode surface as the current compiled line, with no new opcodes.

Negative controls must separately demonstrate:

- non-flag branch operands are rejected;
- layout/type mismatches around explicit flag slots are rejected;
- heap-like escape is rejected by the family gate even if the generic
  substrate still supports it.

## Deferred Work

This wave does not execute the `F14` threat bundle directly.

- `runtime_irrelevance_via_compiler_helper_overencoding` and
  `fast_path_only_helps_the_easy_part` stay deferred to a later explicit lane;
- the placeholder after `H36` is
  `R41_origin_runtime_relevance_threat_stress_audit`;
- `R41` remains inactive until a new explicit post-`R40` packet authorizes it.
