# R47 Acceptance

- the gate remains exact-first rather than demo-first;
- the bridge reuses the existing useful-case bytecode kernels and exactness
  contract instead of introducing a fresh runtime stack;
- allowed frontend forms stay bounded to structured integer useful cases with
  static memory only;
- excluded features remain explicit: no heap, no alias-heavy pointers, no
  recursion, no float, no IO, and no hidden mutable state;
- `translation_identity_match = true` on all `8/8` admitted rows;
- outputs stay machine-readable enough for later explicit `H46` review; and
- no broader Wasm/C, hybrid model work, or merge posture is authorized here.
