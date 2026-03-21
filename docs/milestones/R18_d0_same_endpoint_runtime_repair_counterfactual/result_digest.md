# Result Digest

`R18` closes as a confirmed comparator-only same-endpoint runtime repair
packet. `R18a` first measured one decomp-first exact memory-only
counterfactual on the bounded
`helper_checkpoint_braid_long/retrieval_total` target named by `R17`. `R18b`
then replaced that narrow memory-only probe with pointer-like exact retrieval
on both stack and memory reads, kept the focused target plus matched control
exact, and cleared the full admitted `8/8` confirmation sweep on the same
lowered `D0` endpoint.

## What `R18a` established

- exported one focused target/control comparator packet plus machine-readable
  trace-address profiles;
- preserved exact trace and exact final state on both focused probe rows under
  `partitioned_exact` memory retrieval;
- confirmed that the target remains a dense but still local six-address memory
  trace (`2168` memory ops, `1262` loads, `906` stores, hottest address
  `312`);
- confirmed that the matched control is also six-address but lighter
  (`1009` memory ops, `703` loads, `306` stores, hottest address `112`).

## What `R18a` did not close

- the target improved only about `1.283x` versus the recorded `R17`
  accelerated baseline, below the required `2.0x` gate;
- the matched control ran slower at about `0.651x`, so address partitioning
  alone did not isolate a clean local repair win;
- the full admitted-surface confirmation sweep was not run because the target
  gate failed.

## What `R18b` closed

- pointer-like exact retrieval on both stack and memory reads kept the focused
  target and matched control exact;
- the focused target reached about `1308.5x` versus the recorded `R17`
  accelerated baseline;
- the full admitted `8/8` confirmation sweep stayed exact and reached a median
  of about `1252.7x` versus the recorded `R17` accelerated baseline;
- `R18` therefore closes directly under `R18b`, without needing `R18c`.

## Preserved boundary

This packet remains comparator-only and same-endpoint. It does not by itself
authorize arbitrary compiled-language claims, general softmax replacement, or a
broader “LLMs are computers” headline.
