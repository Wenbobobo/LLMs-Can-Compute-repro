# Obligation Matrix

Any richer value family must satisfy more than "the executor can carry extra
symbols." This matrix records the minimum scientific obligations before a later
family is even plan-worthy.

| Obligation | Current executor floor | Bounded scalar locals and flags | Typed memory words and records | External effects / planner-mediated values |
| --- | --- | --- | --- | --- |
| Trace projection is explicit | satisfied on the current line | required | required | currently missing |
| Exact retrieval addressability is explicit | satisfied on the current line | required | required | currently missing |
| Executor update rule is closed and deterministic | satisfied on the current line | required | required | currently missing |
| Source-semantics comparator is available | satisfied narrowly through the current source/lowered/free-running chain | required | required | currently missing |
| Trace-state or final-state comparator is available | satisfied narrowly on the current line | required | required | currently missing |
| Boundary or perturbation comparator is predeclared | satisfied narrowly through the current admitted row / boundary-probe logic | required | required | currently missing |
| Systems relevance is stated without headline drift | bounded and still narrow | required | required | currently missing |
| Activation remains downstream of a later explicit packet | satisfied | required | required | required |

Interpretation:

- the current executor floor is the only row already closed by evidence;
- `F10` is about making the second row explicit without pretending that it is
  already implemented;
- the third row is kept downstream of `F10`;
- the last column remains outside the current substrate and therefore outside
  the current same-substrate planning horizon.
