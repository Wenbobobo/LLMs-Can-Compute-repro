# R50 Stop Conditions

- stop scientific success immediately if any row breaks tiny-`C` surface
  validation, restricted-frontend lowering, verifier, source/spec agreement,
  canonical identity, lowering parity, or free-running exactness;
- stop immediately if success requires dynamic lengths, parameters, heap,
  pointers, recursion, float, IO, library calls, or hidden mutable state;
- stop immediately if `hist[16]` can only pass by widening the declared fixed
  table boundary;
- do not rescue a failed row by reintroducing fused numeric widening or model
  substitution; and
- if all admitted rows stay exact, stop at `H49` rather than widening by
  momentum.
