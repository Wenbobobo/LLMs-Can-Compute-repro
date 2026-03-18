# Layout Decision Log

This file records paper-layout choices that affect claim wording, evidence
placement, or later drafting effort.

| Item | Decision | Why | Revisit only if | Primary sources |
| --- | --- | --- | --- | --- |
| `R2` systems gate | Keep as a quantified main-text paragraph in the current draft; do not add a standalone main-text table yet. | The main scientific fact is the mixed gate decision, not a broad positive systems win. A full table would spend scarce main-text space on still-negative timing detail and could overstate the maturity of the systems story. | A later paper-layout pass needs a compact quantitative anchor, or a future systems pass materially changes the gate outcome. | `results/R2_systems_baseline_gate/summary.json`, `results/R2_systems_baseline_gate/runtime_profile_rows.csv`, `results/R2_systems_baseline_gate/baseline_matrix.json` |
| Claim-ladder material | Keep as a paired but separate main-text figure/table set: one orienting claim ladder + evidence matrix, plus one auditable supported-vs-unsupported claims table. | The figure should orient the reader to the narrowed scope, while the table should make the unsupported rows explicit and easy to audit. Merging them would either overload the figure or make the unsupported claims easier to soften or omit. | A later layout pass proves that one compact combined artifact can still keep unsupported claims first-class and visually legible. | `docs/publication_record/claim_ladder.md`, `docs/publication_record/claim_evidence_table.md`, `results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json` |
| Next paper-lane mode | Keep the manuscript bundle as the primary paper-facing artifact, but add a separate short release-summary outline for future public-surface syncs. | The manuscript bundle is now rich enough that repeated compression into `README.md` or `STATUS.md` would create wording churn and scope drift. A short downstream release summary preserves restraint while leaving the paper bundle free to grow. | A later paper version stabilizes enough that the manuscript bundle itself becomes concise enough for release-facing reuse without repeated summarization work. | `docs/publication_record/manuscript_bundle_draft.md`, `docs/publication_record/caption_candidate_notes.md`, `README.md`, `STATUS.md` |

## Promotion rule

If `R2` later needs a table in the main text, it should be a compact gate table
derived from the existing `decision_table` in
`results/R2_systems_baseline_gate/summary.json`, not a wholesale promotion of
the full runtime matrix.
