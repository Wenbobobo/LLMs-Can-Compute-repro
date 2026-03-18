# Status

Provisioned on 2026-03-18 while `M6_typed_bytecode_harness` control-flow artifacts are stabilizing.

- scoped the instrumentation burst to the current call/return programs so control-flow widening is not reopened;
- program-level memory layouts now distinguish `frame` versus `heap` cells for the current call/return slice;
- a separate memory-surface verifier now checks declared static addresses, reachable indirect targets, and call-depth-aware alias surfaces without changing the base `M6` exactness contract;
- the follow-up harness now emits deterministic call/ret boundary dumps plus per-access region labels and writes them to `results/M6_memory_surface_followup/`;
- the current export bundle covers 6 annotated programs and 2 negative controls, with `6/6` verifier passes and `6/6` memory-surface matches between bytecode reference execution and the lowered `exec_trace` path.
