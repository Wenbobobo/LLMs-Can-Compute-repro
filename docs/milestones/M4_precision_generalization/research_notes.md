# Research Notes

- Native trace length can hide temporal-resolution failures; horizon inflation
  remains a high-value probe because it changes the epsilon term without
  changing the semantic trace.
- Offset transforms were useful to surface the problem quickly, but they are no
  longer enough as the main evidence suite.
- The next unattended batch keeps the scheme family fixed and instead broadens
  the stream family: hotspot rewrites, flagged indirect updates,
  selector-bank reuse, and deep stack fanout.
- The key next question is not whether decomposition sometimes helps; it is
  where and why it stops helping.
- Base `64` is currently the best empirical default, but that is still a suite
  observation, not a universal design rule.
