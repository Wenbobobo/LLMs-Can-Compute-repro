# R49 Acceptance

`R49` passes as an executed gate only if:

- all widened rows stay inside the preserved useful-case surface;
- exactness rows exist for all `9` planned cases;
- bucket summaries make `bucket_a`, `bucket_b`, and `bucket_c` explicit;
- at least one admitted float32 recovery regime stays exact on `bucket_a` and
  `bucket_b`, otherwise the stop-rule file must flag a practical falsifier;
- comparator-only `R48` evidence is not used as a substitute for exact
  `R46/R47` evidence; and
- the wave stops at `H48` rather than authorizing `F25` directly.
