# M5 Standard 2D Baseline Results

## Current Scope

`M5` is now started as a scaffold branch, not yet as a trained baseline.

Current capability:

- structured trace-sequence serialization from `exec_trace` programs,
- vocabulary construction and sequence statistics,
- a paper-like 2D-head softmax transformer definition gated behind an optional
  Torch dependency,
- a first dataset preview artifact.

## Current Artifact

- `dataset_preview.json` records the current example count, vocabulary size,
  sequence-length range, and token/id previews for the first structured dataset
  slice.

## Not Yet Included

- installed Torch runtime in this environment,
- teacher-forced training runs,
- free-running baseline evaluation,
- comparison claims against `M4`.
