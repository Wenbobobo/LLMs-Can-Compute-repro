# R34 Origin Retrieval Primitive Contract Gate

Executed first Origin-core primitive gate.

`R34` stops relying on the old compiled-endpoint packaging and instead tests
the minimal retrieval primitives that matter for the Origin thesis directly:

- `latest_write(addr)`;
- `stack_top()`;
- `stack_at_depth(d)`;
- `call_return_target()`;
- exact tie-average semantics for `2D` hard-max retrieval.

The gate stays correctness-first: each primitive keeps a linear oracle, an
accelerated `HullKVCache` path, and machine-readable rows that make it obvious
whether the primitive really holds.
