# R55 Origin 2D Hardmax Retrieval Equivalence Gate

Completed exact runtime gate under active `H51`.

Current status: `completed_with_positive_exact_equivalence_verdict`.

`R55` tests whether the claimed `2D` hard-max retrieval primitive is exactly
equivalent to a transparent reference latest-relevant-state lookup on a fixed
bounded suite. It does not authorize transformed-model entry, trainable entry,
or broader runtime widening.

The landed gate records `retrieval_equivalence_supported_exactly` with:

- `5/5` executed tasks exact on the fixed bounded suite;
- `45/45` read observations exact on value parity and `45/45` exact on
  maximizer-row parity;
- `2` declared tie observations handled exactly under explicit tie semantics;
- `2` duplicate-max observations handled without row-identity collapse; and
- `claim_ceiling = exact_retrieval_equivalence_only`.

The next required packet is
`R56_origin_append_only_trace_vm_semantics_gate`.
