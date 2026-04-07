# Comparator Matrix

| Comparator | What it must answer for this family | Minimum artifact shape |
| --- | --- | --- |
| Source semantics comparator | whether the slot/flag behavior is explicit and bounded before optimization | one small reference semantics for bounded locals and flags |
| Lowered interpreter comparator | whether the family still lowers into the current exact executor style without hidden semantics | one explicit lowering invariant set and one lowered reference path |
| Trace-state comparator | whether the family stays visible in append-only trace and final-state projections | one slot-tagged trace projection plus one final-state projection |
| Boundary / perturbation comparator | whether the family changes the right thing for the right reason on one bounded slice | one predeclared contrastive probe and one perturbation rule |
| External runtime comparator | optional later check only if internal comparators cannot decide scientific value cleanly | only downstream of the first four comparators |

Rule:

- a later explicit packet may not skip directly to the external runtime
  comparator;
- the first four comparators must already be satisfiable on one bounded family
  before any later `F9` or `F2` discussion becomes plan-worthy.
