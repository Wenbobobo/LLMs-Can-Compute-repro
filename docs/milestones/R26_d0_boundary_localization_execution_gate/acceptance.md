# Acceptance

- the executed rows match the predeclared first-wave manifest exactly;
- any first failure is rechecked and paired with at least one nearby exact row
  when available;
- the lane ends at
  `first_boundary_failure_localized`,
  `near_boundary_mixed_signal_needs_confirmation`,
  `grid_extended_still_not_localized`, or
  `resource_limited_before_localization`;
- no extra family, axis, suite, or endpoint is introduced.
