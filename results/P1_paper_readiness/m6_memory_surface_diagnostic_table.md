# Memory Surface Diagnostic Table

Current scope: appendix-level D0 diagnostic on the same control-flow-first typed-bytecode slice. This does not widen the compiled-frontend claim boundary.

- Annotated rows: `6`
- Surface verifier passes: `6`
- Surface matches: `6`
- Negative controls: `2`

| Program | Mode | Base exact | Surface verifier | Surface match | Boundary snaps | Max depth | Frame addrs | Heap addrs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bytecode_iterated_helper_accumulator_20_a128_b129 | long_exact_final_state | exact | pass | pass | 40 | 1 | 128|129 | - |
| bytecode_subroutine_braid_long_12_a160 | long_exact_final_state | exact | pass | pass | 24 | 1 | 160|161 | 162|163 |
| bytecode_countdown_helper_call_6_a48 | medium_exact_trace | exact | pass | pass | 12 | 1 | 48 | - |
| bytecode_loop_with_subroutine_update_8_a64_b65 | medium_exact_trace | exact | pass | pass | 16 | 1 | 64|65 | - |
| bytecode_subroutine_braid_6_a80 | medium_exact_trace | exact | pass | pass | 12 | 1 | 80|81 | 82|83 |
| bytecode_call_frame_roundtrip_a192 | short_exact_trace | exact | pass | pass | 2 | 1 | 192 | - |

## Negative controls

| Program | Error class | First error pc | Max depth |
| --- | --- | --- | --- |
| invalid_memory_surface_undeclared_static | undeclared_static_address | 1 | 0 |
| invalid_memory_surface_indirect_escape | undeclared_address_literal | 0 | 0 |

## Scope note

Appendix-level D0 diagnostic only: this preserves the same tiny typed-bytecode control-flow slice and does not introduce a new claim layer.
