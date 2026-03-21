# R16 D0 Real-Trace Precision Boundary Saturation Design

## Goal

Revisit real-trace precision only where same-scope evidence now justifies it:
the admitted, boundary-bearing streams produced by `R15` together with the
preserved `R8/R9` streams.

## Inputs

- `results/R15_d0_remaining_family_retrieval_pressure_gate/summary.json`
- `results/R8_d0_retrieval_pressure_gate/summary.json`
- `results/R9_d0_real_trace_precision_boundary_companion/summary.json`

## Output expectations

- one bounded precision grid over admitted streams only;
- explicit negative controls and failure taxonomy carried forward;
- no open-ended sweep and no broad robustness wording.

## Acceptance

- every screened stream is traceable to an admitted same-scope source row;
- boundary-bearing versus non-boundary-bearing streams are separated cleanly;
- unsupported robustness language remains blocked.
