# R18 D0 Same-Endpoint Runtime Repair Counterfactual Design

## Goal

Keep one comparator/repair lane available for the bounded runtime repair target
that `R17` actually exposed on the same endpoint:
`helper_checkpoint_braid_long/retrieval_total`.

## Inputs

- `results/R17_d0_full_surface_runtime_bridge/summary.json`
- `results/R17_d0_full_surface_runtime_bridge/r18_trigger_assessment.json`
- `results/R17_d0_full_surface_runtime_bridge/focused_attribution_summary.json`
- preserved `R10` representative cost-attribution outputs

## Output expectations

- counterfactual or repair-only comparisons tied to the named
  `helper_checkpoint_braid_long` retrieval bottleneck;
- first probes should stay narrow, for example staged retrieval,
  pointer-like retrieval, or one tighter decomposition-only counterfactual;
- no silent conversion into a new claim-bearing lane.

## Acceptance

- `R18` stays comparator-only even after activation;
- `R18` does not widen beyond the named `helper_checkpoint_braid_long`
  retrieval target unless a later review explicitly says so;
- any outputs remain comparator-only by default;
- same-scope and no-widening rules remain explicit.
