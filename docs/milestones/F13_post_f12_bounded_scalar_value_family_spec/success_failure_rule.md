# Success Failure Rule

This bundle does not run the family. It defines how a later bounded packet
would be judged.

Success means:

- the bounded family remains explicit at source, lowering, trace, and final
  state levels;
- the first four comparators in `comparator_matrix.md` can all be stated
  without widening scope;
- the family can be pressured on the named boundary probe without requiring
  richer value structures.

Failure means:

- the family only changes helper vocabulary while disappearing from trace and
  final-state observables;
- the family requires hidden helper state that the current append-only line
  cannot inspect;
- the family immediately forces typed records, symbolic refs, external effects,
  or a new opcode surface;
- the family cannot be separated from broader semantic-boundary rhetoric.
