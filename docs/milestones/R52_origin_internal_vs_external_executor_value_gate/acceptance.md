# R52 Acceptance

- `R52` runs only on declared `R51` rows;
- the lane compares accelerated internal exact, internal linear/reference, and
  plain external runtime baselines explicitly;
- exactness remains the first constraint, not a secondary metric;
- the lane ends with exactly one verdict:
  `internal_route_has_bounded_value`,
  `exact_but_no_system_value`, or
  `no_value_over_external_baseline`; and
- no broader runtime or model lane is authorized directly from `R52`.
