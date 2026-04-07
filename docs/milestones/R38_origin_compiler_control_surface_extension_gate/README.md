# R38 Origin Compiler Control Surface Extension Gate

Executed one narrow compiled control-surface extension after `H31`.

`R38` keeps the current Origin-core substrate fixed and tests exactly one richer
control/call family:

- admitted row:
  `subroutine_braid_program(6, base_address=80)`;
- boundary stress row:
  `subroutine_braid_long_program(12, base_address=160)`.

The lane is valid only if the current verifier, lowered interpreter, and
accelerated free-running executor stay exact on the same opcode surface used by
`R37`.
