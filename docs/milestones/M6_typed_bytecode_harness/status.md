# Status

Implemented on 2026-03-18.

- `src/bytecode/` now contains the frozen v1 IR, verifier, lowering path,
  reference interpreter, starter datasets, and differential harness.
- The current control-flow-first export batch validates:
  - 22 verifier-passing rows,
  - 7 deterministic verifier failures,
  - 16 short/medium exact-trace matches,
  - 6 long exact-final-state matches.
- The widened `M6` surface now includes static-target non-recursive `call` /
  `ret`, nested call chains, branch-then-call programs, and call-backed loop
  helpers without widening to a broader compiled frontend claim.
