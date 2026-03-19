# H3 Stage Driver Consolidation and Plan Index Design

## Goal

Clarify which documents define the current active stage, which are standing
gates, which are dormant protocols, and which are historical-complete plans.

## Why now

`P8`/`P9` closed the submission/release stabilization phase, but several docs
still read like live drivers rather than completed references. Future
unattended work should not have to infer this state from scattered prose.

## Intended outputs

- one canonical current-stage driver document;
- one planning-state taxonomy document;
- one `H3` milestone scaffold with status/todo/acceptance;
- synchronized references from `README.md`, `STATUS.md`, and
  `docs/publication_record/README.md`.

## Acceptance

- exactly one document presents the current active driver;
- `paper_package_plan.md` is framed as a historical-complete stage plan;
- `release_candidate_checklist.md` is framed as a standing gate;
- `conditional_reopen_protocol.md` is framed as a dormant protocol.
