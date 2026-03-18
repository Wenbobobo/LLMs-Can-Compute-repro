# Research Notes

- Moving from flat tokens to event-level targets was not enough.
- Moving from direct raw event values to pointer-space labels was still not
  enough under the fair structural regime.
- The new `opcode_shape` diagnostic is useful because it shows that even a
  partially fixed event skeleton does not rescue held-out rollout.
- This makes the negative-control story sharper: the issue is not merely
  vocabulary size or tokenization.
