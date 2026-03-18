# Research Notes

- The current staged-pointer result is scientifically valuable only if mask
  strength is made explicit.
- `opcode_shape` is the key ablation because it separates “the strongest mask
  solved it” from “candidate-source prediction solved it”.
- The next unattended batch fixes two concrete harder families:
  `flagged_indirect_accumulator` and `selector_checkpoint_bank`.
- The next gain, if any, should come from understanding specific failure modes,
  not from broad model scaling.
- If new held-out families reveal dispersed failures across many fields, the
  likely outcome is a stronger caveat rather than a stronger success claim.
