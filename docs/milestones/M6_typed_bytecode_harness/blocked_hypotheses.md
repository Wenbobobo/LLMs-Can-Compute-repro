# Blocked Hypotheses

- Heap allocation, floating point, host effects, and concurrency remain blocked.
- Call/return frames, locals, and richer control-flow sugar remain blocked in
  v1.
- The first harness should compare against compiled demos or external solvers.
  Blocked because the first oracle is the in-repo bytecode and lowered
  `exec_trace` interpreters.
