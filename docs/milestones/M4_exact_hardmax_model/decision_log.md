# Decision Log

- Reserve this milestone for exact hard-max semantics only.
- Start with latest-write memory retrieval before any trainable model work.
- Require linear-scan and accelerated decode modes to agree exactly on each
  read event.
