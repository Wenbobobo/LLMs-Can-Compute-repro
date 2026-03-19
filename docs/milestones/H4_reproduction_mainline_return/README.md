# H4 Reproduction Mainline Return

Goal: switch the active stage away from docs-only consolidation and back to the
reproduction mainline, while preserving the current narrow claim boundary and
the locked checkpoint as baseline.

Scope:

- save the full current-round plan in `tmp/`;
- define one canonical return-to-reproduction stage driver;
- synchronize top-level and publication-record entry points to that driver;
- add one machine-readable guard export for the new stage wording.

Non-goals:

- no arbitrary-C widening;
- no frontend widening;
- no conversion of the current narrow claim set into a broad platform thesis.
