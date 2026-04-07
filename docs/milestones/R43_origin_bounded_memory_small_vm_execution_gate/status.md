# R43 Status

- completed bounded-memory small-VM exact gate after the landed `H41/P27`
  control stack;
- validates five fixed bounded-memory families spanning loops, branching,
  checkpoint/reuse memory, stack-depth revisits, and one gated single-call /
  return accumulator;
- keeps source/spec, source/lowered, and accelerated free-running trace plus
  final-state exactness mandatory;
- records `5/5` exact families, including `4/4` exact core families before the
  gated optional call/return family executes; and
- does not authorize useful-case widening, heap-region admission, or model
  evidence as a substitute for exact evidence.
