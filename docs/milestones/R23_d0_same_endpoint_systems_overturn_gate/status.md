# Status

Landed on 2026-03-21 as the systems-focused companion lane to `R22`.

- this lane stays on current positive `D0` suites only;
- it treats `pointer_like_exact` as a first-class runtime candidate rather than
  relying only on the older lowered-path systems gate;
- the landed result is a first-class mixed outcome rather than a softened near-
  positive:
  `lane_verdict = systems_still_mixed`,
  `pointer_like_exact_case_count = 25/25`,
  and `pointer_like_median_ratio_vs_best_reference = 4.1643...`.
