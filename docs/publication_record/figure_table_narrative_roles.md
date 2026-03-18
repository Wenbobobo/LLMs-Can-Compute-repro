# Figure and Table Narrative Roles

This file fixes the argumentative role of each current main-text figure and
table so later prose work does not silently widen the claim set.

## Main-text figures

| Item | Narrative role | Must say | Must not say | Primary sources |
| --- | --- | --- | --- | --- |
| Claim ladder + evidence matrix | Defines the paper's actual target and keeps the reader inside the narrowed scope from the start. | The paper is a reproduction-plus-boundary study with explicit supported and unsupported claims. | The repo reproduces arbitrary C, general LLM computation, or a finished systems story. | `docs/publication_record/claim_ladder.md`, `docs/publication_record/claim_evidence_table.md`, `results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json` |
| Staged decode regime comparison | Shows why staged-neural success remains caveated by legality structure. | Structural and `opcode_shape` do not support a fair unconstrained positive claim; `opcode_legal` remains diagnostic. | A fourth fair regime survived the expanded suite. | `results/M4_staged_pointer_decoder/summary.json`, `results/M4_mask_dependence_executor_gap/summary.json` |
| Provenance-backed staged failure taxonomy | Explains that apparent later nontermination is downstream of earlier semantic mistakes. | The provenance follow-up sharpens the negative closure rather than rescuing the staged claim. | `step_budget` is an independent positive/negative signal family. | `results/M4_failure_provenance/summary.json`, `results/P1_paper_readiness/m4_failure_taxonomy_figure.svg` |
| Real-trace precision boundary | States the current `C3e` boundary in one view. | Single-head fails on current exported families; decomposition helps on the validated suite; broader robustness remains unsupported. | The project has a general long-horizon precision robustness result. | `results/R1_precision_mechanism_closure/summary.json`, `results/P1_paper_readiness/m4_real_trace_boundary_figure.svg` |
| Negative-control comparison | Shows that softmax baselines matter because they fail on the relevant exactness target. | Negative controls remain informative precisely because they share the task surface and still fail. | Any learned baseline family is exhausted in principle. | `results/M5_pointer_baseline/training_run.json`, current `M5` ledgers |
| Frontend boundary diagram | Explains why the first compiled step is `D0` and why it stops there. | Tiny typed bytecode is the endpoint on current evidence, not the first step toward arbitrary source-language claims. | `D0` already implies Wasm-like or arbitrary-C coverage. | `results/P1_paper_readiness/m6_frontend_boundary_diagram.svg`, `results/M7_frontend_candidate_decision/decision_summary.json` |

## Main-text tables

| Item | Narrative role | Must say | Must not say | Primary sources |
| --- | --- | --- | --- | --- |
| Supported vs unsupported claims | Makes the paper's restraint explicit and auditable. | Unsupported claims are first-class outputs, not omitted failures. | Unsupported areas are merely deferred engineering work. | `docs/publication_record/claim_ladder.md`, `results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json` |
| Exact-trace / final-state success table | Summarizes what the current `D0` slice actually proves. | The validated slice covers the frozen `D0` boundary and its current companions only. | The current table generalizes to broader compiled demos or arbitrary runtimes. | `results/P1_paper_readiness/exact_trace_final_state_table.md`, `results/M6_stress_reference_followup/summary.json` |
| Real-trace precision boundary table | Gives the exact family/scheme boundary behind the precision figure. | Boundary statements are suite-specific and scheme-specific. | The table establishes universal precision scaling laws. | `results/R1_precision_mechanism_closure/summary.json`, `results/P1_paper_readiness/m4_real_trace_boundary_rows.csv` |
| Threats-to-validity table | Consolidates what remains externally or internally unproven. | Mechanism, systems, and compiled-boundary limitations are distinct. | Mixed systems results can be ignored because the mechanism result is positive. | `docs/publication_record/threats_to_validity.md`, `docs/publication_record/negative_results.md` |

## Caption discipline

- Every caption should begin with the narrow claim it supports on current
  scope.
- Every caption should include at least one boundary clause when the result is
  partial, mixed, or suite-specific.
- No caption should introduce a broader runtime, frontend, or general-LLM
  framing that is absent from the frozen ledgers.
