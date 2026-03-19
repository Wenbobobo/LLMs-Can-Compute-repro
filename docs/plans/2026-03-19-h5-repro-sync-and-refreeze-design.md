# H5 Repro Sync and Refreeze Design

## Goal

Refreeze the repo after the reproduction-return packet lands by synchronizing
the ledgers, rerunning the standing audits, and recording the new stage output
without reopening broader scope.

## Intended outputs

- one `H5` milestone scaffold;
- refreshed claim/evidence ledgers and experiment manifest;
- refreshed standing-audit results;
- green targeted tests, full `pytest`, and `git diff --check`.

## Acceptance

- the repo returns to one narrow active surface after `H4/E1a/E1b`;
- all standing audits are green on the new driver wording;
- the patch outputs are recorded as bounded evidence, not as a new broad
  program.
