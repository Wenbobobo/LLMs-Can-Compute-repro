# 2026-03-23 Post-H34 F7/F8/P21 Planning-Wave Design

This design captures the first planning-only wave after the landed
`H34_post_r39_later_explicit_scope_decision_packet` interpretation.

The key point is unchanged: `H32` remains the active routing packet,
`H34` remains the current docs-only control packet, and there is still
no active downstream runtime lane.

## Why This Wave Exists

`P20`, `F5`, and `F6` closed the immediate post-`H34` handoff:

- the paper-facing bundle now terminates on the landed `H34` state;
- the contradiction scout concludes `no_reopen_candidate_survives`;
- docs/planning maintenance remains admissible while runtime stays inactive.

That closeout leaves one planning gap, not one missing runtime lane:

- future same-substrate reopen criteria are still spread across
  `F5` helper documents rather than preserved as one mechanical packet template;
- the Origin article and later discussion materials still point to broader
  long-horizon ambitions that should be stored explicitly without being
  misread as current authorization;
- the control surfaces should say which planning-only follow-ons are now
  admissible so later agents do not reopen runtime by momentum.

## Wave Structure

### `F7_post_h34_reopen_trigger_specification_bundle`

Purpose:

- translate the landed `F5` no-reopen conclusion into one mechanical
  contradiction/reopen specification bundle.

Required outputs:

- `trigger_taxonomy.md`
- `reopen_packet_template.md`
- `candidate_registry.md`

Constraints:

- do not authorize a new same-substrate runtime lane;
- preserve `no_reopen_candidate_survives`;
- require any future reopen packet to predeclare contradiction, comparator set,
  success/failure criterion, stop condition, and scope guard.

### `F8_post_h34_beyond_origin_bridge_roadmap`

Purpose:

- store the broader scientific target suggested by `docs/Origin` and the later
  deep discussions without relabeling those ambitions as current evidence.

Required outputs:

- `scientific_target_ladder.md`
- `origin_to_repo_bridge.md`
- `future_family_matrix.md`

Constraints:

- distinguish clearly between:
  current supported Origin-core claims,
  planning-only near/mid-term roadmap families,
  and blocked or new-substrate long-horizon ambitions;
- keep all future family storage inactive by default.

### `F9` / `F10` / `F11` inactive roadmap storage

These directories exist only so future planning work has preserved storage:

- `F9_post_h34_restricted_wasm_semantic_boundary_roadmap`
- `F10_post_h34_executor_value_comparator_matrix`
- `F11_post_h34_hybrid_planner_executor_bridge_roadmap`

They are not active waves, not admitted runtime lanes, and not evidence.

### `P21_post_h34_planning_surface_sync`

Purpose:

- sync the top-level control surfaces so they describe the current
  planning-only follow-on wave accurately.

Required outputs:

- `current_stage_driver.md`
- `tmp/active_wave_plan.md`
- minimal `README.md` / `STATUS.md` / index updates

## Execution Rules

- start from a clean successor worktree forked from `wip/p20-h34-resync`;
- do not develop on dirty `main`;
- do not merge back into `main` by momentum;
- keep `H32/H34` as the live control state;
- keep `F2` planning-only, `F3` blocked, and `R29` blocked;
- do not create `H35`, `R40`, or any new runtime packet by default.

## Acceptance

- `F7` makes future reopen admissibility mechanical and preserves the current
  `no_reopen_candidate_survives` conclusion.
- `F8` preserves a beyond-Origin roadmap without converting roadmap items into
  current authorization.
- `F9/F10/F11` exist only as inactive roadmap storage.
- `P21` updates the control surfaces so later agents can see that the current
  admissible work is planning-only `F7/F8` plus docs-only sync, while runtime
  remains inactive.
