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

## Mandatory tables

| Item | Status | Notes |
| --- | --- | --- |
| Supported vs unsupported claims | ready | Covered by claim ladder plus threats/negative-results ledgers. |
| Exact-trace / final-state success table | ready on current scope | Canonical machine-readable sources now have a 22-row paper-layout companion in `results/P1_paper_readiness/exact_trace_final_state_table.md`; the same `D0` slice also has an appendix-level memory-surface companion in `results/P1_paper_readiness/m6_memory_surface_diagnostic_table.md`, and a dedicated stress/reference companion now exists under `results/M6_stress_reference_followup/`. Broader compiled demos remain blocked unless a later `M7` decision explicitly approves widening. |
| Real-trace precision boundary table | ready | Organic bundle plus scaling sweeps now also feed canonical `P1` boundary rows under `results/P1_paper_readiness/`. |
| Threats-to-validity table | ready | Content exists; only wording polish remains. |

Appendix boundary draft: current appendix-vs-main-text split is fixed in
`docs/publication_record/appendix_boundary_map.md`.
