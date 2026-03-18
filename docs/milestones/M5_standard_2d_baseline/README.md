# M5 Standard 2D Baseline

Current milestone: scaffold the comparison branch without conflating it with the
exact hard-max executor.

The current checkpoint includes:

- a structured trace-sequence serialization layer,
- vocabulary and sequence statistics helpers,
- a paper-like 2D-head softmax transformer definition gated behind an optional
  Torch dependency,
- and a first dataset preview artifact under `results/M5_standard_2d_baseline/`.

This is not yet a trained or evaluated baseline.
