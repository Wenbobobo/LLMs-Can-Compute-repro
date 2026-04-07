# R34 Acceptance

`R34` passes only if:

- all primitive rows are exported in machine-readable form;
- each audited primitive keeps exact agreement between the linear oracle and
  `HullKVCache`;
- tie-average semantics are tested explicitly rather than assumed;
- call/return target retrieval is represented as a real append-only retrieval
  primitive, not just a prose claim;
- the next priority lane becomes `R35_origin_append_only_stack_vm_execution_gate`.
