# Blocked Hypotheses

- “The first frontend should already be Wasm-like.”
  Blocked because that adds frontend surface before the current mechanism is
  closed.
- “The first frontend should define a new richer VM.”
  Blocked because the first bytecode layer should reuse existing `exec_trace`
  semantics and isolate frontend risk from substrate risk.
- “A flashy compiled demo should define the first frontend.”
  Blocked because differential-test clarity matters more than presentation.
- “Calls, returns, locals, and heap must appear in v1.”
  Blocked because they create semantic branches before the typed-bytecode
  verifier and lowering contract are stabilized.
