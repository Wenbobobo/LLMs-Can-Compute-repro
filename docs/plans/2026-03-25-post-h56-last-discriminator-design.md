# 2026-03-25 Post-H56 Last Discriminator Design

## Summary

`H56` already closed the compiled useful-kernel bridge lane as a narrow exact
bridge without bounded value. The only remaining scientifically meaningful
question is whether that value-negative result was mostly a compiled-route
artifact or whether the current append-only executor still lacks bounded value
even when the same useful kernels are run as native trace programs.

This design therefore fixed one last narrow sequence:

`F31 -> H57 -> R62 -> H58`

with `P40` as the only low-priority operational sidecar.

## Runtime Question

`R62` asks only this:

- if `sum_i32_buffer` and `count_nonzero_i32_buffer` are encoded directly in
  the trace DSL, with no TinyC or bytecode lowering time counted in the
  executor comparator, does accelerated internal execution show bounded value
  over native linear execution or over transparent external references?

The declared rows stay deliberately small:

- `sum`: lengths `16` and `64`
- `count_nonzero`: lengths `32` and `64`

## Decision Rule

Positive evidence would require:

- exactness on every declared row
- accelerated beating linear on the longest row of each kernel
- strong aggregate speedup rather than a marginal win
- at least one kernel landing within one order of magnitude of the plain
  external scalar comparator

Any weaker result closes the mainline at `H58`.

## Defaults

- keep `F27`, `R53`, and `R54` blocked
- keep dirty root `main` unmerged
- keep raw large artifacts out of git by default
- prefer early stop over momentum-driven widening
