# Reference Semantics

The candidate family adds one bounded scalar-local layer to the current
Origin-core executor floor.

Reference semantics:

1. local slots are drawn from one fixed finite set, for example
   `L0`, `L1`, `L2`, `F0`, `F1`;
2. each slot stores one scalar from a fixed bounded domain, for example:
   booleans for `F*` and bounded integers for `L*`;
3. writes replace the logical value of one named slot;
4. reads recover the latest logical value of one named slot;
5. branch behavior may depend on those slot values, but only through explicit
   branch-visible comparisons already expressible on the current opcode
   surface.

Semantic non-goals:

- no hidden aggregate record semantics;
- no cross-slot atomic transaction semantics;
- no external observable other than saved trace or final state.
