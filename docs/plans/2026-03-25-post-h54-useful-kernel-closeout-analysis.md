# 2026-03-25 Post-H54 Useful-Kernel Closeout Analysis

## Scope

This note distills what changed scientifically between the prior compiled-boundary
closeout `H54` and the current useful-kernel closeout `H56`, using the landed
`R60/R61` results and the earlier value-negative comparators `R52` and `R57`.

The intended use is narrow: give the next planning packet a compact evidence
base for deciding whether more execution is justified or whether the project
should move toward a stronger stop / paper / falsification framing.

## What `R60` Actually Added

`R60` is a real scientific lift over `H54`, but only on the exactness axis.

- It moved the compiled-boundary line from fixed typed stack-bytecode rows to a
  preserved useful-kernel pair: `sum_i32_buffer` and
  `count_nonzero_i32_buffer`.
- It executed `5/5` admitted variants exactly across `2/2` preserved kernels.
- It preserved translation identity exactly on all `5/5` rows.
- It recorded `compiler_work_leakage_break_count = 0`, so the positive result
  is not merely a hidden-compiler shortcut under the current audit.

That means the strongest surviving positive reading is now:

the current exact compiled route can carry one minimal useful-kernel bridge
without widening to arbitrary `C`, broad Wasm, or a general runtime claim.

## What `R61` Closed

`R61` closes the value question much more sharply than `H54` alone.

On the exact `R60` rows:

- accelerated exactness stayed intact on `5/5`;
- linear exactness stayed intact on `5/5`;
- external exact final values stayed intact on `5/5`;
- accelerated speedup counts were `0/5` against linear, source, lowered, and
  external baselines.

The timing shape is not borderline. It is strongly negative.

- Mean accelerated / linear ratio: `1.726x` slower.
- Mean accelerated / external ratio: `1519.7x` slower.
- Mean accelerated end-to-end / source-total ratio: `20.9x` slower.
- Mean accelerated end-to-end / lowered-total ratio: `20.0x` slower.

By kernel family:

- `sum_i32_buffer`: mean accelerated / linear ratio `1.406x`; mean accelerated
  / external ratio `689.3x`; mean retrieval share `0.940`.
- `count_nonzero_i32_buffer`: mean accelerated / linear ratio `1.939x`; mean
  accelerated / external ratio `2073.3x`; mean retrieval share `0.826`.

This is not a case where the route is almost competitive but loses by a small
constant. The compiled useful-kernel bridge is exact yet operationally much
worse than the transparent baselines.

## Comparison To Earlier Value-Negative Lanes

The important question for next planning is whether `R61` is a one-off bad
measurement or part of a stable pattern. The landed record now says it is a
stable pattern.

Earlier negative comparators:

- `R52`: mean accelerated / linear ratio `0.996x` with `3/5` rows faster than
  linear, but still `121.9x` slower than the external interpreter.
- `R57`: mean accelerated / linear ratio `1.876x`, mean accelerated / external
  ratio `35.8x`, mean retrieval share `0.763`.
- `R61`: mean accelerated / linear ratio `1.726x`, mean accelerated / external
  ratio `1519.7x`, mean retrieval share `0.872`.

Interpretation:

1. The project repeatedly recovers exact mechanism support.
2. The project repeatedly fails to recover bounded system value over simpler
   transparent baselines.
3. The compiled useful-kernel bridge makes the external gap worse, not better,
   because compiler/lowering overhead is now part of the honest route cost.

So the line is not trending toward a latent systems overturn. It is trending
toward a clearer statement that exactness survives farther than value does.

## Implication For The Next Planning Packet

The next explicit plan should assume the following default stance unless new
evidence contradicts it:

- keep `H56` as a legitimate closeout rather than a staging point that must be
  extended automatically;
- treat "exact compiled useful-kernel bridge exists" as already answered
  positively by `R60`;
- treat "this route retains bounded value over simpler baselines" as answered
  negatively, and now answered negatively across multiple related lanes;
- require any reopen to target a different discriminating question, not merely
  another nearby execution demo.

Concretely, the next wave is only justified if it can do at least one of:

1. threaten the current negative value reading with a genuinely different cost
   structure;
2. sharpen a falsifier that would let the project stop earlier and more cleanly;
3. raise paper value by clarifying a scientific boundary rather than by adding
   another narrow exact demo.

If no such question is available, the efficient move is to stop broadening and
consolidate the exact-but-value-negative conclusion.
