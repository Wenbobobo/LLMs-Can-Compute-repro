# M5 Standard 2D Baseline

Current milestone: scaffold the comparison branch without conflating it with the
exact hard-max executor.

The current checkpoint includes:

- a structured trace-sequence serialization layer,
- vocabulary and sequence statistics helpers,
- a paper-like 2D-head softmax transformer definition,
- a teacher-forced training and free-running rollout pipeline,
- CUDA runtime detection and export,
- and first runnable artifacts under `results/M5_standard_2d_baseline/`.

This is now a trained baseline, but not yet a strong one. The first run reaches
nontrivial teacher-forced accuracy while still failing exact free-running
rollout on the current eval slice. The latest checkpoint adds a factorized
digit-level serialization comparison; it improves vocabulary stability and
pushes first error later, but still does not achieve exact rollout.
