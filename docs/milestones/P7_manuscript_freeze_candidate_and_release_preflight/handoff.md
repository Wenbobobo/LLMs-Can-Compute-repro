# Decision-Complete Handoff

This file tells the next plan-mode or unattended pass how to execute the
freeze-candidate wave without reconstructing intent.

## What is already fixed

- the current claim scope is frozen;
- the main-text figure/table order is fixed;
- the appendix companion boundary is fixed;
- the release-preflight checklist is fixed;
- blog work remains blocked by explicit downstream rules.

## Recommended execution order

### Lane A: manuscript freeze pass

Write set:
- `docs/publication_record/manuscript_bundle_draft.md`
- `docs/publication_record/caption_candidate_notes.md`
- `docs/publication_record/figure_table_narrative_roles.md`
- `docs/publication_record/manuscript_section_map.md`

Task:
- execute one consistency-first freeze polish against the fixed main-text
  artifact order, without changing claim boundaries.

### Lane B: appendix freeze pass

Write set:
- `docs/publication_record/appendix_boundary_map.md`
- `docs/publication_record/appendix_stub_notes.md`
- required appendix companion references under `results/P1_paper_readiness/`

Task:
- ensure the minimum appendix package is complete and clearly separated from
  optional companions.

### Lane C: release-preflight pass

Write set:
- `README.md`
- `STATUS.md`
- `docs/publication_record/release_summary_draft.md`
- `docs/publication_record/blog_outline.md`
- refreshed `results/P5_public_surface_sync/`
- refreshed `results/P5_callout_alignment/`

Task:
- rerun the narrow audits and keep outward wording downstream of the release
  summary.

## Integration gate

Only integrate a freeze/preflight batch after:

1. the three lanes above stop conflicting on claim wording;
2. the narrow `P5` audits are green;
3. `pytest -q` passes;
4. `git diff --check` passes.

## Reopen only if

- a manuscript sentence conflicts with the frozen claim/evidence table;
- a main-text artifact pair no longer matches the section map;
- a required appendix companion is missing for a claim explicitly mentioned in
  the manuscript;
- a new evidence wave is deliberately opened by decision rather than drift.
