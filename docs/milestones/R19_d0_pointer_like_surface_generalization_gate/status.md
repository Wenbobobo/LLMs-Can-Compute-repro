# Status

Provisioned on 2026-03-21 as the first experimental lane after `H18`, and now
closed on a landed runtime packet.

- the lane stayed comparator-bounded and same-endpoint;
- admitted `R17` rows remained the fixed baseline set;
- the admitted-plus-heldout runtime gate is now exported with row-level
  runtime rows, address profiles, cohort/family summaries, and one lane
  verdict;
- `pointer_like_exact` stayed exact on admitted `8/8` plus heldout `16/16`
  rows;
- no repair loop was exercised inside this lane.
