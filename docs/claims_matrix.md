# Claims Matrix

| Claim | Minimal technical interpretation | Experiment | Status |
| --- | --- | --- | --- |
| A1 | Computation can be encoded as an append-only trace | Reference interpreter plus replay engine agree on final state | validated for current toy programs |
| A2 | Useful state can be recovered from bounded trace-local semantics | Trace events expose explicit pops, pushes, branches, next-PC transitions, and latest memory writes | validated for current stack + bounded RAM programs |
| B1 | 2D hard-max retrieval can be implemented exactly | Brute-force reference path over 2D keys/values/queries | validated on current tests |
| B2 | A specialized cache can answer the same retrieval sublinearly | `HullKVCache` query agrees with brute force and benchmarks better than linear scan | validated for current benchmark sizes |
| B3 | Tie handling is part of semantics, not a detail | Exact averaging over equal maximizers, including degeneracies | validated on current tie tests |
| C1 | These primitives can support a small exact executor | Tiny stack-machine interpreter, replay engine, and bounded RAM latest-write semantics | partially validated |
| C1a | Latest-write memory reads can be rewritten as exact 2D hard-max causal retrieval | Linear scan and `HullKVCache` agree on extracted memory-read events from real traces | validated for immediate and dynamic bounded RAM examples |
| C1b | Stack-slot reads can be rewritten as exact 2D hard-max causal retrieval | Linear scan and `HullKVCache` agree on extracted stack-slot read events from real traces | validated for current stack-machine examples |
| C1c | A narrow trainable scorer can recover latest-write stack retrieval with the same inductive bias | Fit a two-parameter scorer on short countdown stack traces, then evaluate on longer countdown traces and a dynamic-memory stack trace | validated for current toy traces |
| C1d | An online executor can recover value state from append-only latest-write history during rollout | Free-running exact linear and accelerated executors reproduce the reference trace on current stack, branch, and bounded-RAM programs | validated for current toy programs |
| C2 | The executor survives long free-running rollout | Length-bucket evaluation on countdown-style programs and transfer to small branch/memory families | partially validated |
| C2a | A narrow learned retrieval rule can stay exact in free-running rollout on current stack-family programs | Fit on short countdowns, then run the scorer online in held-out countdown, branch, and current bounded-RAM traces | validated for current toy programs |
| C2b | A learned causal executor can generate event decisions online without exact fallback | Future token/event-level model branch | unvalidated |
| C3 | Finite-precision 2D addressing remains stable at practically relevant scales | Quantized parabolic latest-write stress tests across float64/32/bfloat16/float16 | partially validated with clear collapse limits |
| D1 | A higher-level compiled pipeline can target this substrate | Restricted Wasm-like or tiny C-like compiler path | out of scope for bootstrap |
