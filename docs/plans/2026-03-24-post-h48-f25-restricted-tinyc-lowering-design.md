# Post-H48 F25 Restricted Tiny-C Lowering Design

## Objective

`F25_post_h48_restricted_tinyc_lowering_bundle` is the next planning-only
bundle after landed `H48`.

It does not execute a runtime lane. It saves the smallest scientifically honest
restricted tiny-`C` lowering question that can still test whether the preserved
useful-case bridge can move one step closer to a compiled-language surface
without inflating the claim ceiling.

The bundle stays narrow:

- `H48` remains the current active docs-only packet;
- `H43` remains the paper-grade endpoint;
- `R49` remains completed evidence rather than a continuing lane;
- `R47` remains the preserved exact frontend bridge contract to reuse first;
- no new numeric widening is fused into the first tiny-`C` attempt; and
- arbitrary `C`, broader Wasm, hybrid execution, and model substitution remain
  out of scope.

## Locked Inputs

- current active docs-only packet:
  `H48_post_r49_numeric_scaling_decision_packet`
- preserved prior docs-only packet:
  `H47_post_r48_useful_case_bridge_refreeze`
- current paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- preserved exact frontend bridge gate:
  `R47_origin_restricted_frontend_translation_gate`
- completed current numeric-scaling gate:
  `R49_origin_useful_case_numeric_scaling_gate`
- exact-first planning boundary:
  `F21_post_h43_exact_useful_case_expansion_bundle`
- preserved restricted future frontend boundary:
  `F19_post_f18_restricted_wasm_useful_case_roadmap`
- current low-priority operational wave:
  `P35_post_h47_research_record_rollup`

## Bundle Outputs

`F25` must save exactly four planning surfaces:

- `admitted_surface_matrix`
- `excluded_feature_matrix`
- `execution_matrix`
- `kill_criteria`

It must also fix:

- `R50_origin_restricted_tinyc_lowering_gate` as the only next runtime
  candidate;
- `H49_post_r50_tinyc_lowering_decision_packet` as the only follow-up packet
  that may interpret `R50`; and
- `P36_post_h48_falsification_closeout_bundle` as the preserved non-selected
  closeout branch inherited from `H48`.

## Acceptance

- the bundle remains planning-only;
- `H48` remains the current active docs-only packet;
- `H43` remains the paper-grade endpoint;
- `R49` remains completed current evidence, not an active lane;
- `R50` is the only next runtime candidate fixed here;
- `H49` is the only explicit follow-up packet fixed here;
- the admitted tiny-`C` surface stays limited to bounded `i32` scalars,
  declared static buffers, structured control flow, fixed-range table updates,
  and one top-level kernel function;
- heap, alias-heavy pointers, recursion, float, IO, hidden mutable state,
  library calls, multi-function programs, and arbitrary `C` wording remain
  excluded; and
- the first runtime pass must reuse the preserved `R47` useful-case contract
  before any later packet considers further widening.
