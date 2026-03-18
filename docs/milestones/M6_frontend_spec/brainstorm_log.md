# Brainstorm Log

- Chose tiny typed bytecode over Wasm-like subset because the current question
  is substrate validity, not frontend familiarity.
- Chose exact differential testing over benchmark theater as the first compiled
  acceptance standard.
- Kept Sudoku / Hungarian style demos out of scope for the first compiled step.
- Kept the first typed layer minimal and verifier-visible instead of inventing
  runtime-only opcodes for every type distinction.
- Reused `exec_trace` lowering as the first execution target so frontend bugs
  and substrate bugs stay separable.
