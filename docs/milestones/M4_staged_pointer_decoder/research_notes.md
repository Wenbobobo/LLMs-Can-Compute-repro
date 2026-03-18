# Research Notes

- The right comparison was not “pointer decoder vs induced rules”; it was
  “pointer decoder vs direct raw value decoder under the same append-only
  runtime”.
- The new `opcode_shape` regime matters because it separates “strongest legality
  mask rescued the branch” from “candidate-source prediction itself helped”.
- The key positive signal is that `opcode_shape` recovers substantial rollout on
  the harder held-out slice.
- The key negative signal is that held-out structural rollout is still `0.0`,
  so pointer labels alone are not enough.
