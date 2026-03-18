# Harness Contract

## Differential comparisons

Each harness row compares:
- bytecode reference interpreter output;
- lowered `exec_trace` interpreter output;
- optional later execution branch output when explicitly enabled.

## Frozen result schema

- `program_name`
- `suite`
- `comparison_mode`
- `trace_match`
- `final_state_match`
- `first_divergence_step`
- `failure_class`
- `failure_reason`

## Comparison modes

- `short_exact_trace`
  Requires exact trace and exact final state.
- `medium_exact_trace`
  Requires exact trace and exact final state.
- `long_exact_final_state`
  Requires exact final state. If trace diverges, the harness still records
  `first_divergence_step`, `failure_class`, and `failure_reason`.

## Failure classes

- `verify_error`
- `lowering_mismatch`
- `trace_divergence`
- `final_state_divergence`
- `runtime_exception`

The harness may add more specific subclasses later, but these five remain the
top-level categories.
