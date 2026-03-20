# R4 Mechanistic Retrieval Closure

Goal: show that successful `D0` execution on the current positive suites can be
explained by a small fixed set of retrieval primitives on the same endpoint.

Current state:

- completed on the current positive `D0` suites with `32` programs covered;
- all exported source events are explainable by latest-write, stack, control,
  or deterministic local-transition primitives;
- linear versus accelerated Hull retrieval stays exact on all `4290`
  source-event observations;
- `R5` is not justified on the current scope, and `E1c` remains inactive.

Scope:

- map positive rows back to latest-write, stack, control, or deterministic
  local transition classes;
- require source-event agreement between `linear` and `Hull` retrieval;
- keep staged-pointer and provenance artifacts diagnostic-only.

Non-goals:

- no frontend widening;
- no baseline rescue work by default;
- no systems claim widening.
