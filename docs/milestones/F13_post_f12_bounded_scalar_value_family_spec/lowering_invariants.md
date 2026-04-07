# Lowering Invariants

Any later packet that tries to evaluate this family must preserve all of the
following:

1. same substrate as the current Origin-core line;
2. same opcode surface as the current admitted compiled boundary unless a later
   explicit scope packet says otherwise;
3. no hidden mutable runtime state outside the append-only trace semantics;
4. local and flag reads remain reducible to bounded slot-tagged latest-write
   retrieval, not a new opaque retrieval primitive;
5. lowering preserves the named slot identities and bounded scalar domains;
6. any helper annotations remain eliminable or auditable by a declared
   perturbation comparator.

If any invariant fails, the family no longer qualifies as a bounded same-
substrate continuation and must fall back to blocked scope review.
