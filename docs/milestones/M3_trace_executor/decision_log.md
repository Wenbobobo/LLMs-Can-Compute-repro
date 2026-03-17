# Decision Log

- Start with stack semantics before bounded RAM.
- Record explicit pops, pushes, branch decisions, and next-PC transitions in the
  trace events.
- Use immediate-address `LOAD/STORE` as the first bounded RAM step; keep reads
  zero-initialized until a stricter memory model is needed.
