# R40 Execution Manifest

## Positive Rows

1. admitted row:
   `bounded_scalar_flag_loop_program(6, base_address=320)`
2. boundary row:
   `bounded_scalar_flag_loop_long_program(12, base_address=336)`

## Negative Controls

1. `invalid_bounded_scalar_flag_branch_program(base_address=352)`
   targets non-flag branch operands.
2. `invalid_bounded_scalar_flag_layout_program(base_address=360)`
   targets typed-flag layout mismatch.
3. `invalid_bounded_scalar_heap_escape_program(base_address=368)`
   targets family-scope escape into heap state.

## Required Checks

- `verify_program`
- `validate_program_contract`
- `verify_memory_surfaces`
- source interpreter versus spec reference
- lowered trace versus source trace
- accelerated free-running execution versus lowered trace
