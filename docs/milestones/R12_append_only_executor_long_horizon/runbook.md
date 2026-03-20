# Runbook

## Objective

Reopen the append-only/latest-write executor lane without changing the endpoint.
`R12` should consolidate what is already exact on the current substrate and
make the next harder long-horizon slice explicit before any optional `R13`.

## Inputs

- `results/M4_exact_hardmax_model/free_running_executor.json`
- `results/R3_d0_exact_execution_stress_gate/summary.json`
- `results/R3_d0_exact_execution_stress_gate/claim_impact.json`
- `results/R4_mechanistic_retrieval_closure/summary.json`
- `src/bytecode/datasets.py`
- `src/model/free_running_executor.py`

## Procedure

1. Distill the current exact free-running executor state from `M4`, keeping
   linear, accelerated, and trainable-stack modes separate.
2. Re-read the preserved harder `D0` baseline from `R3` so exact-trace,
   exact-final-state, decode-parity, and precision-companion facts remain
   attached to the reopened lane.
3. Re-read the `R4` mechanistic closure summary to keep the executor story
   framed as latest-write plus local deterministic transition rather than a
   vague “reasoning” claim.
4. Enumerate the currently staged longer-horizon and harder-organization bytecode
   families from `r6_d0_long_horizon_scaling_cases()` and
   `r8_d0_retrieval_pressure_cases()`.
5. Emit one reopened artifact that separates:
   - current exact executor evidence;
   - preserved harder baseline evidence;
   - next harder-slice inventory and failure taxonomy contract.

## Required outputs

- `results/R12_append_only_executor_long_horizon/summary.json`
- `results/R12_append_only_executor_long_horizon/mode_summary.json`
- `results/R12_append_only_executor_long_horizon/horizon_inventory.json`
- `results/R12_append_only_executor_long_horizon/failure_taxonomy.json`
- `results/R12_append_only_executor_long_horizon/claim_impact.json`

## Stop conditions

- Stop green if current exact executor evidence remains exact, preserved harder
  `D0` baselines remain contradiction-free, and the harder-slice inventory is
  explicit enough to decide whether `R13` is needed.
- Stop red if current exactness regresses, if the preserved harder baseline is
  unavailable, or if the next harder slice cannot be stated without widening
  beyond the current endpoint.

## Notes

- `R12` is the main reopened science lane, but this first export remains
  contract-first and artifact-backed.
- A positive `R12` does not by itself authorize broader unseen-family,
  arbitrary-language, or demo-facing claims.
