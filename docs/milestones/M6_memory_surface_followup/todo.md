# Todo

- [x] Finalize code contracts for memory guards without reintroducing new execution regimes.
- [x] Extend the verifier plus translator harness to log heap/stack dumps for every call/ret execution.
- [x] Expand exact-trace runs (short/medium/long) with the new memory diagnostics while freezing control-flow topology.
- [x] Produce `results/M6_memory_surface_followup` JSON/CSV ledgers and publish the diff against the previous `M6` exports.
- [ ] Signal whether the memory instrumentation delta is settled enough for
  `M6_boundary_freeze`.
- [ ] Keep wider frontend expansion blocked until
  `M6_stress_reference_followup` closes.
