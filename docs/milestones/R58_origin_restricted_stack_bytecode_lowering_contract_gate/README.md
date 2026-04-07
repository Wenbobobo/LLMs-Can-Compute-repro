# R58 Origin Restricted Stack-Bytecode Lowering Contract Gate

Completed runtime gate for the restricted compiled-boundary lowering question.

`R58` tests whether one fixed typed stack-bytecode suite lowers exactly into
the existing append-only trace substrate without reopening broad Wasm or
arbitrary `C`.

The admitted suite is fixed to five rows:

- straight-line arithmetic;
- counted loop control;
- latest-write overwrite-after-gap memory;
- shallow call/return roundtrip; and
- branch fallthrough revisit.

The gate exports exact source-vs-spec parity, exact source-vs-lowered trace
parity, exact source-vs-lowered final-state parity, first-fail localization,
and one explicit lane verdict. `R59` is the only next runtime candidate after
positive exact `R58`.
