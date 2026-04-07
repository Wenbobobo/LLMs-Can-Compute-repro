# R56 Semantics Contract

- the reference path is a transparent append-only trace-VM interpreter on the
  declared bounded instruction/state contract;
- the candidate path must use the same declared instruction/state contract;
- both paths must produce the same step transitions and the same final state
  on every executed row;
- hidden mutable side state, teacher forcing, and external execution at tested
  runtime are disallowed; and
- any mismatch counts as a falsifier for the bounded free-running mechanism
  claim on the active lane.
