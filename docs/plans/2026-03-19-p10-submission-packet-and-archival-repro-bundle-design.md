# P10 Submission Packet and Archival Repro Bundle Design

## Goal

Turn the current locked checkpoint into a venue-agnostic submission/archive
packet without changing any scientific claim.

## Required outputs

- a canonical submission packet index;
- an archival reproduction manifest;
- a review-facing boundary summary;
- an external release-note skeleton that remains downstream-only;
- one machine-audited `P10` results bundle.

## Audit contract

The `P10` audit should confirm:

- the current active-driver docs point to the locked checkpoint;
- the submission packet names the canonical manuscript, main-text order,
  appendix minimum package, and regeneration sources;
- restricted-source material remains excluded from public-safe docs;
- `P1`, `P5`, and `H2` audits remain green.

## Acceptance

- another engineer can assemble the current paper bundle and appendix package
  from the `P10` packet docs alone;
- all `P10` checks report zero blocked items.
