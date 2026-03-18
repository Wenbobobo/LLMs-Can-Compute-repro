# Acceptance

This milestone succeeds if it gives a stable and interpretable answer.

Valid success cases:
- nonzero held-out structural exact rollout; or
- nonzero held-out `opcode_shape` rollout that still survives as a fairer
  comparison than `opcode_legal`; or
- persistent structural and `opcode_shape` failure together with a clear
  explanation of why `opcode_legal` exact rollout is not scientifically
  comparable.

The current checkpoint satisfies the third case.
