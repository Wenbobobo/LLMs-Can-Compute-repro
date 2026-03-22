# R39 Origin Compiler Control Surface Dependency Audit

Planning-only same-substrate audit authorized by `H33`.

`R39` is the only future runtime candidate named after `H32/H33`. It asks one
narrow question:

- on the current admitted row plus the current same-family boundary probe, how
  much of the observed exactness depends on compiler-side control-surface
  structure versus the current append-only / exact-retrieval / small-VM
  substrate itself?

`R39` must keep the same opcode surface as `R37/R38`, keep the current
Origin-core substrate fixed, and avoid family breadth or scope lift.
