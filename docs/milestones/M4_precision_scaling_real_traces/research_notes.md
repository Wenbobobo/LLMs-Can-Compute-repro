# Research Notes

- Native trace length can hide temporal precision problems; inflating
  `max_steps` reveals them without changing the stream itself.
- Adding alternating-memory offset streams matters because it reduces the risk
  that the real-trace story is a single-loop artifact.
- The current data suggest two distinct single-head failure modes on real
  streams: delayed collapse after horizon inflation and immediate collapse once
  address magnitude is already too large.
- Base `64` is currently a strong default on the exported suite, but that is an
  empirical observation, not yet a universal design rule.
