# Acceptance

This milestone is counted as passed only for the narrower staged claim:

- the pointer-space decoder must outperform the raw event-value decoder on
  free-running rollout;
- `opcode_legal` staged rollout must be exact on the exported held-out slice;
- weaker decode regimes must also be recorded so the contribution of stronger
  legality masks stays visible;
- the held-out slice must include at least one harder mixed-memory family,
  rather than only the earlier countdown and simpler branch programs.

This milestone does **not** by itself prove a stronger neural executor claim.
