# R42 Acceptance

- retrieval tasks are fixed before execution;
- accelerated retrieval must match brute-force reference exactly;
- duplicate, tie, degenerate, and precision/range cases are included;
- no hidden mutable state or approximate fallback is allowed;
- the gate records exact maximizer-row identity, not value-only agreement;
- `R42` stops below bounded-memory VM execution and restricted-Wasm usefulness.
