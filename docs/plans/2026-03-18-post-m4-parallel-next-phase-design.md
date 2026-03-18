# Post-M4 Parallel Next-Phase Design

> Status note (2026-03-19): partially completed and now superseded. Use this
> file for historical rationale only; current forward planning lives in
> `tmp/2026-03-18-next-stage-plan.md` and the new milestone docs.

## Why this plan exists

`M4-D` and `M4-E` changed the project shape. The staged bridge now has a clear
negative closure under fairer regimes, the precision story is broader but still
narrow, and `M5` is frozen strongly enough to stop open-ended rescue work.

That means the next unattended phase should not chase broader demos. It should
turn the current claim freeze into:

- tighter residual `M4` evidence,
- an implementation-ready tiny-bytecode frontend contract,
- and a paper-grade evidence bundle.

## Chosen track split

### Track A — `M4_failure_provenance`

Purpose:
- explain staged failure roots more precisely than `step_budget` rows alone.

Hard constraints:
- fixed staged checkpoint;
- fixed decode ladder;
- no new regimes, no capacity rescue.

### Track B — `M4_precision_organic_traces`

Purpose:
- widen `C3e` beyond offset-derived streams without widening the scheme set.

Hard constraints:
- keep schemes frozen to `single_head`, `radix2`, and `block_recentered`;
- screen at base `64`, sweep wider bases only on boundary signals.

### Track C — `M6` tiny typed bytecode

Purpose:
- make the first compiled frontend implementation-ready without semantic
  guesswork.

Hard constraints:
- reuse current `exec_trace` semantics;
- keep the first type system to `i32`, `addr`, `flag`;
- keep the first opcode set minimal and integer-only.

### Track D — `P1` paper readiness

Purpose:
- ensure later paper writing depends on preserved evidence rather than reruns.

Hard constraints:
- every unattended batch updates ledgers in the same batch;
- mandatory figures/tables are tracked explicitly.

## Implementation order

1. Finish contract/spec updates for `M6` and `P1`.
2. Add new `M4 residual` milestone records and placeholder result dirs.
3. Run residual `M4` batches before any compiled-demo work.
4. Implement the typed-bytecode harness only in a dedicated follow-up batch.

## Stop/go rules

- Do not reopen staged decoder rescue unless a new fair-regime positive signal
  appears.
- Do not add new precision schemes before organic traces are mapped.
- Do not start compiled demos before the typed-bytecode harness is implemented
  and the paper bundle remains synchronized.
