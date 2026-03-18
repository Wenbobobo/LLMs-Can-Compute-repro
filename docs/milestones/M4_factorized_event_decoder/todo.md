# Todo

- Try one staged decoder that predicts structure first and values second.
- Test whether pointer-like value heads reduce the `push_value_0` error rate.
- Compare bounded next-PC heads against relative-PC heads.
- Re-run rollout on the same train/held-out families after each structural
  change; do not expand task families before rollout improves.
