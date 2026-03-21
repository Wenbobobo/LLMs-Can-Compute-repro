# R23 D0 Same-Endpoint Systems Overturn Gate

Landed same-endpoint systems follow-up after `H20`. `R23` tests whether the
landed `pointer_like_exact` runtime can materially improve the current mixed
systems gate on the already validated positive `D0` suites.

Observed outcome:

- all exact-designated paths stayed exact on `25/25` selected positive rows;
- `pointer_like_exact` improved sharply versus imported accelerated;
- the lane still ended at `systems_still_mixed` because
  `pointer_like_exact` remained about `4.16x` slower than the best current
  reference path and still slower than the lowered path on the bounded `R2`
  criterion.
