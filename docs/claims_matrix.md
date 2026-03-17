# Claims Matrix

| Claim | Minimal technical interpretation | Experiment | Status |
| --- | --- | --- | --- |
| A1 | Computation can be encoded as an append-only trace | Reference interpreter plus replay engine agree on final state | started |
| A2 | Useful state can be recovered from bounded trace-local semantics | Trace events expose explicit pops, pushes, branches, and next-PC transitions | started |
| B1 | 2D hard-max retrieval can be implemented exactly | Brute-force reference path over 2D keys/values/queries | implemented |
| B2 | A specialized cache can answer the same retrieval sublinearly | `HullKVCache` query agrees with brute force and benchmarks better than linear scan | implemented, unbenchmarked |
| B3 | Tie handling is part of semantics, not a detail | Exact averaging over equal maximizers, including degeneracies | implemented, unverified |
| C1 | These primitives can support a small exact executor | Tiny stack-machine interpreter and replay engine | implemented |
| C2 | The executor survives long free-running rollout | Future model branch, length-bucket evaluation | unvalidated |
| D1 | A higher-level compiled pipeline can target this substrate | Restricted Wasm-like or tiny C-like compiler path | out of scope for bootstrap |
