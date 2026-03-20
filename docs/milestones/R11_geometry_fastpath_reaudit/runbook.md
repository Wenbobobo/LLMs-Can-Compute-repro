# Runbook

## Objective

Re-audit the exact `2D` hard-max fast path on the current codebase without
widening past the narrow mechanism target. `R11` should answer two questions:

1. does the current bounded parity slice still match brute-force exactly; and
2. what fast-path wording remains justified once same-endpoint runtime costs
   are kept in view.

## Inputs

- `results/M2_geometry_core/benchmark_geometry.json`
- `results/R4_mechanistic_retrieval_closure/summary.json`
- `results/R10_d0_same_endpoint_cost_attribution/summary.json`
- `tests/test_geometry_hardmax.py`
- `tests/test_model_exact_hardmax.py`

## Procedure

1. Re-run one bounded parity slice on the current geometry stack using the
   same tie, duplicate-maximizer, zero-query, vector-value, and seeded-random
   cases already represented in the current tests.
2. Re-read the stored standalone geometry benchmark and distill only
   cache-versus-brute-force claims.
3. Re-read the current same-endpoint cost attribution artifact and keep the
   wording gate explicit: retrieval can be mechanistically real while still not
   constituting an end-to-end runtime win over the lowered path.
4. Re-anchor the geometry wording to the broader `R4` mechanistic baseline so
   the fast-path discussion stays attached to exact latest-write retrieval
   rather than becoming a detached benchmark talking point.

## Required outputs

- `results/R11_geometry_fastpath_reaudit/summary.json`
- `results/R11_geometry_fastpath_reaudit/parity_rows.json`
- `results/R11_geometry_fastpath_reaudit/benchmark_reaudit.json`
- `results/R11_geometry_fastpath_reaudit/writing_gate.json`
- `results/R11_geometry_fastpath_reaudit/claim_impact.json`

## Stop conditions

- Stop green if the bounded parity slice remains exact and the writing gate
  still blocks end-to-end speedup wording.
- Stop red if current parity breaks, if the stored benchmark is missing, or if
  public wording would need a claim not backed by `M2/R4/R10`.

## Notes

- `R11` is a re-audit over existing exact substrate, not a new systems packet.
- A positive `R11` still does not authorize broader same-endpoint performance
  claims or compiled-facing widening.
