# Acceptance

- Exact linear and accelerated online executors must reproduce the reference
  trace exactly on the current stack, branch, and bounded-RAM program families.
- Free-running evaluation must be reported by length bucket, not only as a
  single aggregate number.
- Any learned substitution must be labeled by what it replaces. In the current
  milestone that is stack-slot retrieval only.
- Finite-precision stress results must be recorded explicitly. If a numeric
  format collapses early, that is part of the result.
- This milestone is not accepted as a learned model milestone until a causal
  model generates its own event decisions online rather than scoring fixed
  reference-generated candidate sets.
