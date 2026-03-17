# Decision Log

- Reserve this milestone for exact hard-max semantics only.
- Start with latest-write memory retrieval before any trainable model work.
- Require linear-scan and accelerated decode modes to agree exactly on each
  read event.
- Extend from immediate-address reads to dynamic-address reads before moving
  toward learned decode.
- Treat stack-slot retrieval as the next exact hard-max target because it uses
  the same causal latest-write structure without needing a new compiler layer.
- Start learned `M4` work with a two-parameter scorer over exact latest-write
  candidate sets, not with a token-level neural decoder.
- Use short countdown traces as the training slice and judge the scorer by exact
  success on longer countdown traces plus cross-family transfer.
