# R45 Mode Mapping

`R45` uses two narrow model-side executor modes on the landed `R43` contract
family:

1. `compiled_weight_executor`
   - stack reads use one analytic quadratic latest-write scorer;
   - the scorer weights are compiled from the bounded contract horizon rather
     than fitted from examples;
   - memory reads remain `accelerated_exact`;
   - call-frame reads remain `pointer_like_exact`.

2. `trainable_2d_executor`
   - stack reads use the same two-parameter scorer family;
   - the scorer is fitted on the four `R43` core families only;
   - evaluation then runs on all five `R43` families, including the held-out
     optional single-call/return family;
   - memory reads remain `accelerated_exact`;
   - call-frame reads remain `pointer_like_exact`.

This mapping keeps `R45` honest:

- it is a real model/comparator lane on the same bounded kernels;
- it does not pretend to be a full unconstrained neural executor;
- it does not let model evidence replace the landed exact `R43` gate.
