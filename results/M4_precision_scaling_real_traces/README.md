# M4 Real-Trace Precision

- `summary.json` records quantized latest-write checks on real trace streams.
- `horizon_base_sweep.json` extends that with explicit float32 horizon/base
  sweeps over loop, ping-pong, and alternating offset streams.
- The current offset program families show that synthetic precision failure
  modes reappear on real memory streams once address magnitude is high enough.
- `alternating_offset_256_memory` first fails at `16x`, and
  `alternating_offset_2048_memory` fails already at `1x` in the single-head
  float32 scheme.
- `radix2` and `block_recentered` with base `64` remain stable through the
  exported `64x` multiplier on the current suite.
