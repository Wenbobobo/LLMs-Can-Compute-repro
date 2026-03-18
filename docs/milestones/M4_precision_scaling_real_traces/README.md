# M4 Precision Scaling Real Traces

Goal: validate finite-precision behavior on real trace streams rather than only
synthetic local sweeps.

Current outcome:
- Offset real traces expose the same family of failures seen in synthetic
  sweeps.
- `float32` single-head can still fail on large-address memory streams.
- The current radix/block decompositions recover the exported offset suite.
