# TODO

- [x] Define the exact hard-max attention API for latest-write memory retrieval
- [x] Build a minimal causal decode loop that compares linear scan and `HullKVCache`
- [x] Validate the decode loop on exported `exec_trace` memory examples
- [x] Generalize beyond immediate-address memory to a richer addressing mode
- [x] Validate the same bridge on logical stack-slot retrieval
- [x] Train a narrow scorer on reference-generated stack traces
- [x] Evaluate exact success by held-out length bucket for the narrow scorer
- [x] Implement exact free-running rollout with linear and accelerated latest-write retrieval
- [x] Evaluate free-running rollout by length bucket
- [x] Record finite-precision failure ranges for parabolic addressing
- [ ] Replace the fixed candidate-set scorer with a causal learned decode loop
- [ ] Extend learned rollout beyond stack-slot retrieval into mixed memory/stack execution
