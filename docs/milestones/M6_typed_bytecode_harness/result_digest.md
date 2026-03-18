# Result Digest

- The verifier now reports deterministic first errors for malformed static
  addresses, bad branch targets, invalid call targets, empty returns,
  unterminated frames, recursive call cycles, and wrong stack typing.
- The current harness batch shows exact agreement between the bytecode
  reference interpreter and the lowered `exec_trace` path on 16 short/medium
  exact-trace rows and 6 long exact-final-state rows.
- The widened control-flow slice now includes static-target non-recursive
  `call` / `ret`, nested helper chains, and call-backed loop bodies.
- This milestone still stays intentionally narrow: it validates the tiny
  boundary, not broader compiled-language claims.
