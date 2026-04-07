# R61 Origin Compiled Useful-Kernel Value Gate

Actual comparator/value gate for the exact `R60` row set.

Current status: `completed_value_gate`.

Landed result:

- `compiled_useful_kernel_route_lacks_bounded_value`

`R61` kept all declared comparators exact on the admitted `R60` rows, but the
accelerated internal route did not retain bounded value over simpler baselines
once compiler/lowering overhead was counted.
