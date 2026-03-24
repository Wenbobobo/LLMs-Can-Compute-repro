# Post-H45 R47 Restricted Frontend Translation Design

## Objective

`R47_origin_restricted_frontend_translation_gate` executes the first exact
frontend bridge admitted by `H45`.

The bridge remains deliberately narrow:

- one structured frontend surface only;
- bounded `i32` values and static memory only;
- lowering onto the already-landed useful-case bytecode kernels only; and
- no new runtime stack, heap model, alias-heavy pointer story, recursion,
  float, IO, or model-side comparison.

## Locked Inputs

- current active docs-only packet:
  `H45_post_r46_surface_decision_packet`;
- preserved prior route packet:
  `H44_post_h43_route_reauthorization_packet`;
- current paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`;
- preserved prior exact runtime gate:
  `R46_origin_useful_case_surface_generalization_gate`;
- fixed useful-case ladder:
  `R44_origin_restricted_wasm_useful_case_execution_gate`;
- current exact-first planning bundle:
  `F21_post_h43_exact_useful_case_expansion_bundle`; and
- blocked comparator bundle:
  `F22_post_r46_useful_case_model_bridge_bundle`.

## Design

Implement one tiny structured frontend AST plus compiler that can express only
the admitted useful-case forms:

- static buffer initialization;
- accumulator fold over a fixed buffer;
- fixed per-element equality branch for nonzero counting; and
- fixed 16-way equality dispatch for histogram bin updates.

The compiler must lower to bytecode programs that are instruction-identical to
the existing useful-case kernels on the admitted cases. `R47` then reuses the
same verification chain as `R46`: verifier, spec oracle, lowered
`exec_trace`, and accelerated free-running exact execution.

## Executed Surface

Execute the same `8` held-out useful-case variants already used by `R46`:

- `2` sum variants;
- `3` count-nonzero variants; and
- `3` histogram variants.

This keeps the evidence contract fixed while testing whether the structured
frontend bridge preserves the already-landed semantics exactly.

## Acceptance

- `translation_identity_match = true` on all admitted rows;
- no excluded feature survives validation;
- exactness survives across bytecode, canonical kernel, lowered path, and
  free-running execution on all `8/8` rows across `3/3` kernels;
- the gate returns `restricted_frontend_supported_narrowly`; and
- the next required lane becomes
  `H46_post_r47_frontend_bridge_decision_packet`.
