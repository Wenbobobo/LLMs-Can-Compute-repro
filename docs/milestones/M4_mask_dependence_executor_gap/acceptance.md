# Acceptance

This milestone is complete only if it produces an interpretable answer.

Valid closure modes:
- positive closure: a fairer regime than `opcode_legal` materially improves over
  the current `opcode_shape` result on every new held-out family; or
- negative closure: a stable failure taxonomy shows that the staged exactness
  still depends on stronger legality constraints.

Minimum evidence requirements:
- per-family rollout summaries for `structural`, `opcode_shape`, and
  `opcode_legal`;
- first-error diagnostics by step and field;
- at least two harder held-out program families beyond the existing easy slice;
- an explicit stop/go decision on whether any fourth decode regime is justified.
