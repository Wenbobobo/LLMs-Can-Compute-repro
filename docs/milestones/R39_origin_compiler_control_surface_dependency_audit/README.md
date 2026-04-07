# R39 Origin Compiler Control Surface Dependency Audit

Executed same-substrate audit after `H33`, now interpreted downstream by
`H34_post_r39_later_explicit_scope_decision_packet`.

`R39` executes one declared control-surface perturbation on the same admitted
row and the same same-family boundary probe used by `R38`:

- baseline rows:
  `subroutine_braid_program(6, base_address=80)` and
  `subroutine_braid_long_program(12, base_address=160)`;
- perturbation rows:
  helper-body permutation with target renumbering on those same two rows.

The lane stays on the same opcode surface as `R37/R38`, keeps the current
Origin-core substrate fixed, and asks one narrow question:

- if helper bodies are relocated and the two call targets are renumbered while
  preserving final semantics, does exact source/lowered/free-running execution
  survive?

On the declared perturbation, the answer is narrowly positive:

- exactness survives on both the admitted row and the named same-family
  boundary probe;
- final state is preserved relative to baseline on both rows;
- trace changes on both rows, so the perturbation is not a no-op.

`R39` remains completed evidence, not a routing change. `H34` interprets the
local positive result as complete-for-now narrow support rather than automatic
authorization for another runtime lane.
