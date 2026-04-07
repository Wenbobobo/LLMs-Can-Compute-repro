# Post-F25 R50 Restricted Tiny-C Lowering Design

## Objective

`R50_origin_restricted_tinyc_lowering_gate` is the only runtime lane admitted
after landed `F25`.

The gate stays deliberately narrow:

- `H48` remains the current active docs-only packet;
- `H43` remains the paper-grade endpoint;
- `F25` remains the planning bundle that fixed this lane;
- `R49` remains completed numeric-scaling evidence rather than a fused second
  axis here; and
- `R47` remains the preserved exact bridge contract that this gate must reuse
  first.

## Locked Inputs

- current active docs-only packet:
  `H48_post_r49_numeric_scaling_decision_packet`
- current post-`H48` planning bundle:
  `F25_post_h48_restricted_tinyc_lowering_bundle`
- current paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- preserved exact frontend bridge gate:
  `R47_origin_restricted_frontend_translation_gate`
- completed current numeric-scaling gate:
  `R49_origin_useful_case_numeric_scaling_gate`

## Admitted Runtime Surface

The source surface is restricted tiny-`C`, not arbitrary `C`.

Admitted now:

- one zero-argument top-level kernel function only;
- bounded `int` literals and scalar accumulators only;
- one declared static input array with fixed literals;
- one declared static output scalar or one declared fixed `hist[16]` table;
- one canonical counted `for` loop with compile-time bound;
- one canonical `if (input[i] != 0)` branch for the count family; and
- one canonical `switch (input[i])` over fixed cases `0..15` for the
  histogram family.

Not admitted:

- function parameters, dynamic array lengths, heap, pointers, recursion,
  float, IO, library calls, multi-function programs, hidden mutable globals,
  or arbitrary `C` wording.

## Acceptance

- the lane executes exactly the preserved `R47` `8/8` useful-case variants
  across the fixed `3/3` kernel ladder;
- tiny-`C` source lowers into the admitted restricted frontend surface first,
  then into the same canonical bytecode kernels;
- translation identity against the canonical kernels remains exact on all
  admitted rows;
- free-running exact execution remains exact on all admitted rows; and
- interpretation stops at
  `H49_post_r50_tinyc_lowering_decision_packet`.
