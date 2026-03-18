# Free-Running Executor Design

## Goal

Push `M4` past the current discriminative latest-write scorer and into a real
online rollout setting.

The target is still narrow:

- keep the reference `exec_trace` semantics fixed,
- carry only step-local summaries such as program counter and stack depth,
- recover value state through latest-write retrieval over append-only history,
- and compare a linear reference runtime against the `HullKVCache` fast path in
  true free-running execution.

## Chosen Shape

- Build a free-running executor over structured `TraceEvent`s, not raw token
  strings.
- Treat stack slots and memory addresses as separate latest-write spaces.
- Use latest-write retrieval for all value reads:
  - exact linear scan,
  - exact accelerated hull lookup,
  - and a trainable stack-only scorer as the first learned substitution.
- Reconstruct final state from emitted events with the existing replay engine,
  so the new executor still proves itself against append-only semantics rather
  than against an internal mutable stack.

## Why This First

This is the smallest version of "free-running exact execution" that is still
scientifically meaningful. If the substrate cannot reproduce the reference
trace online in this structured setting, there is no point jumping to a token
model or a compiler frontend.

## Immediate Boundaries

- Memory reads stay exact in this checkpoint.
- The learned scorer only replaces stack-slot reads.
- This is still not a token-level neural decoder and still not a compiled Wasm
  path.
