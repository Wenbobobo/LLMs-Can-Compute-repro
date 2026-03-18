# Research Notes

- First compiled frontend remains tiny typed bytecode, not Wasm-like and not arbitrary C.
- The translator contract must make verifier-visible type erasure explicit so
  implementation does not silently smuggle extra semantics into lowering.
- The first harness should preserve exact trace rows for short programs because
  they are the cleanest regression oracle.
