# Open Questions

- How close should the baseline stay to the field note's tiny PyTorch snippet
  once training actually starts?
- After factorization reduced vocabulary pressure but did not fix rollout, is
  the right next move sequence compression, a different prompt/rollout boundary,
  or a model-side change?
- Should the comparison branch stay with instruction-conditioned full-trace
  generation, or move closer to an event-grouped decoder before scaling model
  size?
