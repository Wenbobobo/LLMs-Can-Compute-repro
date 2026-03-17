# Trainable Latest-Write Stack Slice Design

## Goal

Add the smallest trainable `M4` slice without pretending that a full learned
executor already exists.

The target is narrower than a token model:

- keep the exact latest-write retrieval structure fixed,
- derive candidate sets from real `exec_trace` stack-slot events,
- fit only the scoring weights that choose the correct prior write,
- and measure exact success on longer countdown traces plus a different stack
  trace family.

## Options Considered

1. **End-to-end neural decoder now**
   Rejected. It would hide whether failure comes from representation,
   optimization, or rollout drift.

2. **Small trainable scorer over exact latest-write candidates**
   Chosen. It keeps the causal retrieval problem explicit while adding a real
   learned parameter fit.

3. **Broaden deterministic coverage further before any fitting**
   Useful, but no longer the highest-value step. The stack and memory bridge is
   already broad enough to justify one narrow learned slice.

## Chosen Shape

- Use logical stack-slot read/write operations extracted from reference traces.
- For each read, build the candidate set of all prior writes plus seeded default
  values.
- Fit a two-parameter scorer:
  - a quadratic address term that rewards exact address match,
  - and a positive time term that prefers the latest write at that address.
- Train on short countdown traces only.
- Evaluate on:
  - the training slice,
  - longer countdown traces bucketed by execution length,
  - a dynamic-memory program viewed through its stack-slot trace.

## Why This First

This is the first place where `M4` stops being purely deterministic, but it
still keeps the claim narrow and inspectable. If this tiny learned slice cannot
generalize across longer traces with the exact inductive bias baked in, there is
little reason to trust a larger learned executor yet.
