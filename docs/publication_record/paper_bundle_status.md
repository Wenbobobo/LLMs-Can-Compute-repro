# Paper Bundle Status

## Mandatory figures

| Item | Status | Notes |
| --- | --- | --- |
| Claim ladder + evidence matrix | ready | Ledgers are synchronized; only paper layout is missing. |
| Staged decode regime comparison | ready | `M4_staged_pointer_decoder` and `M4_mask_dependence_executor_gap` cover the comparison. |
| Provenance-backed staged failure taxonomy | ready | Final plotted layout now exists in `results/P1_paper_readiness/m4_failure_taxonomy_figure.svg`, backed by the canonical taxonomy summary and CSV rows. |
| Real-trace precision boundary | ready | Final plotted layout now exists in `results/P1_paper_readiness/m4_real_trace_boundary_figure.svg`, backed by the canonical boundary summary and CSV rows. |
| Softmax negative-control comparison | ready | Existing `M5` artifacts are stable. |
| Frontend boundary diagram | ready | Final diagram now exists in `results/P1_paper_readiness/m6_frontend_boundary_diagram.svg` and stays explicit about the tiny typed-bytecode scope. |

Narrative-role draft: current main-text figure roles are fixed in
`docs/publication_record/figure_table_narrative_roles.md`.
Caption-ready section notes now live in
`docs/publication_record/section_caption_notes.md`.
Near-prose stubs for `Abstract`, `Introduction`, `Systems gate`, and
`Compiled boundary` now live in
`docs/publication_record/manuscript_stub_notes.md`.
The current sentence-polished manuscript baseline now lives in
`docs/publication_record/manuscript_bundle_draft.md`, and the current
systems-gate placement choice is recorded in
`docs/publication_record/layout_decision_log.md`.
The same near-prose stub set now also covers `Methods`, `Executor branches`,
`Mask dependence`, `Precision boundary`, and `Negative results / threats`.
Caption candidates for the current fixed figure/table set now live in
`docs/publication_record/caption_candidate_notes.md`.
The latest layout/readiness pass is now complete under the current
public-surface and callout audit guards. Main-text artifact pairings stay
fixed, the Methods section stays prose-first, and the systems gate remains
inline rather than promoted to a standalone main-text table. The next
paper-facing work is manuscript-freeze candidacy and release preflight.

## Mandatory tables

| Item | Status | Notes |
| --- | --- | --- |
| Supported vs unsupported claims | ready | Covered by claim ladder plus threats/negative-results ledgers; current main-text layout stays as a separate table paired with the claim-ladder figure rather than one merged artifact. |
| Exact-trace / final-state success table | ready | Canonical machine-readable sources now have a 22-row paper-layout companion in `results/P1_paper_readiness/exact_trace_final_state_table.md`; the same `D0` slice also has an appendix-level memory-surface companion in `results/P1_paper_readiness/m6_memory_surface_diagnostic_table.md`, and a dedicated stress/reference companion now exists under `results/M6_stress_reference_followup/`. This table is ready on the current frozen `D0` scope; broader compiled demos remain blocked unless a later deliberate scope decision explicitly approves widening. |
| Real-trace precision boundary table | ready | Organic bundle plus scaling sweeps now also feed canonical `P1` boundary rows under `results/P1_paper_readiness/`. |
| Threats-to-validity table | ready | Content exists; only wording polish remains. |

Appendix boundary draft: current appendix-vs-main-text split is fixed in
`docs/publication_record/appendix_boundary_map.md`.
Appendix prose and regeneration framing now live in
`docs/publication_record/appendix_stub_notes.md`.
