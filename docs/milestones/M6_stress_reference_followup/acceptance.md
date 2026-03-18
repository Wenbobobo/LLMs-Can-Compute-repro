# Acceptance

- the stress family stays inside the current tiny typed-bytecode semantics and
  introduces no new feature class;
- the stress family includes at least one long positive row and one matched
  negative control;
- the planned suite shape is explicit before implementation starts;
- the external reference path is implementation-independent enough that a
  lowering bug and a bytecode-interpreter bug are less likely to fail together;
- the milestone records exactly how mismatches would be classified:
  verifier disagreement,
  trace disagreement,
  final-state disagreement,
  or diagnostic-only disagreement.
- current status: satisfied on the exported `M6-E` bundle, with no mismatch
  rows and no semantic widening beyond the frozen `D0` boundary.
