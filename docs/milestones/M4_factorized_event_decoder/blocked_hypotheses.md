# Blocked Hypotheses

- A single-stage direct event-value decoder is not yet enough to stabilize
  free-running rollout, even with recent-history context and top-of-stack
  features.
- The next bottleneck likely sits in value prediction and PC prediction, not in
  stack-read/pop-count legality.
