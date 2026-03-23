# Post-H37 F16-H38-P26 Candidate Isolation Design

This design lands one narrow docs/control wave after the completed
`P25 -> F15 -> H37` control packet. It does not authorize runtime execution by
momentum.

## Objective

Lock four follow-on tasks in order:

1. `F16_post_h37_r41_candidate_isolation_bundle`
   reduces the saved `R41` candidate catalog to decision-complete statuses on
   the fixed landed `R40` row pair;
2. `H38_post_f16_runtime_relevance_reopen_decision_packet`
   consumes `F16`, `H37`, `F15`, `F14`, and the saved `R41` design and selects
   exactly one of two outcomes:
   `keep_h36_freeze` or
   `authorize_r41_origin_runtime_relevance_threat_stress_audit`;
3. `P26_post_h37_promotion_and_artifact_hygiene_audit`
   audits promotion posture and artifact hygiene on a clean successor branch
   without touching dirty `main`;
4. `F17_post_h38_same_substrate_exit_criteria_bundle`
   stores the next planning-only route-selection rules if `H38` keeps the
   freeze.

The default remains `keep_h36_freeze`.

## Packet Order

1. `F16_post_h37_r41_candidate_isolation_bundle`
2. `H38_post_f16_runtime_relevance_reopen_decision_packet`
3. `P26_post_h37_promotion_and_artifact_hygiene_audit`
4. `F17_post_h38_same_substrate_exit_criteria_bundle`

No runtime lane follows automatically. If a later packet ever authorizes
`R41`, the future order must still be:

later explicit packet ->
conditional `R41_origin_runtime_relevance_threat_stress_audit` ->
`H39_post_r41_runtime_relevance_refreeze`

## F16 Scope

`F16` is planning-only and candidate-isolation only.

It must:

- preserve `H37` as the prior docs-only runtime-relevance decision packet;
- preserve `H36` as the active routing/refreeze packet underneath `H38`;
- keep the candidate catalog fixed to the three `F14` ids only;
- lock every candidate to the landed `R40` row pair, the first four `F13`
  comparators, one measurement rule, and one stop rule;
- assign each candidate exactly one status:
  `inadmissible`, `nonunique`, or `execution_ready`;
- end in one bundle verdict:
  `no_candidate_ready`,
  `exactly_one_candidate_ready`, or
  `multiple_or_nonunique_candidates`.

It must not:

- add new candidate families;
- widen the opcode surface, value family, or substrate;
- reopen runtime execution.

The current expected bundle verdict is `no_candidate_ready`.

## H38 Decision Rule

`H38` remains docs-only and keeps `H36` as the preserved active
routing/refreeze packet.

Selected outcome:

- `keep_h36_freeze`

Non-selected outcome:

- `authorize_r41_origin_runtime_relevance_threat_stress_audit`

`H38` may authorize `R41` only if `F16` produces exactly one
`execution_ready` candidate on the fixed landed `R40` row pair.

If `F16` produces zero `execution_ready` candidates or more than one
non-unique candidate, `H38` must keep the freeze and name no active runtime
candidate.

## P26 Scope

`P26` is operational only.

It must:

- preserve `wip/f16-h38-p26-exec` as the current clean audit branch;
- preserve `wip/p25-f15-h37-exec` as the prior clean source branch for the
  landed `P25/F15/H37` wave;
- keep `main` untouched in this wave;
- record a promotion packet split, a worktree runbook, and a large-artifact
  policy;
- classify whether the user-mentioned
  `results/R20_d0_runtime_mechanism_ablation_matrix/probe_read_rows.json`
  belongs to the current promotion bundle.

It must not:

- authorize a merge by momentum;
- relabel dirty-tree artifacts as part of the clean source bundle;
- use artifact hygiene as a pretext to widen scientific scope.

## F17 Scope

`F17` is planning-only future-route storage after the `H38` decision.

It must:

- define when a future same-substrate packet is still discussable;
- define when to route instead to `F9`, `F11`, or publication-only work;
- keep all routes blocked until a later explicit packet makes one active.

## Required Outputs

- `F16`:
  `candidate_status_matrix.md`,
  `decision_basis.md`
- `H38`:
  standard docs-only packet set plus machine-readable `results/` summary,
  checklist, claim packet, and snapshot
- `P26`:
  `commit_split_manifest.md`,
  `main_delta_summary.md`,
  `artifact_tracking_policy.md`,
  `worktree_runbook.md`
- `F17`:
  `exit_criteria_matrix.md`,
  `route_selection_rules.md`

## Non-Goals

This wave does not authorize:

- `R41` execution by default;
- any restricted-Wasm, arbitrary `C`, or general-computer claim lift;
- hybrid planner/executor work;
- direct merge of dirty `main`.
