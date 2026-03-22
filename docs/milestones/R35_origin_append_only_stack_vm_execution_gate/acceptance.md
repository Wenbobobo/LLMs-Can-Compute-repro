# R35 Acceptance

`R35` passes only if:

- the exported case bundle includes straight-line, loop, indirect-memory, and
  call/return coverage;
- the retrieval-backed executor stays exact on both trace and final state across
  the bundle;
- call/return coverage produces real retrieval-backed call-space reads;
- any failure is exported as a trace-level failure row rather than hidden in a
  summary average.
