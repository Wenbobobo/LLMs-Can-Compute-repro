# Origin Long-Arc Summary

The real post-`H38` target is narrower than the article headline.

The current long arc is:

1. preserve the validated Origin-core substrate:
   append-only traces plus exact low-dimensional retrieval plus a small exact
   executor;
2. test whether the missing state-reconstruction obligations can be pushed from
   the current small stack/VM line into bounded addressable memory without
   hidden mutable side channels;
3. only then test whether a restricted Wasm / tiny-`C` lowering can run useful
   kernels exactly on that substrate.

This route treats the current repo as a `neural VM with indexed cache`, not as
evidence that a general LLM has become a computer.

The scientific target remains:

- `A`: computation as append-only trace;
- `B`: critical retrievals can be made sparse / geometric / sublinear;
- `C`: those retrievals support a useful exact executor;
- `D`: restricted program lowering only after `A/B/C` survive.

`D` is now a saved future route, not a current claim.
