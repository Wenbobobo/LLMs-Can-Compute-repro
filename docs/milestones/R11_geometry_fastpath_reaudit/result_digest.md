# Result Digest

`R11` re-audited the current exact `2D` geometry fast path and kept the
geometry story narrow: the bounded parity slice remains exact, the standalone
cache benchmark remains strongly positive, and same-endpoint speedup wording
remains blocked.

## What `R11` closed

- reran a bounded current-code parity slice over duplicate-maximizer, tie,
  zero-query, vector-value, and seeded-random cases and kept `5/5` cases
  exact against brute-force;
- distilled the preserved `M2` standalone benchmark as a pure cache-versus-
  brute-force result, with cache speedup ranging from about `42.8x` to
  `249.2x` and median speedup around `171.1x`;
- reattached the geometry discussion to the preserved `R4` mechanistic
  baseline and the negative same-endpoint `R10` cost result;
- made the wording gate explicit: exact geometry remains mechanistically real,
  but it does not support an end-to-end lowered-path speedup claim.

## What `R11` did not do

- did not reopen a broader systems packet or claim same-endpoint runtime
  superiority;
- did not widen the standalone geometry benchmark into a broader compiled or
  headline-level thesis;
- did not activate `R13`, `R14`, or `E1c`.
