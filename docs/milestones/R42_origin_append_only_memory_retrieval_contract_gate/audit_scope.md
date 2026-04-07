# R42 Audit Scope

The fixed future task families are:

- `latest_write_same_address_short`
- `latest_write_same_address_long`
- `stack_slot_depth_short`
- `stack_slot_depth_long`
- `address_reuse_duplicate_and_tie_cases`
- `precision_range_sweep`

Every task must run on:

- a brute-force append-only reference implementation;
- the accelerated retrieval path under the same trace;
- exact task-level comparison of retrieved row identity and final value.

The point is to validate the retrieval contract, not to benchmark a full VM.
