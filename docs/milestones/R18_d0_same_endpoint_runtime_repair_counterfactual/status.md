# Status

Provisioned on 2026-03-20 as an optional `H16` lane and conditionally activated
by `R17` on 2026-03-20.

- `R18` was inactive by default until `R17` named one bounded repair target:
  `helper_checkpoint_braid_long` on `retrieval_total`;
- it remains comparator-only and same-endpoint even after activation;
- `R18a` completed one decomp-first `partitioned_exact` memory probe on the
  named target plus matched control `stack_memory_braid`, but did not clear its
  target gate;
- `R18b` has now completed the bounded pointer-like exact retrieval follow-up
  on both stack and memory reads;
- exactness held on the focused target plus matched control, the target reached
  about `1308.5x` versus the recorded `R17` accelerated baseline, and the full
  admitted `8/8` confirmation sweep also stayed exact;
- the confirmation median reached about `1252.7x` versus the recorded `R17`
  accelerated baseline, so `R18` now closes as a confirmed same-surface runtime
  repair packet;
- `R18c` staged deterministic retrieval is therefore not needed;
- the packet now hands directly to `H17_refreeze_and_conditional_frontier_recheck`;
- `R18` still cannot be used to widen claim scope indirectly.
