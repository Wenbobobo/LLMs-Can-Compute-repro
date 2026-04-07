# R52 Origin Internal Vs External Executor Value Gate

Completed comparator/value gate after positive `R51`.

Current status: `completed_with_negative_value_verdict`.

`R52` is not another widening gate. It runs only on the exact `R51` rows and
asks whether the current internal exact route retains bounded system value
relative to simpler baselines once richer memory/control pressure already
survives.

The landed gate records `internal_route_lacks_bounded_value` with:

- all three comparators exact on `5/5` executed rows;
- accelerated internal exact faster than linear/reference on only `3/5` rows;
- accelerated internal exact faster than the plain external interpreter on
  `0/5` rows; and
- the external interpreter remaining materially faster and operationally
  simpler on every admitted row.

The next required packet is
`H50_post_r51_r52_scope_decision_packet`.
