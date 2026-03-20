# Release Preflight Checklist Audit Design

## Goal

Convert the current manual `release_preflight_checklist.md` into one bounded
machine-readable audit so unattended runs can detect outward-sync drift before
any release-facing wording batch is treated as stable.

## Approach

- keep `docs/publication_record/release_preflight_checklist.md` as the human
  checklist for release-facing work;
- add one exporter that reads the current outward-facing docs, the frozen
  paper-facing ledgers, and the standing audit summaries that already guard the
  locked checkpoint;
- require the new audit to verify three things together:
  1. the outward public surface still names the current narrow scope and active
     `H13/V1` governance/runtime stage;
  2. the frozen manuscript, bundle-status, figure-order, appendix-scope, and
     blocked-blog controls still agree;
  3. the existing standing audits remain green, including the current
     `V1` timing classification.

## Scope Lock

- do not open a new science lane or change any scientific claim wording;
- do not replace the existing `P5`, `H2`, `H11`, or `P10` guards;
- do not treat the new audit as proof that the repo is clean for release;
  git-state hygiene remains a separate manual gate.

## Intended Outputs

- one machine-readable checklist with blocked/pass items;
- one snapshot of matched lines from the key release-facing docs;
- one summary that says whether outward docs and standing audits are green on
  the current refrozen checkpoint.

## Acceptance

- the new audit passes on the current `H13/V1` checkpoint-hold state;
- it fails if the outward docs drop the active-stage wording or the current
  bounded runtime classification;
- it leaves one explicit reminder that repo cleanliness still requires manual
  git-state verification before any outward sync commit.
