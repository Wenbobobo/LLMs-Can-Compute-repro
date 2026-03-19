# Decision-Complete Handoff

## What is already fixed

- the current claim scope is frozen;
- the main-text order is fixed;
- the appendix companion boundary is fixed;
- `P1` and `P5` audits already guard public-surface and callout drift;
- `H2` is the standing hygiene/audit lane for post-`P7` governance.

## Recommended execution order

### Lane A: manuscript lock

Write set:
- `docs/publication_record/manuscript_bundle_draft.md`
- `docs/publication_record/caption_candidate_notes.md`
- `docs/publication_record/figure_table_narrative_roles.md`
- `docs/publication_record/manuscript_section_map.md`

Task:
- execute one consistency-first lock pass without changing claim boundaries or
  main-text artifact ownership.

### Lane B: appendix minimum-package lock

Write set:
- `docs/publication_record/appendix_boundary_map.md`
- `docs/publication_record/appendix_stub_notes.md`
- required appendix companions under `results/P1_paper_readiness/`

Task:
- ensure every required companion is present and optional companions stay
  clearly non-blocking.

### Lane C: ledger lock

Write set:
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/claim_evidence_table.md`
- `docs/publication_record/negative_results.md`
- `docs/publication_record/threats_to_validity.md`
- `docs/publication_record/paper_bundle_status.md`

Task:
- keep the frozen endpoint explicit across claims, caveats, and blocked rows.

## Integration gate

Only integrate a `P8` batch after:

1. no claim wording conflict remains across the three lanes;
2. `P1`, `P5`, and `H2` audits are green;
3. `pytest -q` passes;
4. `git diff --check` passes.
