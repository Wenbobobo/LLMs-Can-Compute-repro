# R8 D0 Retrieval-Pressure Gate

Stress the same fixed `D0` endpoint with harder latest-write, stack, and
control retrieval pressure without widening semantics.

The bounded gate is now closed on the current packet: `4/4` harder-family
exact rows remain admitted, the bounded decode-parity probe matches on `2/2`
heaviest admitted rows, and the next handoff stays on `R9/R10` rather than
triggering `E1c`.
