# Planning State Taxonomy

This file defines the allowed planning-state labels for the current repo.

## Allowed states

- `active_driver`
  The one document set that defines what the current stage is doing now.
- `standing_gate`
  A persistent checklist or audit definition that must stay green across later
  stages.
- `historical_complete`
  A completed stage plan or milestone that remains useful as rationale but is
  no longer the current driver.
- `dormant_protocol`
  A procedure that is valid only when a named trigger occurs, and is otherwise
  inactive.

## Current assignments

- `docs/publication_record/current_stage_driver.md` — `active_driver`
- `docs/publication_record/release_candidate_checklist.md` — `standing_gate`
- `docs/publication_record/paper_package_plan.md` — `historical_complete`
- `docs/publication_record/conditional_reopen_protocol.md` — `dormant_protocol`

## Operating rule

At any moment, the repo should expose exactly one current `active_driver`.
Later plans may replace it, but should not silently create a second one.
