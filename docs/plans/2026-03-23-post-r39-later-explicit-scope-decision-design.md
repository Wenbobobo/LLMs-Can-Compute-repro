# 2026-03-23 Post-R39 Later Explicit Scope Decision Design

## Summary

`R39_origin_compiler_control_surface_dependency_audit` is now complete.

It answered the only question authorized by
`H33_post_h32_conditional_next_question_packet`:

- on one declared helper-body permutation with target renumbering, exact
  source/lowered/free-running execution survives on both the admitted row and
  the named same-family boundary probe;
- final state is preserved on both rows;
- trace changes on both rows, so the perturbation is not a no-op.

The next move should still remain narrow and explicit. The post-`R39`
scope-decision packet should therefore select:

- `freeze_compiled_boundary_as_complete_for_now`

instead of automatically authorizing a new runtime lane.

## Why Freeze Here

`R39` weakens the strongest "compiler did all the work" objection, but only in
one declared way. It does not establish arbitrary control-surface freedom, a
broader compiled-family result, or a broader language claim.

The line is now coherent but still intentionally narrow:

1. `R37` shows one tiny compiled subset survives on the active substrate;
2. `R38` shows one richer same-opcode control/call family survives;
3. `R39` shows one declared control-surface perturbation survives on the same
   two rows.

That is enough to preserve the current compiled-boundary evidence packet as
honest narrow support. It is not enough to justify another runtime question by
momentum when no single sharper same-substrate gap clearly dominates.

## Packet Contract

The later explicit post-`R39` packet must remain docs-only.

Required outputs:

- keep `H32_post_r38_compiled_boundary_refreeze` as the current active
  routing/refreeze packet;
- interpret `H33/R39` explicitly rather than leaving the downstream state
  implied;
- select one post-`R39` outcome and record the non-selected alternative;
- name no future runtime candidate in the selected freeze outcome;
- preserve `R29`, `F3`, and frontier/demo widening as blocked.

## Selected Versus Non-selected Outcomes

Selected outcome:

- `freeze_compiled_boundary_as_complete_for_now`

Non-selected alternative:

- `authorize_one_more_origin_core_substrate_question`

The non-selected alternative remains available only behind a future explicit
packet tied to a concrete contradiction or a sharper same-substrate gap than
the ones already audited in `R37/R38/R39`.

## Reopen Conditions

Do not reopen the compiled-boundary line unless a later packet can name all of
the following in advance:

- one concrete contradiction, failure mode, or sharper unresolved dependency
  tied back to the current admitted row and/or the named same-family boundary
  probe;
- one predeclared same-substrate comparator set;
- no new opcode, no hidden host evaluator, and no family-breadth drift;
- one fixed success/failure criterion before execution.

Without that standard, `H34` should freeze the line complete-for-now rather
than manufacturing another weak positive lane.

## Save Rule

Save this design before landing the post-`R39` scope-decision packet.

- keep the packet docs-only;
- keep the commit packet-scoped;
- sync `README.md`, `STATUS.md`, the publication entrypoints, and
  `tmp/active_wave_plan.md` only after the packet artifacts exist;
- do not treat the decision packet as a routing change or as frontier
  authorization.
