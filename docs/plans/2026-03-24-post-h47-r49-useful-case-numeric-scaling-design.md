# Post-H47 R49 Useful-Case Numeric Scaling Gate Design

## Objective

Execute the only runtime lane admitted by landed `F23` without widening the
claim ceiling above bounded useful cases.

`R49` must answer one question only: does the preserved exact useful-case
surface from `R46/R47` survive one more narrow numeric-scaling extension when
buffer length, absolute base span, and exact step budget are widened inside
the saved `F23` envelope?

## Locked Scope

- preserve `H47_post_r48_useful_case_bridge_refreeze` as the current active
  docs-only packet;
- preserve `H43_post_r44_useful_case_refreeze` as the paper-grade endpoint;
- preserve the fixed kernel family:
  `sum_i32_buffer`, `count_nonzero_i32_buffer`, and `histogram16_u8`;
- keep the runtime surface at structured `i32` plus static memory only;
- keep exact `R46/R47` evidence decisive relative to comparator-only `R48`;
- keep `F24_post_h47_hybrid_executor_growth_bundle` dormant; and
- do not activate heap, alias-heavy pointers, recursion, float semantics, IO,
  hidden mutable side channels, or broader Wasm/`C` rhetoric.

## Executed Regimes

`R49` executes exactly four precision regimes:

- `float32_single_head` as the preserved negative control;
- `float32_radix2` as the primary admitted recovery regime;
- `float32_block_recentered` as the coequal admitted recovery regime; and
- sampled `float64_reference` rows on one boundary-bearing case per bucket.

`R49` does not activate `float32_segment_rescaled`,
`bfloat16_single_head`, or `float16_single_head`. Those remain reserve or
diagnostic-only rows and are not needed to answer the narrow gate question.

## Bucket Contract

`R49` uses the saved `F23` buckets directly:

- `bucket_a_2x`: `len16` / `len18` / `len16`, `+256` preserved-base shift,
  `max_steps = 600`;
- `bucket_b_4x`: `len32` / `len36` / `len32`, `+1024` preserved-base shift,
  `max_steps = 1600`;
- `bucket_c_8x`: `len64` / `len72` / `len64`, `+4096` preserved-base shift,
  `max_steps = 4000`.

The gate remains two-layered:

1. exactness first on source/spec, lowering parity, and free-running exact
   execution;
2. memory-only finite-precision screening on exact rows only.

## Acceptance

The wave is complete only if it exports machine-readable:

- exactness rows for all `9` widened cases;
- precision screening rows for the admitted regimes plus sampled references;
- bucket summaries that make the `bucket_a/b/c` decision boundary explicit;
- a stop-rule file that maps directly onto the `F23` kill criteria; and
- one summary that hands interpretation to
  `H48_post_r49_numeric_scaling_decision_packet`.

If `bucket_a` or `bucket_b` loses all admitted float32 recovery regimes, the
line should be treated as a practical falsifier rather than widened further.
