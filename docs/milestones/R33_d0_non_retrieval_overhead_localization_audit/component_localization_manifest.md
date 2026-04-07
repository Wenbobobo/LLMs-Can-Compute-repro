# Component Localization Manifest

## Scope Lock

- current positive `D0` suite only;
- fixed comparator set:
  `spec_reference`,
  `lowered_exec_trace`,
  `pointer_like_exact`;
- no direct `R29` recovery framing inside this lane;
- no widened endpoint, suite, or comparator drift.

## First-Pass Audit Sample

The recommended first execution packet is a stratified `10`-to-`12` row audit
drawn from the same `5` current positive `D0` suites used by `R23`:

- `smoke`
- `loops`
- `memory`
- `control_flow`
- `stress_reference`

Use the following minimum selection rule:

- `2` rows per suite;
- one median `pointer_like_ratio_vs_best_reference` row per suite;
- one worst `pointer_like_ratio_vs_best_reference` row per suite;
- include at least one control-heavy row if the suite offers one.

Escalate from the stratified packet to the full `25` `R23` rows only if
dominant-component rankings remain unstable across suites or if the first-pass
rows fail to isolate one credible non-retrieval bucket.

## Component Targets

The lane should preserve the existing aggregate runtime fields and decompose the
current `pointer_like_exact_non_retrieval_seconds` bucket into bounded
subcomponents that still map back to the aggregate:

- `dispatch_decode_seconds`
- `state_update_bookkeeping_seconds`
- `tensor_python_plumbing_seconds`
- `residual_fixed_overhead_seconds`

At minimum, the final tables must still report:

- exactness on every audited row;
- `retrieval_seconds`;
- total `non_retrieval_seconds`;
- dominant component counts by suite and globally;
- ratio versus `spec_reference` and `lowered_exec_trace`.

## Kill Criteria

- if exactness regresses on the bounded suite, stop and record a stronger
  negative systems result;
- if any apparent gain survives only after dropping `spec_reference` or
  `lowered_exec_trace`, stop and keep `R29` blocked;
- if the lag remains suite-stable after decomposition, stop and reject any
  one-family or one-suite recovery narrative;
- if instrumentation requires widened suites, widened endpoints, or invasive
  code churn that changes the scientific question, stop and record an
  instrumentation blocker instead of widening scope.
- if the first-pass rows preserve exactness and the same non-retrieval bucket
  dominates in every suite, stop without expanding directly to `R29`.

## Verdict Vocabulary

- `non_retrieval_overhead_localized`
- `non_retrieval_overhead_still_aggregate_only`
- `suite_stable_noncompetitive_after_localization`
- `instrumentation_blocked_without_scope_drift`

## Required Outputs

- `component_profile_rows.json`
- `component_profile_rows.csv`
- `suite_component_summary.json`
- `comparator_summary.json`
- `attribution_verdict.json`
- `sample_manifest.json`
- `summary.json`

## Must Be Explicit Before Execution

- the stratified packet remains the first execution step;
- escalation to the full `25` `R23` rows is allowed only if the first-pass
  component signal remains unstable or inconclusive;
- the comparator set stays fixed to `spec_reference`, `lowered_exec_trace`, and
  `pointer_like_exact`;
- the non-retrieval decomposition must map back to the current aggregate timing
  rows rather than replacing them with a different metric family;
- the lane still does not authorize direct `R29` activation by itself.
