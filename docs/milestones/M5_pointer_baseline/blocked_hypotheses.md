# Blocked Hypotheses

- “M5 only needed better target factoring” is not supported.
- “M5 only needed pointer-space labels” is not supported.
- “Opcode-shape fixing is enough to rescue held-out execution” is not
  supported.
- “Opcode-legal exact rollout means the baseline learned execution” is
  explicitly blocked, because that exactness survives even when label accuracy
  remains zero.
