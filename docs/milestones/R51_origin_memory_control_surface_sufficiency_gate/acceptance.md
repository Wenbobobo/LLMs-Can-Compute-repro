# R51 Acceptance

- the lane stays exact-first;
- the lane stays append-only and rejects hidden mutable side channels;
- the lane stays inside the declared bounded memory/control surface;
- required outputs include full-trace parity, final-state parity,
  maximizer-row identity, and first-fail artifacts;
- the lane ends with exactly one verdict:
  `surface_extends_narrowly`, `mixed_with_explicit_boundary`, or
  `fails_memory_control_sufficiency`; and
- no broader useful-case, trainable, or transformed-executor lane is activated
  directly from `R51`.
