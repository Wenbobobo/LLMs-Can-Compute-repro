# Restricted Wasm Surface

The allowed future semantic surface is intentionally narrow.

Allowed now as future target:

- bounded `i32` values only;
- `const`, `add`, `sub`, `eq`, `lt`;
- structured branches and loops lowered into the current append-only trace VM;
- bounded locals;
- bounded static memory with explicit address ranges;
- optional single-layer `call/return` once `R43` stays exact.

Excluded by default:

- heap allocation;
- alias-heavy pointers;
- indirect calls;
- recursion;
- float;
- IO or external side effects;
- hidden mutable state outside the append-only trace;
- arbitrary `C` wording.

Execution default:

- reference interpreter plus exact lowering first;
- accelerated append-only retrieval second;
- any later trainable or translated model variant only as a comparator after
  exact lowering survives.
