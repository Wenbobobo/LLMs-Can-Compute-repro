# Allowed Variations

`R46` admits only in-surface changes that keep the landed `R44` kernel family
intact.

Allowed:

- fixed-buffer length shifts inside the same kernel schema;
- base-address relocation on the same static-memory discipline;
- value-distribution changes such as mixed sign, sparsity, density, bimodality,
  skew, or wider bin usage;
- the same declared restricted opcode surface used by landed `R44`.

Not allowed:

- heap memory;
- new kernel families;
- new opcodes or broader control flow;
- unrestricted Wasm or arbitrary `C`;
- frontend translation claims;
- model-side evidence replacing exact execution.
