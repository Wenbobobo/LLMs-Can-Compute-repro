# H9 Refreeze Sync Design

## Goal

Close the `H8/R6/R7/H9` packet on the same fixed endpoint and leave the repo in
one synchronized state.

## Intended outputs

- refreshed top-level docs;
- refreshed publication ledgers and negative-result/manifest records;
- rerun standing audits and current driver guard outputs;
- final milestone digests for `H8`, `R6`, `R7`, and `H9`.

## Scope lock

- no new experiments beyond standing reruns;
- no scope widening while synchronizing records;
- the packet should end refrozen, not partially open.

## Acceptance

- control docs, ledgers, and standing audits agree on one packet state;
- prior packet remains preserved as completed baseline;
- `pytest -q` and `git diff --check` can run cleanly after sync.
