# Research Notes

- The current positive evidence is already strong enough to justify a narrow
  boundary freeze, but not yet a broader frontend claim.
- The most important distinction is between:
  “freeze the boundary” and
  “declare compiled demos ready”.
  These are not the same decision.
- A contradiction should mean one of:
  verifier instability on the frozen suite,
  differential mismatch on the frozen suite,
  memory-surface diagnostics forcing a broader semantic claim,
  or a downstream reference oracle disagreeing on the same frozen slice.

## Explicit contradiction triggers

1. Verifier behavior changes on the frozen suite.
2. Bytecode-reference vs lowered-`exec_trace` agreement breaks on the frozen
   suite.
3. Memory-surface diagnostics require new semantics rather than diagnostic
   metadata.
4. The downstream external reference oracle disagrees on the same frozen slice.

## Handoff rule

- `M6_stress_reference_followup` may start only after the freeze rule and these
  contradiction triggers are written into the milestone docs and publication
  ledgers.
- That follow-up may add exactly one stress family and one external reference
  path, but it may not add new opcodes, new types, recursion, dynamic call
  targets, heap allocation, syscalls, or broader compiled-demo claims.
- Any need for new semantics returns the project to `M6_boundary_freeze`
  instead of silently broadening the frontend claim.
