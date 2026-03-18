# Acceptance

- `M6` does not start until `M4` has a real causal rollout result and `M5`
  exists as a separate comparison branch.
- The first frontend must be a restricted bytecode or Wasm-like subset with
  explicit unsupported features.
- Every compiled example must be checked against an external reference
  interpreter with exact trace or final-state comparison.
- No demo counts as evidence if it hides the compiler/runtime boundary.
