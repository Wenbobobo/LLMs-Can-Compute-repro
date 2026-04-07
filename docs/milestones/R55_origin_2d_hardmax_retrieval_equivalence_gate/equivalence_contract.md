# R55 Equivalence Contract

- the reference path is a transparent latest-relevant-state lookup over the
  declared append-only history only;
- the candidate path is the claimed `2D` hard-max retrieval implementation on
  the same query inputs;
- both paths must return the same value and the same maximizer-row identity on
  every declared read;
- tie handling must be fixed explicitly and tested rather than treated as an
  incidental floating-point artifact; and
- any mismatch counts as a falsifier for the fast-path retrieval claim on the
  active mechanism lane.
