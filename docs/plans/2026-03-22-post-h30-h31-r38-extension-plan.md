# 2026-03-22 Post-H30 H31 R38 Extension Plan

## Summary

`H30_post_r36_r37_scope_decision_packet` plus the completed clean closeout in
`P17_h30_commit_hygiene_and_clean_worktree_promotion` leave exactly one
scientifically justified compiled-boundary question on the current
append-only / exact-retrieval / small-VM substrate:

can one richer control/call family stay exact without changing the opcode
surface, retrieval substrate, or blocked-lane discipline?

This plan fixes the answer path as:

1. docs-only `H31_post_h30_later_explicit_boundary_decision_packet`;
2. narrow runtime `R38_origin_compiler_control_surface_extension_gate`;
3. refreeze in `H32_post_r38_compiled_boundary_refreeze`;
4. clean-worktree packaging in
   `P18_post_h32_clean_worktree_promotion`.

## Save Rule

Save this plan before execution. Do not use dirty `main` or dirty
`wip/h27-promotion` for this wave.

Work from a clean successor branch created from `wip/p17-h30-clean`. The
default lane is `wip/h31-later-explicit`.

## H31 Contract

`H31_post_h30_later_explicit_boundary_decision_packet` is docs-only.

It must lock the following decisions before any new runtime execution:

- outcome:
  `execute_one_more_tiny_extension`;
- admitted runtime row:
  `subroutine_braid_program(6, base_address=80)`;
- non-admission boundary row:
  `subroutine_braid_long_program(12, base_address=160)`;
- no-go rule:
  no new opcode, no new hidden host evaluator, no new retrieval substrate, no
  softening of `R29/F3`.

Rejected alternatives:

- clarification-only with no runtime execution;
- broader selector/checkpoint or mixed memory/control families;
- arbitrary `C`, wider Wasm, or demo-first widening.

## R38 Contract

`R38_origin_compiler_control_surface_extension_gate` tests exactly one richer
compiled control/call family on the current substrate.

Required evidence for the admitted row:

- verifier pass;
- source/spec contract pass;
- exact source-reference trace and exact final state;
- exact lowered-interpreter trace and exact final state;
- exact accelerated free-running trace and exact final state.

Required evidence for the boundary row:

- run the same checks;
- export mismatch step and failure class if it fails;
- record it as a boundary observation rather than an authorization to widen
  substrate work.

Allowed opcode surface remains:

- `add_i32`
- `call`
- `const_i32`
- `eq_i32`
- `halt`
- `jmp`
- `jz_zero`
- `load_static`
- `ret`
- `store_static`
- `sub_i32`

## H32 Contract

`H32_post_r38_compiled_boundary_refreeze` must freeze the result explicitly.

If the admitted row is exact:

- keep the claim narrow:
  one richer compiled control family is now supported on the current
  Origin-core substrate;
- keep `D1` blocked:
  this is still not arbitrary `C`, not broad compiler support, and not a
  systems claim.

If the admitted row is not exact:

- freeze compiled-boundary work as complete-for-now on the current substrate;
- do not reopen `R29`, `F3`, or any broader compiler lane in the same batch.

## P18 Rule

`P18_post_h32_clean_worktree_promotion` packages only the narrow
`H31/R38/H32/P18` packet and the corresponding current-facing doc sweep.

Use the clean successor worktree directly:

- path:
  `D:/zWenbo/AI/LLMCompute-worktrees/h31-later-explicit`
- branch:
  `wip/h31-later-explicit`

Do not merge back into dirty `main` during this wave.
