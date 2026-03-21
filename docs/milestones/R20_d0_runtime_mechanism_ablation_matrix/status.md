# Status

Provisioned on 2026-03-21 as the second experimental lane after `H18`.

- the lane has now landed on the fixed `R19`-derived bounded sample set;
- it stayed on the same endpoint and the same exactness requirements;
- `pointer_like_exact` stayed exact on `16/16` selected rows;
- `pointer_like_shuffled` and `address_oblivious_control` each failed on
  `16/16` selected rows in a claim-relevant way;
- the lane exported runtime, row-level mechanism, and per-read probe artifacts;
- `mechanism_supported` is the landed verdict, and `R21` is the next bounded
  executor-boundary lane.
