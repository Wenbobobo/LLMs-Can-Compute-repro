# 2026-03-22 Post-R36 Explicit Next-Wave Design

## Summary

`H29` and `R36` close the current Origin-core wave in a scientifically useful
state:

1. append-only traces remain exact on the active narrow substrate;
2. exact `2D` hard-max retrieval remains exact on the active primitive suite;
3. the small append-only stack/VM executor remains exact on the active bundle;
4. float32 `single_head` precision does not scale monotonically on inflated
   horizons, while bounded decomposition schemes recover the exported failing
   rows.

That is enough to justify one new explicit planning packet. It is not enough to
justify automatic scope lift.

## Immediate Rule

Save this plan before any new execution.

Do not activate `R37` from momentum, from a passing `R36`, or from old `D0`
plans. The next execution wave must begin from a clean worktree and only after a
later explicit authorization packet chooses to spend time on a compiled/lowered
boundary.

## Recommended Next Order

1. Preserve `H29` as the current active routing packet.
2. Preserve `R34`, `R35`, and `R36` as the frozen Origin-core evidence base.
3. Keep `R29`, `F3`, and broader outward claims blocked.
4. Use this document plus the `R37` and `H30` milestone skeletons as the only
   authorized planning surface for the next wave.
5. If and only if a later explicit packet reauthorizes it, execute:
   `R37_origin_compiler_boundary_gate` ->
   `H30_post_r36_r37_scope_decision_packet`

## Why `R37` Is Conditional

Two tempting but wrong conclusions must be avoided:

- `R36` does not show broad long-horizon robustness. It shows a narrow,
  suite-bounded failure-and-recovery pattern.
- `R35` does not show arbitrary compiled-program coverage. It shows exactness on
  the current narrow stack-VM bundle.

Therefore the next reasonable question is not "does the repo already support a
compiler?" but "is there one tiny lowered boundary that can be tested honestly
on the current substrate without smuggling back the old same-endpoint story?"

## `R37` Contract

`R37_origin_compiler_boundary_gate` should stay narrow and falsifiable.

Allowed target:

- one tiny lowered source fragment only;
- direct lowering into the current append-only stack-VM instruction surface;
- no hidden host evaluator, no hidden Python-only control stack, and no extra
  runtime substrate outside the current active bundle.

Recommended source fragment:

- integer constants and addition/subtraction;
- equality or less-than branch;
- bounded `while` or counted loop;
- at most one narrow local-variable lowering scheme;
- optional straight-line helper lowering only if it compiles into existing
  `CALL/RET` semantics already validated by `R35`.

Required rows:

- hand-written source program;
- lowered stack-VM program;
- reference source-level result;
- lowered-program interpreter result;
- free-running exact executor result;
- exact-trace and exact-final-state criteria kept separate.

No-go triggers:

- any need to widen the opcode surface materially;
- any mismatch that can only be fixed by reintroducing hidden side channels;
- any pressure to relabel the result as same-endpoint systems recovery;
- any attempt to treat one tiny compiler boundary as arbitrary-language support.

## `H30` Contract

`H30_post_r36_r37_scope_decision_packet` should freeze the post-`R36/R37`
decision explicitly.

It must answer:

1. Did `R37` stay exact on the declared tiny compiled boundary?
2. If yes, is the result still only a narrow substrate-plus-lowering fact?
3. Do `R29`, `F3`, and broader headline claims remain blocked?
4. Does any later compiled or systems wave become justified, or does the repo
   remain on the same narrow Origin-core line?

`H30` should reclassify claims into supported, unsupported, and disconfirmed
without softening the current no-momentum rule.

## Worktree And Delegation Rule

Before any future `R37` execution:

- create a clean worktree from `wip/h27-promotion`;
- keep one worker on lowering/reference pairing;
- keep one worker on export/test/result surfaces;
- keep the integrating thread responsible for active driver changes and final
  claim wording;
- do not merge back into dirty `main` during execution.

## Low-Risk Remainder For The Current Wave

The current wave's remaining low-risk tasks are docs-only:

- propagate `H29/R36` into claim/publication ledgers;
- save `R37/H30` planning skeletons;
- keep commit hygiene explicit so the frozen Origin-core packet can later be
  committed as one coherent batch.

No additional runtime execution is required to close the present wave.
