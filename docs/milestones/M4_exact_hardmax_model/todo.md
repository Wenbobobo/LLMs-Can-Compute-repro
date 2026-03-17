# TODO

- [x] Define the exact hard-max attention API for latest-write memory retrieval
- [x] Build a minimal causal decode loop that compares linear scan and `HullKVCache`
- [x] Validate the decode loop on exported `exec_trace` memory examples
- [ ] Generalize beyond immediate-address memory to a richer addressing mode
- [ ] Train on reference-generated traces
- [ ] Evaluate free-running rollout by length bucket
