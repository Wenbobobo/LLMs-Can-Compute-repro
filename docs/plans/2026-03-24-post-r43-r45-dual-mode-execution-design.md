# Post-R43 R45 Dual-Mode Execution Design

`R43` is now landed, so the next admissible lane is `R45`.

## Recommended Implementation

Use the narrowest real model lane already supported by the repo:

- keep the `R43` bounded-memory family manifest fixed as the shared contract;
- keep memory retrieval on the landed exact accelerated path;
- model only stack latest-write selection;
- evaluate two admitted modes on the same five-family contract:
  - `compiled_weight_executor`
  - `trainable_2d_executor`

This is the recommended path because it is executable now, does not require
PyTorch, and stays consistent with the exact-versus-model evidence boundary in
`F20`.

## Rejected Broader Alternatives

- full neural event executors as the main `R45` surface:
  too wide, CUDA/torch-dependent, and not needed to satisfy the coequal model
  contract.
- induced-rule or hand-coded transition libraries as the primary `R45` mode:
  too close to exact compiled structure, so the “model” reading becomes weak.
- arbitrary new trainable memory machinery:
  unjustified widening beyond the landed substrate and current code paths.

## Concrete Mapping

- `compiled_weight_executor`
  becomes one analytic quadratic latest-write scorer whose weights are derived
  from the bounded horizon of the fixed `R43` programs.
- `trainable_2d_executor`
  becomes the same scorer family fitted on the four core `R43` families and
  then evaluated on all five families, leaving the optional call/return family
  effectively held out.

## Required Outputs

- `src/model/r45_dual_mode.py`
- `scripts/export_r45_origin_dual_mode_model_mainline_gate.py`
- `tests/test_export_r45_origin_dual_mode_model_mainline_gate.py`
- `results/R45_origin_dual_mode_model_mainline_gate/`
- refreshed `R45` milestone docs
- refreshed control surfaces so the next required packet becomes
  `H42_post_r43_route_selection_packet`
