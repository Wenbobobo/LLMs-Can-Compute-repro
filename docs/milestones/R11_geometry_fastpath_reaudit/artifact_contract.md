# Artifact Contract

## Result directory

`results/R11_geometry_fastpath_reaudit/`

## Files

- `summary.json`
  - machine-readable top-level decision for the reopened geometry lane
- `parity_rows.json`
  - one row per bounded current-code parity case
- `benchmark_reaudit.json`
  - distilled standalone cache-versus-brute-force benchmark facts from `M2`
- `writing_gate.json`
  - explicit allowed versus blocked geometry wording on the current endpoint
- `claim_impact.json`
  - short claim-facing summary for downstream stage sync
- `README.md`
  - file index only

## Minimum summary fields

- `current_exactness`
  - `parity_case_count`
  - `exact_match_count`
  - `all_cases_exact`
- `benchmark_reaudit`
  - `row_count`
  - `min_cache_speedup_vs_bruteforce`
  - `median_cache_speedup_vs_bruteforce`
  - `max_cache_speedup_vs_bruteforce`
  - `speedup_increases_with_history`
- `mechanistic_baseline`
  - `program_count`
  - `parity_failure_count`
  - `contradiction_candidate_count`
- `same_endpoint_guard`
  - `dominant_exact_component`
  - `median_retrieval_share_of_exact`
  - `median_exact_vs_lowered_ratio`
  - `same_endpoint_fastpath_material`
- `claim_impact`
  - `status`
  - `next_lane`
  - `supported_here`
  - `unsupported_here`
  - `allowed_wording`
  - `blocked_wording`

## Interpretation

- `all_cases_exact == true` means the current bounded parity slice still agrees
  with brute-force on the active codebase.
- `same_endpoint_fastpath_material == false` means the repo may keep
  asymptotic geometry wording, but not convert it into an end-to-end same-endpoint
  speedup claim.
