# 2026-03-25 Post-H54 Useful-Kernel Stop/Go Design

## Summary

`H54` is a legitimate closeout for the post-`H52` restricted compiled-boundary
lane. It shows that one fixed typed stack-bytecode suite can be lowered
exactly into the current append-only trace substrate and executed exactly by
the current free-running trace-VM machinery. It does not yet show that this
compiled-boundary route reaches a useful-case kernel, and it does not show
bounded value over simpler baselines.

The origin materials and the three saved discussions imply that this is now the
smallest unresolved question that still matters scientifically. If the current
compiled-boundary route cannot carry even one or two preserved useful kernels
without compiler-side leakage or operational collapse, then the strongest
remaining "compiled program inside the model" story should stop here. If it
can, then the project earns one more explicit later packet before any broader
Wasm or `C` rhetoric is revisited.

This design therefore recommends one narrow stop/go successor wave:

`F30_post_h54_useful_kernel_bridge_bundle` ->
`H55_post_h54_useful_kernel_reentry_packet` ->
`R60_origin_compiled_useful_kernel_carryover_gate` ->
`R61_origin_compiled_useful_kernel_value_gate` ->
`H56_post_r60_r61_useful_kernel_decision_packet`

with the low-priority sidecar
`P39_post_h54_successor_worktree_hygiene_sync`.

## Why This Route

Three routes were considered:

1. Recommended: test one minimal useful-kernel carryover and a bounded value
   gate.
2. Reopen a broader compiled useful-case ladder immediately, closer to the old
   `R44` three-kernel surface.
3. Stop now with no further compiled-boundary follow-up.

Route 1 is the best choice because it is the smallest packet that can still
change the scientific conclusion materially. Route 2 is too wide after a wave
that only landed `5/5` toy compiled-boundary rows. Route 3 is defensible, but
it leaves one decisive question unanswered: whether the current exact
compiled-boundary route is merely a toy lowering result or whether it can carry
even the simplest preserved useful kernels under the same exactness rules.

The origin materials are clear on the underlying priority: the project should
prefer the smallest falsifiable experiment over the largest demo, and it should
stop early if exact compiled execution does not survive the first meaningful
useful-case carryover.

## Scientific Target

The next wave should not ask whether arbitrary `C`, broad Wasm, trainable
executors, or transformed executors are possible. It should ask only:

1. can the current exact compiled-boundary substrate carry one minimal useful
   kernel family that is already preserved elsewhere in the repo;
2. can that carryover happen without hiding substantial computation in the
   compiler or exporter; and
3. if exact carryover succeeds, does the route retain any bounded value over
   simpler transparent baselines on the exact admitted rows.

This directly matches the most conservative reading of the origin material:
append-only traces and geometric retrieval might support a useful exact
executor, but the credible target is a narrow neural runtime or coprocessor,
not a general claim that "LLMs are computers."

## Chosen Route

The chosen route is:

- `F30` saves the post-`H54` claim delta and fixes the only admissible order;
- `H55` preserves `H54` while authorizing one useful-kernel carryover reentry
  through `R60` only;
- `R60` tests whether the current compiled-boundary route can carry a fixed
  minimal useful-kernel suite exactly without scope lift;
- `R61` tests whether the exact `R60` rows retain bounded value relative to
  simpler baselines; and
- `H56` closes the lane explicitly as either a minimal positive bridge, a
  value-negative bridge, or a clean stop.

`P39` remains operational/docs-only and keeps the successor worktree, commit
cadence, artifact policy, and no-merge posture explicit for this wave.

## F30 Contract

`F30` must remain planning-only and must do five things:

- preserve `H54` as the active compiled-boundary closeout, preserve `H52` as
  the prior mechanism closeout, and preserve `H43` as the paper-grade
  endpoint;
- rewrite the active next question around minimal useful-kernel carryover
  rather than around broader frontend growth, transformed entry, or trainable
  entry;
- fix `H55` as the only follow-up packet;
- fix `R60 -> R61 -> H56` as the only admissible execution order; and
- keep `F27`, `R53`, and `R54` explicitly blocked.

## P39 Contract

