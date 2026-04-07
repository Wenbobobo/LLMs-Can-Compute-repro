# Execution Manifest

The admitted five-row suite is:

1. straight-line arithmetic;
2. counted loop control;
3. latest-write overwrite-after-gap memory;
4. shallow call/return roundtrip; and
5. branch fallthrough revisit.

Each row is evaluated on:

- source bytecode interpreter execution;
- normalized spec execution;
- lowered append-only trace interpreter execution; and
- exact trace plus final-state parity checks.
