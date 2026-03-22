# Execution Manifest

## Scope Lock

- current Origin-core substrate only;
- same opcode surface as `R37/R38` only;
- fixed family only:
  `subroutine_braid_program(6, base_address=80)` and
  `subroutine_braid_long_program(12, base_address=160)`;
- no new opcode, hidden host evaluator, or new program family.

## Comparator Set

The lane is fixed to four rows:

1. admitted baseline:
   `subroutine_braid_program(6, base_address=80)`;
2. admitted perturbation:
   `subroutine_braid_permuted_helpers_program(6, base_address=80)`;
3. boundary baseline:
   `subroutine_braid_long_program(12, base_address=160)`;
4. boundary perturbation:
   `subroutine_braid_long_permuted_helpers_program(12, base_address=160)`.

No fifth row or second perturbation is part of this first execution packet.

## Declared Perturbation

The perturbation is:

- helper-body permutation with target renumbering.

Concrete edit shape:

- swap the two helper bodies at PCs `30-34` and `35-39`;
- renumber the two `CALL` targets so the same final semantics are preserved;
- keep instruction count, opcode surface, loop structure, and dynamic
  call/branch counts unchanged.

This is intended to change compiler-controlled PC/return-address layout while
preserving the same program-level result.

## Required Checks

For every row, export separately:

- verifier pass / fail;
- spec-contract pass / fail;
- source reference exactness;
- source-to-lowering exactness;
- lowered free-running exactness.

For each perturbation row relative to its baseline, export:

- same final state as baseline;
- same trace as baseline;
- first trace divergence step;
- dynamic workload preservation:
  instruction count, step count, call count, branch count, and read counts.

## Stop Rules

- stop and mark dependence detected if the perturbation fails verifier or spec
  contract;
- stop and mark dependence detected if exactness breaks on the admitted row;
- stop and mark boundary sensitivity if the admitted row survives but the
  boundary row does not;
- do not widen to a second perturbation inside this lane.

## Verdict Vocabulary

- `control_surface_dependence_not_detected_on_declared_permutation`
- `declared_permutation_survives_admitted_case_boundary_case_mixed`
- `control_surface_dependence_detected_on_declared_permutation`

## Required Outputs

- `source_case_rows.json`
- `lowering_audit_rows.json`
- `execution_rows.json`
- `comparison_rows.json`
- `failure_rows.json`
- `summary.json`

## Must Stay Explicit

- the perturbation is one declared helper permutation only;
- same final state plus changed trace is the intended comparison target;
- this lane does not authorize arbitrary `C`, broader compiler support, or a
  general LLM-computer claim;
- a later explicit post-`R39` decision packet is still required before any
  routing or scope change.
