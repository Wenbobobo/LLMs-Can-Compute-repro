# Status

Second runnable checkpoint completed.

Current scope:

- structured tokenization of reference programs plus emitted trace events,
- baseline vocabulary construction and dataset statistics,
- a standard 2D-head softmax transformer definition,
- CUDA runtime validation in the project `uv` environment,
- paired atomic-vs-factorized serialization experiments,
- teacher-forced training and free-running rollout evaluation for both variants.

Current result:

- `torch==2.10.0+cu128` is installed and CUDA is available on the local GTX
  1650,
- the atomic union-vocab branch reaches train token accuracy about `0.97` and
  held-out teacher-forced token accuracy about `0.72`,
- the factorized train-only-vocab branch shrinks vocab size from `249` to `53`,
  reaches train token accuracy about `0.98`, and held-out teacher-forced token
  accuracy about `0.73`,
- factorization delays the first held-out countdown rollout error from token
  index `28` to token index `94`,
- exact free-running rollout is still `0.0` on current countdown, branch, and
  memory eval groups for both variants.

Not yet included:

- a baseline result that survives free-running rollout,
- a clean fairness study against `M4` under multiple prompt boundaries or model
  sizes,
- a decisive explanation of whether the remaining failure is mainly due to
  sequence length, rollout boundary, or model expressivity.
