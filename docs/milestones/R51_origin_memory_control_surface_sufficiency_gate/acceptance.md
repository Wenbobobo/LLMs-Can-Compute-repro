# R51 Acceptance

- the lane stays exact-first;
- the lane stays append-only and rejects hidden mutable side channels;
- the lane stays inside the declared bounded memory/control surface;
- required outputs include full-trace parity, final-state parity,
  maximizer-row identity, and first-fail artifacts;
- the lane ends with exactly one verdict:
  `memory_control_surface_supported_narrowly`,
  `memory_control_surface_mixed_with_explicit_boundary`, or
  `memory_control_surface_not_supported`; and
- no broader useful-case, trainable, or transformed-executor lane is activated
  directly from `R51`.
