# H8 Driver Replacement Design

## Goal

Replace the refrozen `H6/R3/R4/(inactive R5)/H7` driver with the next
long-horizon packet while preserving the prior packet as a completed baseline.

## Intended outputs

- one saved master plan under `tmp/`;
- one new guard export for stage-alignment drift;
- refreshed top-level and publication control docs naming `H8/R6/R7/H9` as the
  active packet;
- milestone folders for `H8`, `R6`, `R7`, and `H9`.

## Scope lock

- governance/documentation replacement only;
- no evidence widening while the driver is being replaced;
- the prior packet must remain preserved as completed baseline, not deleted.

## Acceptance

- the canonical stage driver names `H8/R6/R7/H9`;
- `README.md`, `STATUS.md`, and publication short docs agree on the new packet;
- a guard export can detect misalignment after future unattended batches.
