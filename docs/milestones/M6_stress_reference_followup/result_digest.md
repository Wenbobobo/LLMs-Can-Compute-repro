# Result Digest

- Implemented bundle:
  `results/M6_stress_reference_followup/summary.json`.
- Exported suite shape:
  `2` medium exact-trace positives,
  `1` long exact-final-state positive,
  `1` typed-branch contract negative,
  `1` memory-surface contract negative.
- Agreement result:
  all three positives match across the current bytecode interpreter,
  the lowered `exec_trace` path,
  and the standalone Python spec interpreter on their declared target;
  both negatives reject with matched contract-level error class and first-error
  location.
- Companion diagnostics:
  the same three positive rows all preserve reference-vs-lowered
  memory-surface agreement, so the follow-up strengthens `D0` without creating
  a new claim layer.
