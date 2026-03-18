# M5 Baseline Scaffold Design

## Goal

Start `M5` in a way that is technically useful now, even before committing to a
full PyTorch training run.

The immediate purpose of `M5` is comparison:

- keep the standard softmax branch separate from `M4`,
- define a faithful 2D-head baseline model shape,
- and create a deterministic dataset interface so later training and evaluation
  are not blocked on representation churn.

## Chosen Shape

- Add a trace-sequence serialization layer that turns reference programs and
  emitted events into structured token sequences.
- Add a baseline vocabulary and sequence statistics layer.
- Add a PyTorch model definition that mirrors the blog's tiny 2D-head
  transformer when `torch` is available.
- Keep Torch optional for now; the scaffold should still be importable and
  testable without forcing the dependency into every environment.

## Why This First

The real comparison question is not "can we train something eventually?" but
"what exact sequence representation and architecture are we comparing against?"
This scaffold fixes those choices now and keeps `M5` honest as a baseline
branch instead of a moving target.
