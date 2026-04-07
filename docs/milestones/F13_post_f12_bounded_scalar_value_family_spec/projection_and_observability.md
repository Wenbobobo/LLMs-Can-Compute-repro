# Projection And Observability

For this family to count as a real scientific delta, it must remain observable
without hidden mutable side channels.

Required observability surfaces:

| Surface | Required projection |
| --- | --- |
| Append-only trace | every local/flag write must appear as an explicit slot-tagged write event or equivalent deterministic projection |
| Trace-state readback | every local/flag read must be reconstructible as latest-write over the saved slot-tagged history |
| Final state | the final local/flag table must be derivable from the saved trace and must match the reference semantics |
| Boundary probe | at least one bounded contrastive slice must make wrong local/flag handling visible in trace or final state |

Disallowed shortcuts:

- hidden helper metadata that carries the logical current local table outside
  the saved trace;
- opaque compiler annotations that make the scalar values disappear from both
  trace and final-state projections;
- crediting the family as meaningful if it changes only vocabulary but not any
  saved observable.
