# M4 Precision Scaling Real Traces

Goal: validate finite-precision behavior on real trace streams rather than only
synthetic local sweeps.

Current outcome:
- Offset real traces expose the same family of failures seen in synthetic
  sweeps.
- The float32 single-head scheme can still fail on large-address memory streams,
  and the newer horizon sweep shows that some native-pass streams fail once the
  effective horizon is inflated.
- The sweep now includes alternating-memory offset streams in addition to the
  earlier loop and ping-pong families.
- `alternating_offset_256_memory` first fails at `16x`, while
  `alternating_offset_2048_memory` fails already at `1x` under float32
  single-head.
- `radix2` and `block_recentered` with base `64` remain stable through the
  exported `64x` sweep on the current offset suite.
