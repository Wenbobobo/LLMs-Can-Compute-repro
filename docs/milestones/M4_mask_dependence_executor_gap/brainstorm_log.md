# Brainstorm Log

- Rejected the “just scale the staged model” idea because it would blur the
  mechanistic question.
- Rejected jumping straight to a Wasm-like frontend because the current gap is
  still inside the staged executor itself.
- Chosen direction: characterize where `opcode_shape` fails, then decide
  whether to stop or add one more narrowly justified decode regime.
