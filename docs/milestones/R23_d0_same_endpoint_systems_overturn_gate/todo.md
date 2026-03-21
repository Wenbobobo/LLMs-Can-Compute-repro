# Todo

- [x] Re-run the current systems gate on the positive `D0` suites using
  `pointer_like_exact` as a measured candidate.
- [x] Compare current best reference/spec, lowered `exec_trace`,
  `linear_exact`, current accelerated, and `pointer_like_exact`.
- [x] Export exactness, full-program runtime, per-step runtime, and component
  attribution in one bounded bundle.
- [x] End with exactly one verdict:
  `systems_materially_positive`, `systems_still_mixed`, or
  `systems_negative_under_same_endpoint`.
- [x] Do not widen endpoint, frontend, or compiled-language wording here.
