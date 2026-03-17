# Exact Hard-Max Decode Design

## Goal

Implement the smallest useful `M4` slice:

- exact 2D hard-max retrieval,
- causal online decode state,
- linear-scan reference path,
- `HullKVCache` accelerated path,
- and direct validation on `exec_trace` memory events.

## Options Considered

1. **Full trainable executor now**
   Too early. It mixes representation risk, optimization risk, and runtime risk.

2. **Deterministic decode layer over current trace semantics**
   Chosen. It isolates the real question: can latest-write memory reads be
   expressed as exact 2D hard-max retrieval with causal online updates?

3. **Jump straight to token-level end-to-end demos**
   Rejected for now. It would blur mechanism validation with presentation.

## Chosen Shape

- Use a latest-write addressing scheme over integer addresses.
- Seed bounded addresses with zero-valued writes.
- Encode each write at address `a` and causal step `t` as a 2D key whose
  dot-product with the address query prefers:
  1. exact address match,
  2. then the latest write for that address.
- Run each memory trace through two decoders:
  - brute-force hard-max lookup,
  - `HullKVCache` lookup.
- Require exact agreement on every read event.

## Why This First

This turns `M4` into a strict bridge between `M2` and `M3`.
If this bridge fails, there is no basis for a learned exact hard-max executor.
