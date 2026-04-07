# R47 Todo

- [x] Fix one exact restricted frontend bridge onto the existing useful-case
  contract rather than introducing a new runtime stack.
- [x] Keep the admissible frontend surface inside bounded `i32`, structured
  loop/branch, and static memory only.
- [x] Reuse the landed `R44/R46` useful kernels and exactness harness rather
  than widening the evidence contract.
- [x] Stop on the first excluded feature, translation ambiguity, or exact
  free-running execution break.
- [x] Export machine-readable artifacts for later explicit `H46`
  interpretation without widening claims here.
