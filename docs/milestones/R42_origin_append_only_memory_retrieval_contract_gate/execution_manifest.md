# R42 Execution Manifest

## Fixed Task Families

1. `latest_write_same_address_short`
2. `latest_write_same_address_long`
3. `stack_slot_depth_short`
4. `stack_slot_depth_long`
5. `address_reuse_duplicate_and_tie_cases`
6. `precision_range_sweep`

## Required Checks

- brute-force exact retrieval versus accelerated retrieval on the same
  append-only history;
- exact retrieved value agreement;
- exact maximizer-row identity agreement;
- explicit duplicate, tie, default-read, and range-sweep coverage;
- immediate stop on the first retrieval-contract break.
