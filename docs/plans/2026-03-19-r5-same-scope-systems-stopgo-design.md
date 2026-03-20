# R5 Same-Scope Systems Stop-Go Design

## Goal

Run at most one more bounded systems follow-up, and only if the active
`R3/R4` evidence state justifies it.

## Intended outputs

- one `R5` milestone scaffold marked conditional-only by default;
- if activated, one refreshed same-scope runtime matrix over the same `D0`
  comparison surface;
- one bounded decision table answering whether a single follow-up changes the
  current mixed `R2` gate.

## Activation rule

Activate only if:

- `R3` introduces new positive `D0` suites worth re-profiling, or
- `R4` exposes one concrete same-scope bottleneck that can be tested without
  widening scope.

## Acceptance

- either one bounded systems intervention materially changes the current
  same-scope picture, or the repo records a sharper stop/no-go reason and
  refreezes without further systems churn.
