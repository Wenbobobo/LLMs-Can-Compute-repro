# R47 Origin Restricted Frontend Translation Gate

Completed exact frontend bridge gate authorized by landed `H45`.

`R47` is not a new runtime stack. It is the narrowest admitted structured
frontend bridge onto the already-landed useful-case contract:

- restricted frontend forms lower instruction-identically onto the existing
  useful-case bytecode kernels;
- execution stays exact on the same bounded useful-case contract rather than
  introducing a new evaluator or new substrate;
- the scope stays below heap allocation, alias-heavy pointers, recursion,
  float, IO, hidden mutable state, and any broader compiler/runtime claim.

The landed gate records `restricted_frontend_supported_narrowly` on `8/8`
held-out useful-case variants across the fixed `3/3` kernel ladder while
keeping `claim_ceiling = bounded_useful_cases_only`.

This wave preserves:

- `H45` as the current active docs-only decision packet above the runtime lane;
- `H44` as the preserved prior route packet;
- `H43` as the current paper-grade endpoint;
- `R46` as the preserved prior post-`H44` exact runtime gate;
- `F21` as the current exact-first planning bundle; and
- `F22` as a blocked future comparator bundle until later explicit `H46`.
