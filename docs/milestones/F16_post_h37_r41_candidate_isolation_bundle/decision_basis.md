# Decision Basis

`F16` uses the saved `R41` design as a fixed admissibility surface, not as
execution authorization.

Current basis:

- both helper-overencoding candidates remain scientifically relevant;
- neither helper-overencoding candidate is uniquely isolating yet;
- the easy-part-only slice candidate is not execution-ready because the
  required same-row slice pairs are still not mechanically declared on both
  fixed `R40` rows.

Decision consequence:

- `execution_ready_candidate_count = 0`;
- `bundle_verdict = no_candidate_ready`;
- `H38` must select `keep_h36_freeze`;
- `R41` remains deferred.
