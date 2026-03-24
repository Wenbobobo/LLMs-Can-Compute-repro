# R52 Acceptance

- `R52` runs only on declared `R51` rows;
- the lane compares accelerated internal exact, internal linear/reference, and
  plain external runtime baselines explicitly;
- exactness remains the first constraint, not a secondary metric;
- the lane ends with exactly one verdict:
  `internal_route_retains_bounded_value` or
  `internal_route_lacks_bounded_value`; and
- no broader runtime or model lane is authorized directly from `R52`.
