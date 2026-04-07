# Stop/Go Criteria

This bundle is intentionally designed to be decisive.

## Go Conditions

The route may continue past `H56` only if both conditions hold:

- `R60` lands exact useful-kernel carryover on the admitted rows without
  material compiler-side work leakage; and
- `R61` shows bounded value relative to simpler baselines on those same rows.

If both conditions hold, the only allowed next move is one later explicit
planning packet for a slightly wider useful-family question.

## Stop Conditions

The route should stop at this layer if any of the following occurs:

- `R60` loses exactness on the admitted useful-kernel rows;
- `R60` requires so much compiler/export scaffolding that runtime-side meaning
  becomes ambiguous;
- `R61` is exact but value-negative against transparent or external baselines;
  or
- the only way to keep the route alive is to widen scope mid-wave.

## Reading Rule

- positive `R60` plus negative `R61` means "narrow mechanistic bridge only";
- negative `R60` means "toy compiled-boundary exactness only";
- positive `R60/R61` means "one later explicit useful-family packet is
  justified";
- none of the above means arbitrary `C`, broad Wasm, transformed entry, or
  trainable entry become active.
