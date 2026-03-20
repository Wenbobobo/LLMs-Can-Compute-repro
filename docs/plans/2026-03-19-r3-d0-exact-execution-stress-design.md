# R3 D0 Exact Execution Stress Design

## Goal

Test whether the current exact executor remains exact on a bounded but harder
`D0` suite without widening frontend scope.

## Intended outputs

- one `R3` milestone scaffold;
- one bounded stress suite covering longer control flow, deeper stack-memory
  interleaving, and longer indirect-memory horizons;
- exact-trace, exact-final-state, first-mismatch, and failure-reason outputs;
- precision follow-up only on newly boundary-bearing rows, using the current
  `single_head`, `radix2`, and `block_recentered` schemes plus one weaker
  negative control.

## Scope lock

- current `D0` endpoint only;
- no new frontend, language, or runtime widening;
- no open-ended precision sweep program;
- only true endpoint contradictions may route to `E1c`.

## Acceptance

- either the new suite stays exact on the frozen endpoint, or failures are
  clearly typed as finite-precision, unsupported-mode, or true `D0`
  contradictions;
- the exporter keeps `linear` and `Hull` decode parity explicit on the tested
  rows;
- negative/control rows clarify boundary logic rather than broadening claims.
