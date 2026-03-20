# H10 R7 Reconciliation Design

## Goal

Reconcile the completed `R7` packet to the artifact-backed top-`4` profile
result before any new same-endpoint science lane runs.

## Intended outputs

- one saved master plan under `tmp/`;
- refreshed top-level and publication docs with corrected `R7` wording;
- refreshed `R7` / `H9` milestone digests;
- one reconciliation guard export.

## Scope lock

- documentation and audit sync only;
- no new experiments;
- preserve `H8/R6/R7/H9` as completed direct baseline.

## Acceptance

- all public and paper-facing ledgers agree that `R7` preserves the full
  `8`-family admitted surface but profiles only the top `4` heaviest
  representatives;
- historical `H8/R6/R7/H9` wording is corrected without widening claims;
- one machine-readable guard can detect future drift.
