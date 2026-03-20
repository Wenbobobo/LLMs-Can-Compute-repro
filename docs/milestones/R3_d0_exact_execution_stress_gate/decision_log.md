# Decision Log

- Keep `R3` on the current `D0` endpoint instead of widening the frontend.
- Treat precision follow-up as boundary accounting, not as an open-ended sweep
  program.
- Use the existing lowered-program path plus `run_free_running_exact(...)` to
  make linear-versus-Hull parity explicit without replacing the bytecode/spec
  agreement harness.
- Let only boundary-bearing longer streams enter the immediate precision
  companion screen, and use one weaker base-`256` block-recentered control
  rather than opening a new broad sweep.
- Route only true endpoint contradictions to `E1c`.
