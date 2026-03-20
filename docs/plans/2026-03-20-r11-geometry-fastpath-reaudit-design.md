# R11 Geometry Fastpath Re-Audit Design

## Goal

Re-audit the exact 2D geometry fast path on the current codebase and current
public wording so the reopened stage starts from real mechanistic footing
rather than stale asymptotic language.

## Why this comes first

The strongest direct mechanistic substrate in the repo is still exact 2D
hard-max retrieval plus Hull-based acceleration. Before pushing longer
execution horizons again, the reopened stage should verify that the current
implementation, benchmark harness, and wording still agree on:

- exactness versus brute-force;
- where fast-path wins are real versus only asymptotic;
- where negative controls fail as expected;
- whether current public wording overstates the current endpoint.

## Expected reads

- `src/geometry/hardmax.py`
- `src/geometry/hull_kv.py`
- `tests/test_geometry_hardmax.py`
- `tests/test_model_exact_hardmax.py`
- `results/R4_mechanistic_retrieval_closure/summary.json`
- `results/R10_d0_same_endpoint_cost_attribution/summary.json`

## Acceptance

- the reopened stage has one fresh geometry/fast-path audit artifact;
- exactness and negative-control behavior remain explicit;
- any fast-path wording kept in public docs is backed by the reopened audit.
