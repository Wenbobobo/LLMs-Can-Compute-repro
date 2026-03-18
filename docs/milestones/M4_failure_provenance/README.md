# M4 Failure Provenance

Goal: explain the cleaned staged-pointer failures mechanistically after `C2h`
closed negative, without reopening model-capacity or decode-ladder exploration.

This milestone does not train a new model and does not add a fourth regime. It
uses the existing staged export plus replay diagnostics to answer a narrower
question:

- which failures are first semantic mistakes;
- which `step_budget` rows are downstream symptoms of earlier mistakes;
- whether any supposedly non-attributable failures remain after provenance is
  reconstructed.

Frozen scope:
- fixed checkpoint and fixed decode ladder:
  `structural`, `opcode_shape`, `opcode_legal`;
- fixed expanded held-out suite already used in `M4-D`;
- no new label space, no new mask family, no capacity rescue.
