# Publication Record

This directory is now the paper-first evidence ledger for the repository.
Formal paper text is still evolving, but claim wording, figure/table ownership,
and public-safe evidence mapping should be treated as active rather than
speculative.

Core ledgers:
- `claim_ladder.md` — which claims are validated, partial, negative, or still
  open;
- `claim_evidence_table.md` — concrete artifacts already supporting published
  claims;
- `figure_backlog.md` — reserved future figures and tables;
- `experiment_manifest.md` — reproducibility ledger for unattended runs;
- `threats_to_validity.md` — constraints, caveats, and external-threat notes;
- `negative_results.md` — results that narrow or block claims;
- `paper_outline.md` and `blog_outline.md` — downstream writing structure once
  the evidence stabilizes.

Operating rule:
- every unattended batch that changes a claim boundary, a milestone gate, or a
  future figure/table dependency must update these ledgers in the same batch.
- appendix-level diagnostics that strengthen an existing claim row without
  widening scope should stay tied to that claim and the `P1` paper bundle,
  rather than becoming a new claim layer by default.
- `paper_outline.md` is active planning material for the current paper-first
  workflow.
- `blog_outline.md` remains downstream and currently blocked: `M7` resolved as
  a no-widening decision, so broader blog prose should not outrun the present
  paper-grade endpoint.
