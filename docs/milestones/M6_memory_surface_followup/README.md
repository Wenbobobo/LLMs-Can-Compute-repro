# M6 Memory Surface Follow-up

Goal: extend the frozen typed-bytecode harness with systematically instrumented memory surfaces while keeping `M4`/`M5` claims and control-flow contracts untouched.

Scope:

- reuse the stabilized call/ret bytecode and verifier from `M6_typed_bytecode_harness`;
- grow memory typing (heap/stack abstraction, validity checks) without widening the runtime beyond the existing interpreter boundary;
- bake results into the `results/M6_memory_surface_followup` ledger so later phases can reference deterministic data;
- keep the claim ladder limited to `D0`/`C2h`/`C3e` precision metrics and avoid introducing new speculative claims.

Deliverables:

- short/medium/long call/return programs annotated with memory surface diagnostics;
- verifier rules that prove aliasing/heap reachability within the staged runtime;
- a differential perimeter comparing reference traces before and after memory instrumentation;
- a machine-readable ledger (JSON, CSV) describing the precise delta induced by the new diagnostics.

Current artifact bundle:

- `results/M6_memory_surface_followup/summary.json`
- `results/M6_memory_surface_followup/call_boundary_snapshots.json`
- `results/M6_memory_surface_followup/memory_surface_delta.csv`
