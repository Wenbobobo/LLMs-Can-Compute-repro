# Boundary Probe

The family should be stressable on one bounded contrastive slice, not a broad
new suite.

Recommended bounded slice:

- admitted candidate shape:
  one loop counter `L0` and one branch flag `F0` on the current same-substrate
  executor line;
- boundary probe shape:
  two local slots `L0/L1` plus one branch flag `F0`, where repeated overwrites,
  reuse, and branch-visible comparisons make slot identity and last-write
  observability matter.

Why this is the right probe:

- it is richer than the current floor without requiring typed records;
- it pressures latest-write retrieval, slot identity, and branch visibility;
- it can expose whether the family is scientifically meaningful or only
  compiler-side vocabulary drift.
