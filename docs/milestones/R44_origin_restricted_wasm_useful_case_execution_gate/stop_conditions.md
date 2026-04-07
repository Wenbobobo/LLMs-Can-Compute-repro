# R44 Stop Conditions

Stop immediately if any kernel:

- needs an excluded feature from `restricted_wasm_surface.md`;
- breaks exact free-running trace or final-state semantics;
- requires hidden mutable state or a new substrate;
- is swapped out for a different kernel family;
- is only supportable by a trainable model path while exact lowering still
  fails.
