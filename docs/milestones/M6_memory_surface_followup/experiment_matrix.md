# Experiment Matrix

- Inputs: locked call/ret bytecode programs, verifier snapshot from `M6_typed_bytecode_harness`, heap/stack access grid from current interpreter.
- Interventions: memory tagging instrumentation, aliasing invariants, and instrumented export scripts.
- Outputs: precise `heap_diff`/`stack_diff` records per row, verifier pass/fail justification logs, and the new ledgers that show how memory instrumentation shifts exact-final-state comparisons.
