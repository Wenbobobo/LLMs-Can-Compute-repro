# Acceptance

- `M5` must stay analytically separate from `M4`.
- The baseline must use standard softmax attention and keep head dimension fixed
  at 2 in the primary configuration.
- Training claims are out of scope until the branch can actually be run with
  PyTorch and report free-running evaluation, not only teacher-forced loss.
- Sequence representation, vocabulary, and architecture config must be fixed
  before any baseline result is treated as meaningful.
