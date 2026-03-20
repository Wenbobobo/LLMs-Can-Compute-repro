# R10 D0 Same-Endpoint Cost Attribution Design

## Goal

Explain why current same-endpoint decode acceleration does not materially close
the runtime bridge on the fixed `D0` endpoint.

## Intended outputs

- one cost-breakdown table over the current and newly admitted long rows;
- retrieval versus non-retrieval attribution rows;
- one bounded stop/go interpretation.

## Scope lock

- same endpoint only;
- no broader systems benchmark matrix reopen;
- attribution, not rescue.
- representative-row attribution is allowed when full admitted-row exact
  profiling exceeds unattended runtime budget.

## Acceptance

- one table answers where same-endpoint time is actually spent;
- negative attribution remains publishable and explicit.
- the selected attribution set must be justified by a measured runtime budget
  note rather than by convenience alone.
