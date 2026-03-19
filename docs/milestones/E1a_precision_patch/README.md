# E1a Precision Patch

Goal: sharpen the bounded `C3d/C3e` precision story on the already validated
suite and make one weak decomposition negative-control slice explicit without
widening scope.

Scope:

- current trace families only;
- stream-level first-failure and family-level boundary summaries;
- one explicit weaker coarse-bucket negative-control bundle on the same tracked suite;
- synchronized precision ledgers on the same bounded wording.

Non-goals:

- no new trace-family program;
- no broad robustness claim;
- no systems or compiled-boundary widening.
