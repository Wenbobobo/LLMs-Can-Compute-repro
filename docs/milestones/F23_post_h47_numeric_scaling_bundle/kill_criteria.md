# F23 Kill Criteria

`H48` must freeze the post-`H47` useful-case line as a practical falsifier if
any of the following occurs in `R49`:

1. no admitted float32 recovery regime stays exact on `bucket_a_2x`;
2. only `float64_reference` survives while all admitted float32 regimes fail;
3. exactness requires a new kernel, heap, alias-heavy pointers, recursion,
   float semantics, IO, or hidden mutable side channel;
4. success requires treating comparator/model evidence as a substitute for
   exact `R46/R47` evidence; or
5. exactness breaks so early that no clean transition to `F25` remains
   scientifically honest.

If none of these triggers fire and `bucket_a_2x` plus `bucket_b_4x` remain
exact under at least one admitted float32 regime, `H48` may authorize `F25`
as the next planning bundle.
