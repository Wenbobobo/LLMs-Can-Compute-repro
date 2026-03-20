# Status

Provisioned on 2026-03-20 as a conditional `H14` lane.

- `R13` is not required by default;
- it exists only if `R11/R12` leave a bounded executor gap that benefits from a
  small trainable comparator;
- this lane must remain downstream of the deterministic reopened core.
