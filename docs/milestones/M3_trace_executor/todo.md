# TODO

- [x] Define a tiny stack-machine instruction set
- [x] Implement interpreter and replay engine
- [x] Add deterministic example-program generators
- [x] Add basic correctness tests
- [x] Rename the trace package to avoid the Python stdlib `trace` conflict
- [x] Extend to an initial bounded RAM model with `LOAD/STORE` and latest-write reconstruction
- [x] Extend to runtime dynamic-address RAM with `LOAD_AT/STORE_AT`
- [x] Decide whether `CALL/RET` belongs in `M3` or should wait for a later compiled subset; it moved to the later typed-bytecode compiled subset.
