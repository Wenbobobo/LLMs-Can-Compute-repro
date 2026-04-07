# H28 Acceptance

`H28` passes only if:

- one explicit post-`H27` reanchor packet is exported;
- the packet treats `H27` as the closeout of the old same-endpoint recovery
  wave rather than a soft authorization for `R29`;
- the next required order is `R34 -> R35 -> H29`;
- the active claim target is the narrower Origin-core append-only / retrieval /
  small-VM ladder;
- `R29`, `F3`, and `F2` remain blocked or planning-only as appropriate.
