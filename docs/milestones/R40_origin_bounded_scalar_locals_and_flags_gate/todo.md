# R40 Todo

- keep the admitted and boundary rows explicit and reproducible;
- keep the positive family frame-only, scalar-only, and explicitly typed around
  `FLAG` slots;
- keep the negative controls explicit and separate:
  non-flag branch operand, layout/type mismatch, and heap escape;
- preserve the no-new-opcode rule and the no-automatic-`R41` rule;
- hand interpretation to `H36_post_r40_bounded_scalar_family_refreeze`.
