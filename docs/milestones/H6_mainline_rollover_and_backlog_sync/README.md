# H6 Mainline Rollover and Backlog Sync

Goal: switch the active stage from the completed `H4/E1a/E1b/H5` packet to a
new bounded `D0` mainline packet while removing stale backlog ambiguity.

Scope:

- save the full current-round plan in `tmp/`;
- define one canonical `H6/R3/R4/(optional R5)/H7` stage driver;
- synchronize top-level and publication-record entry points to that driver;
- clean dormant historical checklist items so they no longer look active;
- add one machine-readable guard export for the new stage wording.

Non-goals:

- no frontend widening;
- no arbitrary-C or broader runtime claim;
- no new evidence lane execution inside `H6` itself.
