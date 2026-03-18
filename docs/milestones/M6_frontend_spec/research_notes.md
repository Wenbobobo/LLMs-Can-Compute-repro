# Research Notes

- The first compiled frontend should stress the substrate, not the marketing
  layer.
- A tiny typed bytecode is a better first boundary than a Wasm-like subset
  because it reuses the current DSL semantics and minimizes frontend noise.
- Differential-test clarity matters more than frontend familiarity.
- The type system should be just rich enough to catch obvious lowering errors:
  value-vs-address confusion and branch-flag misuse.
- The first bytecode layer is a verifier and translator problem before it is an
  execution problem.