`P39` remains operational/docs-only and codifies:

- the clean `F30/H55/P39/R60/R61/H56` worktree as the only scientific
  execution surface for this wave;
- `uv` as the default execution path for exporters and tests;
- raw row dumps, per-step traces, and any artifact above roughly `10 MiB` as
  out-of-git by default;
- separate commit cadence for `F30/H55/P39`, `R60`, `R61`, and `H56`; and
- continued no-merge posture for dirty root `main`.

## H55 Contract

`H55` is docs-only and must make one narrow decision:

- `authorize_useful_kernel_carryover_through_r60_first`; or
- `keep_h54_terminal_and_stop_before_useful_kernel_reentry`.

The only admissible positive outcome here is
`authorize_useful_kernel_carryover_through_r60_first`.

That outcome must preserve negative `H54` on bounded fast-path value while
recognizing that the current exact compiled-boundary route has not yet been
tested on even the smallest preserved useful kernels.

## R60 Contract

`R60` is the only next runtime candidate fixed here. It must test whether the
current compiled-boundary route can carry a fixed minimal useful-kernel suite
exactly on the current append-only substrate.

The admitted suite should stay smaller than the preserved `R44` three-kernel
ladder and should be fixed up front:

- `sum_i32_buffer`
- `count_nonzero_i32_buffer`

`histogram16_u8` stays out of scope for this first carryover pass.

Required outputs:

- exact source-vs-lowered trace parity;
- exact source-vs-lowered final-state parity;
- exact source-vs-spec parity;
- declared kernel, length, and state-pressure coverage;
- explicit compiler-work leakage accounting; and
- one lane verdict.

If `R60` fails, `R61` and `H56` do not open positively.

## R61 Contract

`R61` runs only after a positive exact `R60` and only on the admitted `R60`
rows. Its question is whether the current compiled useful-kernel route retains
bounded value relative to simpler baselines without hiding costs elsewhere.

Required comparators:

- transparent source execution;
- transparent lowered-trace execution;
- free-running exact linear trace-VM execution;
- free-running exact accelerated trace-VM execution; and
- a plain external reference runtime on the same kernel rows.

Required outputs:

- exactness parity across all admitted routes where applicable;
- end-to-end latency and throughput reporting;
- retrieval-share and trace-length decomposition;
- compiler/export overhead accounting; and
- one explicit lane verdict.

Teacher forcing, pre-expanded answer playback, or compiler-side pre-solving do
not count as success.

## H56 Decision Rule

`H56` is docs-only and must read `R60` and `R61` together.

Allowed outcomes:

- `freeze_minimal_useful_kernel_bridge_supported_without_bounded_value`;
- `authorize_later_compiled_useful_family_packet`;
- `stop_as_compiled_boundary_toy_only`; or
- `stop_due_to_compiler_work_leakage`.

`authorize_later_compiled_useful_family_packet` is admissible only if both
`R60` and `R61` are positive on their declared bounded criteria. Even then, it
must not raise the claim ceiling above `H43` automatically; it authorizes one
later explicit packet only.

## Stop/Go Meaning

This design intentionally makes the next wave decisive.

If `R60` fails, the current compiled-boundary route should be treated as
evidence for toy compiled exactness only, not for useful compiled execution.
If `R60` passes but `R61` is value-negative, the route may still count as a
narrow mechanistic bridge, but it should not be sold as a systems result. If
both pass, the project earns one later explicit packet for a wider useful-case
family; it still does not earn arbitrary `C`, broad Wasm, transformed entry,
or trainable entry.

This means the project is still far from a broad public "LLMs are computers"
claim, but it is only one narrow wave away from a meaningful compiled-route
stop/go decision.

## Defaults

- Do not reopen `F27`, `R53`, or `R54`.
- Do not widen into arbitrary `C`, broad Wasm, or demo-first presentation.
- Do not treat old `R44/H43` useful-case evidence as if it automatically
  validates the current compiled-boundary route.
- Do not count external execution during tested runtime as internal execution
  evidence.
- Prefer early stop on a strong falsifier over a wider follow-on wave.
- Keep dirty root `main` unmerged and out of scope for scientific execution.
