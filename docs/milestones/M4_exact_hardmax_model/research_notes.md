# Research Notes

- The real point of this milestone is not "make a tiny transformer look like a
  VM" but "show that append-only value recovery can actually run online through
  latest-write retrieval."
- The blog and Discuss files strongly suggest that stack-like state is the
  right proving ground before broader RAM or Wasm claims.
- The geometric claim is only useful if it survives inside a decode loop, not
  only as an isolated lookup primitive.
- Finite precision is a first-class systems risk, especially for parabolic
  address encodings. This risk is strong enough to deserve its own artifact.
