# R35 Origin Append-Only Stack VM Execution Gate

Executed second Origin-core runtime gate.

`R35` tests whether the current append-only trace substrate plus retrieval
primitives can actually run a small exact stack VM free-running, without hiding
call/return state in a Python-only side channel.

The gate stays on the narrow exact-execution question:

- straight-line arithmetic and overwrite-readback;
- loops and branch/control flow;
- indirect memory;
- nested call/return;
- exact trace and exact final-state criteria kept separate.
