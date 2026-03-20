# Decision Gate

## Purpose

`H15` is the first refreeze after the `H14` reopen. It should record one
explicit decision from `R11/R12` and any justified conditional follow-up, not
leave the lane semi-open.

## Required inputs

- `results/H14_core_first_reopen_guard/summary.json`
- `results/R11_geometry_fastpath_reaudit/summary.json`
- `results/R12_append_only_executor_long_horizon/summary.json`
- optional `results/R13_small_model_executor_reactivation/summary.json`
- optional `results/R14_bounded_compiled_probe/summary.json`
- standing outward-sync and bundle-lock audits

## Decision table

### Direct refreeze

Use `H15` directly if:

- `R11` keeps bounded geometry parity exact;
- `R11` keeps same-endpoint fast-path wording explicitly bounded;
- `R12` keeps current executor evidence exact and the harder-slice inventory
  explicit enough that no bounded bridge is needed;
- no contradiction or widening trigger appears in standing guards.

### Conditional `R13`

Activate `R13_small_model_executor_reactivation` only if:

- `R11` is green;
- `R12` leaves one bounded executor gap that is plausibly localized to the
  stack-read bridge rather than to endpoint scope, precision collapse, or a
  broader trace-representation failure.

### Conditional `R14`

Activate `R14_bounded_compiled_probe` only if:

- `R11` and `R12` are already landed;
- any optional `R13` has already clarified the executor picture or been
  explicitly waived;
- the probe remains inside tiny typed-bytecode `D0`.

## Required H15 outputs

- synchronized root/publication wording
- one explicit next-stage decision
- preserved blocked claims and no-widening constraints

## Explicit non-goals

- no silent escalation from bounded `D0` evidence to broader compiled-language
  claims
- no paper/blog language that outruns the current artifact set
