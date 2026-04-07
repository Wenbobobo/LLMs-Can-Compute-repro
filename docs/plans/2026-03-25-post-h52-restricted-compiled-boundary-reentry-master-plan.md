# 2026-03-25 Post-H52 Restricted Compiled-Boundary Reentry Master Plan

## Summary

`H52` remains a correct closeout for the post-`H50` mechanism-only lane. It
shows a real exact substrate through `R55/R56`, but it does not show bounded
fast-path value through `R57`, so that lane should not be widened by
momentum.

This plan therefore still does not reopen `F27`, does not reactivate
transformed or trainable executor entry, does not treat broad Wasm or
arbitrary `C` as an acceptance target, and does not turn "LLMs are computers"
into a live repo claim.

Instead, it saves one new explicit falsification-first lane for a narrower
compiled-boundary question: can one fixed typed stack-bytecode surface be
lowered exactly into the existing append-only trace substrate, and can that
lowered program then execute exactly under the current free-running trace-VM
machinery?

The fixed mainline order is:

`F29_post_h52_restricted_compiled_boundary_bundle` ->
`H53_post_h52_compiled_boundary_reentry_packet` ->
`R58_origin_restricted_stack_bytecode_lowering_contract_gate` ->
`R59_origin_compiled_trace_vm_execution_gate` ->
`H54_post_r58_r59_compiled_boundary_decision_packet`.

The fixed low-priority sidecar is:

`P38_post_h52_compiled_boundary_hygiene_sync`.

## Execution Status

This plan is active only on the clean successor `F29` worktree. It is a new
planning packet above preserved `H52`; it is not an extension of the closed
`F28 -> H51 -> R55 -> R56 -> R57 -> H52` lane.

## Scientific Target

This wave narrows the current scientific target to one explicit chain:

1. one fixed typed stack-bytecode suite can be declared without reopening
   broad frontend claims;
2. that bytecode can be lowered exactly into the existing append-only trace
   instruction substrate;
3. the lowered trace program retains exact source-level trace and final-state
   parity on a transparent interpreter contract; and
4. the same lowered trace program can be executed exactly by the current
   free-running trace-VM executor without hidden mutable side channels.

The strongest claims remain blocked:

- arbitrary `C`;
- broad Wasm coverage;
- general "LLMs are computers";
- transformed-model entry;
- trainable-executor entry; and
- merge back to dirty root `main`.

## Chosen Route

The chosen route is:

- `F29` saves the restricted compiled-boundary claim delta and fixes the only
  admissible order;
- `H53` preserves `H52` while authorizing one compiled-boundary reentry
  through `R58` only;
- `R58` isolates exact lowering from one fixed typed stack-bytecode suite into
  the append-only trace substrate;
- `R59` isolates exact compiled trace-VM execution on the exact `R58` rows
  only; and
- `H54` closes the lane explicitly without raising the broader claim ceiling.

`P38` serves as the operational/docs sidecar that keeps the clean worktree,
artifact policy, `uv` usage, and no-merge posture explicit for this wave.

## F29 Contract

`F29` must remain planning-only and must do five things:

- preserve `H52` as the preserved prior mechanism closeout and preserve `H43`
  as the paper-grade endpoint;
- rewrite the active next question around a restricted compiled-boundary
  contract rather than around transformed or trainable entry;
- fix `H53` as the only follow-up packet;
- fix `R58 -> R59 -> H54` as the only admissible execution order; and
- keep `F27`, `R53`, and `R54` explicitly blocked.

## P38 Contract

`P38` remains operational/docs-only and codifies:

- the clean `F29/H53/P38/R58/R59/H54` worktree as the control and execution
  surface for this wave;
- `uv` as the default execution path for exporters and tests;
- raw row dumps, per-read dumps, and any artifact above roughly `10 MiB` as
  out-of-git by default;
- a separate commit cadence for `F29/H53/P38`, `R58`, `R59`, and `H54`; and
- continued no-merge posture for dirty root `main`.

## H53 Contract

`H53` is docs-only and must make one narrow decision:

- `authorize_compiled_boundary_reentry_through_r58_first`; or
- `keep_h52_terminal_and_stop_before_compiled_boundary`.

The only admissible positive outcome here is
`authorize_compiled_boundary_reentry_through_r58_first`.

That outcome must preserve negative `H52` on fast-path value while recognizing
that the narrower compiled-boundary question has not yet been tested directly
on exact lowering and exact free-running execution.

## R58 Contract

`R58` is the only next runtime candidate fixed here. It must test whether one
fixed typed stack-bytecode suite lowers exactly into the existing append-only
trace substrate.

Required outputs:

- exact source-vs-lowered trace parity;
- exact source-vs-lowered final-state parity;
- exact normalized source-vs-spec parity;
- declared opcode-surface and category coverage;
- first-fail localization; and
- one explicit lane verdict.

If `R58` fails, `R59` and `H54` do not open positively.

## R59 Contract

`R59` runs only after a positive exact `R58`. Its question is whether the
lowered trace programs from `R58` can execute exactly under the current
free-running trace-VM executor on the admitted rows only.

Required comparators:

- transparent source bytecode interpreter execution;
- transparent lowered trace interpreter execution;
- free-running exact linear trace-VM execution; and
- free-running exact accelerated trace-VM execution.

Required outputs:

- exact full-trace parity where applicable;
- exact final-state parity where applicable;
- declared first-fail localization;
- end-to-end latency reporting; and
- one explicit lane verdict.

Teacher forcing, answer-only agreement, or hidden replay do not count as
success.

## H54 Decision Rule

`H54` is docs-only and must read `R58` and `R59` together.

Allowed outcomes:

- `freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value`;
- `stop_before_restricted_compiled_boundary`; or
- `stop_due_to_compiler_work_leakage`.

`H54` must preserve `H43` as the paper-grade endpoint unless a later explicit
packet raises the claim ceiling on stronger evidence than this wave.

## Defaults

- Do not reopen `F27`, `R53`, or `R54`.
- Do not widen into arbitrary `C`, broad Wasm, or demo-first presentation.
- Do not count external execution during tested runtime as internal execution
  evidence.
- Prefer exact equivalence and clear falsifiers over bigger frontends.
- Keep dirty root `main` unmerged and out of scope for scientific execution.
