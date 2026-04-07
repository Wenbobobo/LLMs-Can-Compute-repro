# Comparator Catalog

`F10` is comparator-first. A richer value family is not scientifically useful
here unless the repo can say what it would be compared against.

| Comparator | Role | Minimum requirement before any later activation | Why it is not activation by itself |
| --- | --- | --- | --- |
| Source semantics comparator | defines the bounded meaning of the richer value family before optimization or lowering | one explicit reference semantics for the candidate family | a reference semantics alone does not justify a runtime lane |
| Lowered interpreter comparator | checks whether the richer family can be represented in the current exact executor style without hidden semantics | one explicit lowering target and invariant set | lowering feasibility alone does not justify scope lift |
| Trace-state comparator | checks whether the richer family is visible in append-only traces or exact final state | one explicit projection from richer values to saved trace or state fields | observability alone does not imply scientific value |
| Boundary / perturbation comparator | checks whether the richer family changes the right thing for the right reason on a named contrastive slice | one predeclared perturbation or boundary case | one perturbation result would still need a later explicit packet |
| External runtime comparator | checks whether a richer family adds anything beyond current source/lowered/executor agreement | only if a later family claims semantic coverage that cannot be judged internally | external comparison without narrow scope can easily outrun the repo's claims |
| Systems comparator | checks whether a richer family creates a new systems-relevant story rather than only a broader semantics story | only after semantic comparators close | systems comparison is downstream and cannot rescue missing semantic discipline |

Additional rule:

- `F9` would need at least the first four comparators on one bounded value
  family before it becomes discussable;
- `F11` would need an additional planner-interface comparator that `F10`
  intentionally does not provide.
