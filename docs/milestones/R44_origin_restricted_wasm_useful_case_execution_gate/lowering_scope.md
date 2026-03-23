# R44 Lowering Scope

The allowed future lowering surface is the one fixed in
`restricted_wasm_surface.md`.

The future gate must:

- lower only the fixed useful kernels;
- keep all state reconstruction inside the append-only trace plus declared
  retrieval rules;
- compare against a reference interpreter for every kernel;
- treat any later trainable or translated model executor as comparator-only
  until exact lowering survives.
