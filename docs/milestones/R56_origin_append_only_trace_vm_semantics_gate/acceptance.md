# R56 Acceptance

- `R56` remains an exact semantics gate, not a demo sweep;
- the VM contract stays fixed and bounded;
- reference and candidate routes execute the same declared instructions;
- full step-trace parity and final-state parity are both required;
- external execution at tested runtime is disallowed;
- compiler-side replay does not count as internal execution; and
- `R57` does not open unless `R56` is exact.
