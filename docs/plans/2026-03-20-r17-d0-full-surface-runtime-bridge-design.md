# R17 D0 Full-Surface Runtime Bridge Design

## Goal

Resume same-endpoint runtime measurement only after `R16` has screened the full
admitted same-scope precision surface. `R17` should stop being a partial rerun
of `R7` and instead measure the entire admitted `R8 + R15` runtime surface,
while keeping deeper cost attribution bounded to the smallest subset that can
still name or refuse an `R18` repair lane.

## Inputs

- `results/R8_d0_retrieval_pressure_gate/exact_suite_rows.json`
- `results/R15_d0_remaining_family_retrieval_pressure_gate/exact_suite_rows.json`
- `results/R16_d0_real_trace_precision_boundary_saturation/runtime_bridge_handoff.json`
- `results/R7_d0_same_endpoint_runtime_bridge/summary.json`
- `results/R10_d0_same_endpoint_cost_attribution/summary.json`

## Runtime Surface Contract

- Load the admitted runtime surface from landed `R8` and `R15` exact-suite
  rows, not from the older `R6`-only runtime subset.
- Validate that the loaded surface matches the `R16` runtime handoff:
  `8` admitted rows, `8` families, and the same representative memory-stream
  names.
- Export one runtime bridge row for every admitted program on the same lowered
  endpoint, preserving linear-versus-accelerated exact execution comparison.
- Keep coverage explicit by exporting:
  - one `runtime_surface_index.json`;
  - one `source_surface_runtime_summary.json`;
  - one `family_bridge_summary.json`;
  - one `runtime_bridge_rows.csv`.

## Focused Attribution Contract

- Attribute deeper runtime cost only on two rows:
  - the unique `R16` boundary-bearing stream
    `bytecode_helper_checkpoint_braid_long_180_a312_s0_memory`;
  - the heaviest admitted `R15` row by bytecode step count.
- Reuse the `R10`-style profiled exact executor so retrieval, local transition,
  bookkeeping, and executor overhead stay explicit.
- Keep attribution artifacts bounded:
  - `focused_attribution_selection.json`
  - `focused_attribution_summary.json`
  - `focused_cost_breakdown_rows.csv`

## `R18` Trigger Contract

- `R18` remains inactive by default.
- `R17` may point to `R18` only if it names one bounded same-endpoint repair
  target explicitly.
- The trigger is intentionally conservative:
  - the full-surface bridge must still be open;
  - the worst focused row must also be the worst full-surface runtime row;
  - the focused row must be a sharp outlier versus the other focused row;
  - one dominant component must carry enough of the exact runtime to name a
    local counterfactual.
- If these conditions are not met, `R17` should hand off to
  `H17_refreeze_and_conditional_frontier_recheck`.

## Acceptance

- `R17` exports runtime rows for all `8` admitted families.
- No coverage is implied: source-lane, family, and stream accounting stay
  machine-readable.
- Focused attribution remains bounded to `2` rows.
- `claim_impact.next_lane` is:
  - `E1c_compiled_boundary_patch` only on exactness contradiction;
  - `R18_d0_same_endpoint_runtime_repair_counterfactual` only on an explicit
    bounded repair target;
  - otherwise `H17_refreeze_and_conditional_frontier_recheck`.
- `R17` does not widen to unseen families, broader systems claims, or arbitrary
  compiled-language support.
