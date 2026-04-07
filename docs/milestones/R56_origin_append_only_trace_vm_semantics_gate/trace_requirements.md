# R56 Trace Requirements

- export instruction-by-instruction traces for both reference and candidate
  routes;
- record state, stack, and memory deltas on every step;
- keep the row set fixed and bounded;
- localize the first mismatch to one instruction transition; and
- separate semantic mismatches from performance-only observations.
