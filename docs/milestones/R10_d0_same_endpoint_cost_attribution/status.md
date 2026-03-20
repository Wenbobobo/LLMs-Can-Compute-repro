# Status

Opened on 2026-03-20.
Closed on 2026-03-20 with `same_endpoint_cost_attribution_measured`.

- `R10` stayed on representative same-endpoint rows because a full
  component-wise exact attribution on the heaviest `R8` row exceeded `150s`
  without finishing in one local benchmark;
- the selected top-`2` harder `R8` families and their matched admitted `R6`
  source rows closed as `4` profiled rows;
- median exact-versus-lowered runtime remains about `2429.1x`, with median
  retrieval share of exact runtime about `99.8%` and harness share effectively
  negligible;
- all `4/4` profiled rows are dominated by retrieval cost, not by local
  transition, bookkeeping, or harness setup;
- `E1c` stayed inactive and the next lane is `H12`.
