# Todo

- [x] Reuse the hardest currently admitted `D0` families and the current
  bounded executor surface as the starting point.
- [x] Extend the `R21` grid past the current address, horizon, checkpoint, and
  hot-address settings without changing endpoint semantics.
- [x] Export branch rows, candidate rows, and first-fail diagnostics.
- [x] End with exactly one verdict:
  `first_boundary_failure_localized`, `no_failure_in_extended_grid`, or
  `resource_limited_without_failure`.
  Landed verdict: `no_failure_in_extended_grid`.
- [x] Do not open a repair lane from inside `R22`.
