# Todo

- [x] Decide whether `R13` is actually needed after `R11/R12`.
- current decision: `R13` is not currently needed because `R12` exports no
  bounded executor gap that requires a trainable bridge.
- [ ] If needed, select the smallest useful trainable bridge setup.
- [ ] Keep outputs comparator-only rather than claim-bearing by default.
