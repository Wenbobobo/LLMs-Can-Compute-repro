# Post-H38 F18-F19 Long-Arc Design

This design lands one planning-only post-`H38` wave on top of the completed
`F16 -> H38 -> P26 -> F17` control stack. It does not authorize runtime
execution, merge `main`, or treat a saved roadmap as an active lane.

## Objective

Lock two planning bundles in order:

1. `F18_post_h38_origin_core_long_arc_bundle`
   fixes the current claim ladder, route-selection defaults, and
   worktree/merge policy after the `H38` keep-freeze decision;
2. `F19_post_f18_restricted_wasm_useful_case_roadmap`
   turns the semantic-boundary route into one decision-complete near-term
   roadmap for bounded restricted-Wasm / tiny-`C` useful cases without
   authorizing execution.

The default forward direction is semantic-boundary planning under `F9`, not a
same-substrate reopen.

## Packet Order

1. `F18_post_h38_origin_core_long_arc_bundle`
2. `F19_post_f18_restricted_wasm_useful_case_roadmap`

No runtime lane follows automatically. If the semantic-boundary route is later
authorized explicitly, the future order must still be:

later explicit post-`H38` semantic-boundary packet ->
conditional `R42_origin_append_only_memory_retrieval_contract_gate` ->
conditional `R43_origin_bounded_memory_small_vm_execution_gate` ->
conditional `R44_origin_restricted_wasm_useful_case_execution_gate` ->
later explicit refreeze / route-selection packet

If a same-substrate contradiction ever becomes uniquely isolating instead, the
future order remains:

later explicit post-`H38` packet ->
conditional `R41_origin_runtime_relevance_threat_stress_audit` ->
`H39_post_r41_runtime_relevance_refreeze`

## F18 Scope

`F18` is planning-only and route-fixing only.

It must:

- preserve `H38` as the current active docs-only decision packet;
- preserve `H36` as the underlying active routing/refreeze packet;
- preserve `P26` as `audit_only`, not merge authorization;
- preserve `F17` as the route-selection bundle that blocks automatic reopen;
- make the claim ladder explicit as `A/B/C/D`;
- mark `F9` as the preferred forward family if the next question becomes
  semantic-boundary / useful-case work;
- keep `R41` as a deferred contradiction route only, not the default next move;
- keep `F11` as `requires_new_substrate`;
- record a save-first, clean-worktree-first, subagent-parallel work rule.

It must not:

- replace `H38` as the active routing packet;
- activate `R41`, `R42`, `R43`, or `R44`;
- authorize a merge into dirty `main`;
- relabel arbitrary `C`, general LLM-computer rhetoric, or demo-first work as
  current science.

## F19 Scope

`F19` is planning-only semantic-boundary storage after `F18`.

It must:

- treat restricted Wasm / tiny `C` as a bounded future surface, not as
  reproduced arbitrary `C`;
- fix one allowed semantic surface:
  pointer-free bounded `i32`, arithmetic, comparisons, branches/loops, bounded
  locals, bounded static memory, and optional single-layer `call/return`;
- exclude heap, alias-heavy pointers, indirect calls, float, IO, and external
  side effects;
- fix three deferred future gates:
  `R42`, `R43`, and `R44`;
- fix one useful-case kernel ladder:
  `sum_i32_buffer`,
  `count_nonzero_i32_buffer`,
  `histogram16_u8`;
- record that exact lowering / compile-style execution is the default first
  route, while any later trainable executor variant is comparator-only.

It must not:

- authorize execution of the three future gates;
- widen the current same-substrate opcode family;
- treat a roadmap as proof that restricted Wasm is already supported.

## Required Outputs

- `F18`:
  `origin_long_arc_summary.md`,
  `claim_ladder.md`,
  `route_activation_matrix.md`,
  `merge_worktree_policy.md`
- `F19`:
  `restricted_wasm_surface.md`,
  `future_gate_matrix.md`,
  `useful_kernel_set.md`
- `R42`:
  fixed audit scope, required outputs, and stop rules
- `R43`:
  fixed execution scope, required outputs, and stop rules
- `R44`:
  fixed lowering scope, kernel suite, required outputs, and stop rules

## Non-Goals

This wave does not authorize:

- `R41` execution by default;
- arbitrary `C`, unrestricted Wasm, or general-computer claim lift;
- hybrid planner/executor work;
- paper/blog/README expansion beyond low-priority maintenance;
- merging dirty `main`.
