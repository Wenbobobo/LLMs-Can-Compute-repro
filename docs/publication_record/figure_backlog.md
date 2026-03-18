# Figure Backlog

## Mandatory paper figures

1. Claim ladder and evidence matrix.
   Status: ready.
2. Staged decode regime comparison (`structural` vs `opcode_shape` vs
   `opcode_legal`).
   Status: ready.
3. Per-family failure taxonomy for staged-pointer held-out rollout.
   Status: ready. Final plotted layout now exists in `results/P1_paper_readiness/m4_failure_taxonomy_figure.svg`.
4. Real-trace horizon/base sweep with failure-type annotation.
   Status: ready. Final plotted layout now exists in `results/P1_paper_readiness/m4_real_trace_boundary_figure.svg`.
5. Negative-control comparison for `M5` event-level and pointer-space baselines.
   Status: ready.
6. Frontend boundary diagram: trace DSL -> typed bytecode -> future compiled path.
   Status: ready. Final diagram now exists in `results/P1_paper_readiness/m6_frontend_boundary_diagram.svg`.

## Mandatory paper tables

1. Supported vs unsupported claims.
   Status: ready.
2. Exact-trace and exact-final-state success by family and length bucket.
   Status: ready on current scope; canonical `P1` table rows now have a
   paper-layout markdown table, and the `M6-E` stress/reference bundle remains
   a companion extension rather than a widening trigger.
3. Real-trace precision boundary by stream family and scheme.
   Status: ready in evidence terms, with canonical `P1` boundary rows available for layout/plotting.
4. Threats-to-validity summary.
   Status: ready, pending final wording pass only.

## Optional follow-up figures

1. Precision family catalog for every real-trace stream.
2. Typed-bytecode plus stress/reference regression matrix if the appendix still
   benefits from one compact `D0` overview.

## Optional follow-up tables

1. Memory-surface diagnostic delta for the control-flow-first `D0` slice.
   Status: ready as an appendix-level companion in
   `results/P1_paper_readiness/m6_memory_surface_diagnostic_table.md`.
