# R2 Systems Baseline Gate

Goal: force a systems-level baseline comparison before any new frontend
widening.

Scope:

- compare linear-scan and specialized retrieval on the same trace families;
- compare typed-bytecode reference/oracle paths against the lowered path on the
  same suites;
- record where asymptotic wins matter and where ordinary interpreter/runtime
  cost still dominates.

Out of scope:

- demo-first throughput claims;
- new frontend work before the gate closes.
