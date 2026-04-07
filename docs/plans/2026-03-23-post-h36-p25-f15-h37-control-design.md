# Post-H36 P25-F15-H37 Control Design

This design lands one narrow docs/control wave after the completed
`H35 -> R40 -> H36 -> P24` bounded-scalar packet. It does not authorize a new
runtime lane by momentum.

## Objective

Lock three follow-on tasks in order:

1. `P25_post_h36_clean_promotion_prep`
   prepares one clean promotion inventory from the real source-of-truth branch
   `wip/h35-r40-p24-exec` without touching dirty `main`;
2. `F15_post_h36_origin_goal_reanchor_bundle`
   replaces `F12` as the current canonical derivative mapping from the origin
   materials onto the landed `H36/P24` state;
3. `H37_post_h36_runtime_relevance_decision_packet`
   consumes `H36`, `P25`, `F15`, `F14`, and the saved `R41` design and selects
   exactly one of two outcomes:
   `keep_h36_freeze` or
   `authorize_r41_origin_runtime_relevance_threat_stress_audit`.

The default is `keep_h36_freeze`.

## Packet Order

1. `P25_post_h36_clean_promotion_prep`
2. `F15_post_h36_origin_goal_reanchor_bundle`
3. `H37_post_h36_runtime_relevance_decision_packet`

No runtime lane follows automatically. If a later contradiction packet ever
reauthorizes `R41`, the future order must still be:

later explicit packet ->
conditional `R41_origin_runtime_relevance_threat_stress_audit` ->
later refreeze packet

## P25 Scope

`P25` is operational only.

It must:

- preserve `wip/h35-r40-p24-exec` as the scientific source of truth;
- preserve `main` as dirty and not directly touched in this wave;
- create one clean prep branch/worktree:
  `wip/p25-f15-h37-exec` at
  `D:/zWenbo/AI/LLMCompute-worktrees/p25-f15-h37-exec`;
- inventory the landed `H27 -> H36/P24` window and the attached planning
  surfaces that are ahead of `main`;
- record a future promotion runbook, but not execute the promotion.

It must not:

- merge by momentum;
- mix unrelated dirty-tree work into the packet;
- reopen runtime execution.

## F15 Scope

`F15` is the new canonical derivative bundle for the origin article plus the
three discussion files.

It must:

- mark the append-only / exact-retrieval / small-executor floor as
  `supported_here`;
- mark the tiny compiled slice, richer same-opcode control family, and bounded
  scalar locals/flags family as `supported_here` narrowly;
- rank the two surviving same-substrate cautions from `F14` as the top current
  unresolved gaps:
  `runtime_irrelevance_via_compiler_helper_overencoding` and
  `fast_path_only_helps_the_easy_part`;
- keep restricted semantic-boundary work, arbitrary `C`, general
  LLM-computer rhetoric, and broad systems claims blocked.

## H37 Decision Rule

`H37` remains docs-only and keeps `H36` as the preserved prior
routing/refreeze packet.

Selected outcome:

- `keep_h36_freeze`

Non-selected outcome:

- `authorize_r41_origin_runtime_relevance_threat_stress_audit`

`H37` may authorize `R41` only if one candidate satisfies the full `F14`
admissibility gate on the fixed landed `R40` row pair:

- same admitted row and same boundary row;
- same opcode surface;
- same substrate;
- one named contradiction tied to exactly one of the two surviving threat
  families;
- one fixed comparator set already implied by `F13`;
- one predeclared measurement rule;
- one explicit stop condition;
- no need for richer values outside `bounded scalar locals and flags`.

If no uniquely isolated admissible candidate exists, `H37` must keep the
freeze and leave `R41` deferred.

## Required Outputs

- `P25`:
  `promotion_manifest.md`, `hygiene_summary.md`,
  `source_of_truth_delta.md`, `worktree_runbook.md`
- `F15`:
  `claim_delta_matrix.md`, `scientific_goal_stack.md`,
  `repro_gap_ladder.md`, `origin_material_index.md`
- `H37`:
  standard docs-only packet set plus machine-readable `results/` summary,
  checklist, claim packet, and snapshot

## Non-Goals

This wave does not authorize:

- immediate merge into `main`;
- `R41` execution by default;
- restricted-Wasm widening;
- arbitrary `C` rhetoric;
- hybrid planner/executor work;
- frontier or same-endpoint reopen.
