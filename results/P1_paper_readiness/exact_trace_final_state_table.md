# Exact Trace / Final State Table

Current scope: current `D0` typed-bytecode families only. This table is ready
for the current paper scope; broader compiled families remain intentionally
blocked rather than “missing.”

- Total rows: `22`
- Exact-trace matches: `22`
- Exact-final-state matches: `22`
- Verifier-passing rows: `22`
- Companion `M6-E` positives outside this table: `3`

| Program | Suite | Length | Target | Verifier | Bytecode instr | Lowered instr | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bytecode_iterated_helper_accumulator_20_a128_b129 | control_flow | long | exact final state | pass | 21 | 21 | exact |
| bytecode_subroutine_braid_long_12_a160 | control_flow | long | exact final state | pass | 40 | 40 | exact |
| bytecode_countdown_helper_call_6_a48 | control_flow | medium | exact trace | pass | 15 | 15 | exact |
| bytecode_loop_with_subroutine_update_8_a64_b65 | control_flow | medium | exact trace | pass | 21 | 21 | exact |
| bytecode_subroutine_braid_6_a80 | control_flow | medium | exact trace | pass | 40 | 40 | exact |
| bytecode_accumulator_12 | loops | long | exact final state | pass | 19 | 19 | exact |
| bytecode_checkpoint_replay_long_8_a96 | loops | long | exact final state | pass | 70 | 70 | exact |
| bytecode_indirect_counter_bank_12_a32_b33 | loops | long | exact final state | pass | 26 | 26 | exact |
| bytecode_stack_memory_braid_8_a64 | loops | long | exact final state | pass | 45 | 45 | exact |
| bytecode_alternating_memory_loop_6_a16 | loops | medium | exact trace | pass | 37 | 37 | exact |
| bytecode_countdown_6 | loops | medium | exact trace | pass | 10 | 10 | exact |
| bytecode_selector_checkpoint_bank_6_a32 | loops | medium | exact trace | pass | 70 | 70 | exact |
| bytecode_dynamic_latest_write | memory | medium | exact trace | pass | 9 | 9 | exact |
| bytecode_indirect_memory_roundtrip | memory | short | exact trace | pass | 6 | 6 | exact |
| bytecode_static_memory_roundtrip | memory | short | exact trace | pass | 4 | 4 | exact |
| bytecode_arithmetic_smoke | smoke | short | exact trace | pass | 4 | 4 | exact |
| bytecode_branch_then_call_false | smoke | short | exact trace | pass | 13 | 13 | exact |
| bytecode_branch_then_call_true | smoke | short | exact trace | pass | 12 | 12 | exact |
| bytecode_call_add_halt | smoke | short | exact trace | pass | 6 | 6 | exact |
| bytecode_call_chain_smoke | smoke | short | exact trace | pass | 10 | 10 | exact |
| bytecode_eq_branch_false | smoke | short | exact trace | pass | 8 | 8 | exact |
| bytecode_eq_branch_true | smoke | short | exact trace | pass | 8 | 8 | exact |

## Scope note

Current scope covers the current typed-bytecode paper boundary. The dedicated
`M6-E` stress/reference bundle remains a companion extension, and later
compiled frontend families are blocked unless a future frontend decision
explicitly widens scope.
