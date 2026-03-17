# M4 Exact Hard-Max Model Results

## Current Scope

This milestone now contains the first deterministic bridge from `M3` trace
semantics to `M2` hard-max retrieval.

Current capability:

- immediate-address latest-write memory reads are encoded as exact 2D hard-max
  queries,
- runtime dynamic-address memory reads are also encoded and checked through the
  same exact hard-max bridge,
- stack-slot reads/writes are also decoded through the same latest-write bridge
  over logical stack-slot addresses,
- a narrow trainable scorer can be fitted on short stack traces and checked on
  longer traces and one cross-family stack example,
- both decode modes are present:
  - brute-force linear scan,
  - `HullKVCache` accelerated retrieval,
- both modes are required to agree exactly on every exported read event.

## Current Artifacts

- `decode_examples.json` records the latest-write and memory-accumulator trace
  examples, plus a dynamic-address memory example and stack-slot examples,
  together with exact linear/accelerated decode observations.
- `trainable_stack_latest_write.json` records the first narrow learned slice:
  fit on short countdown stack traces, then exact evaluation on held-out longer
  countdowns and a dynamic-memory stack trace.

For the current grid search, the selected scorer uses
`quadratic_scale=0.25` and `time_scale=0.0005`. It reaches exact program
accuracy `1.0` on:

- 7 short countdown training programs,
- 14 held-out longer countdown programs, including the `steps>=49` bucket,
- 1 dynamic-memory stack trace from a different program family.

The current dynamic-address example still targets a single effective address at
runtime. It is evidence that the bridge survives runtime address selection, not
yet evidence for broad dynamic-address workloads. The new stack examples should
be read the same way: they validate the bridge on real stack evolution. The
trainable scorer result is also narrow: it shows that a tiny parameterized
latest-write rule can fit and extrapolate on the current candidate-set task, not
that a full causal neural executor has been reproduced.

## Not Yet Included

- trainable attention modules,
- token-level parameterized models,
- free-running learned rollouts,
- learned generation of candidate writes or trace events.
