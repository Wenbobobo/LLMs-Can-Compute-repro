# Artifact Contract

## Result directory

`results/R12_append_only_executor_long_horizon/`

## Files

- `summary.json`
  - machine-readable reopened executor summary
- `mode_summary.json`
  - one row per current executor mode and suite bucket
- `horizon_inventory.json`
  - one row per staged `R6` or `R8` long-horizon family case
- `failure_taxonomy.json`
  - bounded failure classes for future `R12` follow-up or conditional `R13`
- `claim_impact.json`
  - short claim-facing summary for stage sync
- `README.md`
  - file index only

## Minimum summary fields

- `free_running_baseline`
  - `mode_count`
  - `all_modes_exact`
  - `countdown_heldout_program_count`
  - `max_exact_heldout_steps`
- `harder_d0_baseline`
  - `exact_suite_row_count`
  - `positive_row_count`
  - `decode_parity_match_count`
  - `boundary_bearing_stream_count`
  - `negative_control_failure_count`
- `mechanistic_baseline`
  - `program_count`
  - `source_observation_count`
  - `parity_failure_count`
  - `contradiction_candidate_count`
- `horizon_inventory`
  - `r6_row_count`
  - `r6_family_count`
  - `r8_row_count`
  - `r8_family_count`
  - `max_r6_horizon_multiplier`
  - `max_r8_horizon_multiplier`
- `claim_impact`
  - `status`
  - `next_lane`
  - `supported_here`
  - `unsupported_here`
  - `followup_contract`

## Failure taxonomy

Future failures should be classified into one of:

- `retrieval_exactness`
- `horizon_budget`
- `trace_organization`
- `precision_boundary`
- `local_transition`

If no failure is observed, keep the taxonomy as a contract rather than
inventing a negative result.
