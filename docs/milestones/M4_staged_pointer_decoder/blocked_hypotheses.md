# Blocked Hypotheses

- “Pointer labels alone are enough” is not supported because held-out
  structural rollout is still `0.0`.
- “Opcode shape alone closes the gap” is not supported because held-out
  `opcode_shape` rollout is still below exact.
- “The current staged result is equivalent to a general neural executor” is not
  supported because `opcode_legal` masks materially constrain the decode space.
