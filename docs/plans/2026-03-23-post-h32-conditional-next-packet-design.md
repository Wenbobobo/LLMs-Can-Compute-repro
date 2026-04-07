# 2026-03-23 Post-H32 Conditional Next-Packet Design

## Summary

`H32_post_r38_compiled_boundary_refreeze` plus the completed clean closeout in
`P18_post_h32_clean_worktree_promotion` leave the project in a strong but still
narrow state:

1. the active scientific target is still the Origin-core line:
   append-only trace, exact retrieval, and a small exact stack/VM executor;
2. the compiled-boundary line is now positive on one tiny family plus one
   richer control/call family;
3. the current result still does not justify automatic compiler breadth,
   arbitrary-language claims, or a new substrate question by momentum.

The next justified move is therefore planning-only. Before any later runtime
execution, the project should save one explicit post-`H32` packet design that
answers a narrower question:

is there still one scientifically necessary Origin-core substrate question left
inside the current admitted rows and opcode surface, or should the
compiled-boundary line be frozen as complete-for-now?

## Decision Options

### Option A: Freeze At `H32` And Shift To Background Maintenance

Pros:

- safest interpretation of the current no-widening state;
- keeps the branch focused on paper/control maintenance only.

Cons:

- leaves the main unresolved scientific risk underexplained:
  whether the current compiled exactness is mostly substrate-driven or too
  dependent on compiler-side structuring;
- gives later agents no principled rule for deciding whether another narrow
  same-substrate check is still worth doing.

### Option B: Recommended - Save One Docs-Only `H33` Question-Selection Packet

Pros:

- respects `H32` by keeping the next move docs-only;
- narrows the next question before any runtime work;
- targets the most important remaining risk from the origin notes and
  discussions: "compiler does all the work" or "the fast path only helps the
  easy part";
- keeps any later runtime lane on the same admitted rows, same opcode surface,
  and same Origin-core substrate unless a later packet explicitly says
  otherwise.

Cons:

- adds one more planning/control layer before any new runtime work;
- may end by freezing the compiled-boundary line complete-for-now rather than
  authorizing another experiment.

### Option C: Open A Broader Compiled Or New-Substrate Lane Now

Pros:

- maximizes short-term experimental throughput.

Cons:

- violates the current `H32` rule that a new plan is required first;
- risks breadth-by-momentum instead of a new falsifiable question;
- pushes the project back toward the blog headline rather than the narrower,
  defensible mechanism claim.

Rejected for now.

## Recommendation

Choose Option B.

The next packet after `H32/P18` should be one docs-only conditional
question-selection packet:

- candidate packet:
  `H33_post_h32_conditional_next_question_packet`;
- allowed outcomes:
  `freeze_compiled_boundary_as_complete_for_now` or
  `authorize_one_origin_core_substrate_question`;
- disallowed outcomes:
  automatic new-family widening, arbitrary `C`, broader Wasm rhetoric, or any
  scope-lift wording by momentum.

This recommendation follows the most conservative reading of the original
materials:

- the strongest reproducible claim is still the append-only / exact-retrieval /
  small-VM substrate, not broad "LLMs are computers";
- after `R38/H32`, the biggest unresolved risk is no longer raw family breadth;
  it is whether the current compiled-boundary result still depends too heavily
  on compiler-side structure or a narrow easy-case control surface.

## Save Rule

Save this design before any post-`H32` runtime execution.

- keep `H32` as the current active routing/refreeze packet;
- keep `P18` complete and preserved as the clean packaging lane;
- do not reopen dirty `main` or dirty `wip/h27-promotion`;
- do not treat this design as authorization by itself.

## Recommended Conditional Order

The recommended conditional order is:

`docs/plans/2026-03-23-post-h32-conditional-next-packet-design.md` ->
conditional docs-only
`H33_post_h32_conditional_next_question_packet` ->
either `freeze_compiled_boundary_as_complete_for_now`
or one same-substrate Origin-core substrate question.

No new runtime experiment is active until `H33` lands and picks one of those
two outcomes explicitly.

## `H33` Contract

`H33_post_h32_conditional_next_question_packet` should be docs-only.

It must:

- keep `H32` explicit as the current active routing/refreeze packet;
- compare exactly two next-step outcomes:
  `freeze_compiled_boundary_as_complete_for_now` and
  `authorize_one_origin_core_substrate_question`;
- preserve `R29`, `F3`, and frontier/demo widening as blocked;
- name at most one future runtime lane if it authorizes one;
- keep the same opcode surface and same admitted/boundary row discipline unless
  a later explicit packet changes that state.

## Candidate Substrate Question If `H33` Authorizes One

If `H33` authorizes one more narrow runtime lane, the recommended target is not
"one more compiled family." The recommended target is one same-substrate audit
of whether the current compiled result is genuinely runtime/mechanism-bearing.

Recommended candidate lane:

- `R39_origin_compiler_control_surface_dependency_audit`

Recommended question:

- on the current admitted row plus the current boundary probe, how much of the
  observed exactness depends on compiler-side control-surface structure versus
  the current append-only / exact-retrieval / small-VM substrate itself?

Required constraints:

- no new opcode;
- no new hidden host evaluator;
- no new program-family breadth;
- no new scope-lift wording;
- no replacement of the current admitted row with an easier surrogate.

If this question cannot be made precise enough, `H33` should choose
`freeze_compiled_boundary_as_complete_for_now` instead.

## Background Work While `H33` Is Only Planned

- refresh `F2_future_frontier_recheck_activation_matrix` to the current
  `H27 -> H28 -> H29 -> R36 -> R37 -> H30 -> H31 -> R38 -> H32` stack;
- keep `P12_manuscript_and_manifest_maintenance` low-priority and downstream of
  landed evidence;
- keep README/publication wording subordinate to `H32` until a later decision
  packet says otherwise.

## Defaults

- stay on the current Origin-core substrate;
- do not reopen same-endpoint `D0` recovery narratives as the active mainline;
- do not widen compiled-boundary scope by momentum;
- treat future frontier work as planning-only unless a later packet explicitly
  reauthorizes it.
