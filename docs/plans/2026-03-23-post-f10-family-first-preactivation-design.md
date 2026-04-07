# 2026-03-23 Post-F10 Family-First Preactivation Design

This design captures the next docs-only planning wave after the completed
`F10_post_h34_executor_value_comparator_matrix` bridge and the completed
`P22_post_f10_planning_surface_sync`.

The control point is unchanged:

- `H32_post_r38_compiled_boundary_refreeze` remains the active routing packet;
- `H34_post_r39_later_explicit_scope_decision_packet` remains the current
  docs-only control packet;
- there is still no active downstream runtime lane.

## Why This Wave Exists

`F10` solved the value-family classification gap, but only at family-matrix
granularity. The repo can now say that the nearest richer same-substrate family
is `bounded scalar locals and flags`, but it still lacks one decision-complete
preactivation bundle that states:

- the exact bounded semantics of that family;
- how the family would remain observable in append-only trace or final-state
  projections;
- what lowering and comparator rules would have to hold before the family could
  ever become discussable beyond vocabulary;
- what contradiction shape would be strong enough to justify a future explicit
  reopen packet on that family.

That makes the next gap a planning-interface gap, not a runtime gap.

## Wave Structure

### `F12_post_f10_origin_claim_delta_reanchor_bundle`

Purpose:

- reanchor the origin article plus the three discussion files to the current
  `H34/F10/P22` state;
- replace the earlier `F4` matrix as the current origin-facing canonical delta
  surface while preserving `F4` historically.

Required outputs:

- `claim_delta_matrix.md`
- `scientific_goal_stack.md`
- `repro_gap_ladder.md`
- `origin_material_index.md`

### `F13_post_f12_bounded_scalar_value_family_spec`

Purpose:

- take the nearest same-substrate richer family already identified by `F10`
  and write it up as one bounded preactivation spec.

Required outputs:

- `family_scope.md`
- `reference_semantics.md`
- `projection_and_observability.md`
- `lowering_invariants.md`
- `comparator_matrix.md`
- `boundary_probe.md`
- `success_failure_rule.md`
- `stop_conditions.md`

Constraints:

- choose exactly one family: `bounded scalar locals and flags`;
- stay same-substrate, same-opcode-surface, and planning-only;
- do not widen into typed records, symbolic references, external effects, or
  planner-mediated values.

### `F14_post_f13_conditional_reopen_readiness_bundle`

Purpose:

- convert the strongest remaining same-substrate scientific cautions into one
  conditional future explicit-packet blueprint without authorizing it now.

Required outputs:

- `threat_model.md`
- `candidate_perturbation_catalog.md`
- `admissibility_gate.md`
- `decision_packet_blueprint.md`
- `runtime_audit_blueprint.md`
- `execution_guardrails.md`

Constraints:

- keep `runtime_irrelevance_via_compiler_helper_overencoding` and
  `fast_path_only_helps_the_easy_part` as the only two active threat families;
- permit a future explicit packet only if one same-row, same-opcode,
  same-substrate candidate becomes uniquely isolated;
- do not create an active `H35` or `R40` lane by wording alone.

### `P23_post_f13_planning_surface_sync`

Purpose:

- align the top-level driver, wave plan, and indexes to the new
  `F12/F13/F14` state.

Required outputs:

- `current_stage_driver.md`
- `tmp/active_wave_plan.md`
- minimal root/index/publication surface refreshes

## Execution Rules

- start from a clean successor worktree forked from `wip/f10-p22-planning`;
- do not develop on dirty `main`;
- do not merge back into dirty `main` by momentum;
- keep `H32/H34` as the live control state;
- keep `F10` as the current semantic/value bridge surface;
- keep `F13` planning-only as the current bounded family preactivation surface;
- keep `F9` blocked, `F11` new-substrate, `F2` planning-only, `F3` blocked,
  and `R29` blocked;
- do not create `H35`, `R40`, restricted-Wasm runtime work, or hybrid runtime
  work in this wave.

## Acceptance

- `F12` becomes the current origin-facing canonical delta surface.
- `F13` specifies one bounded scalar-local-and-flag family in a way that later
  packets can evaluate without reopening design ambiguity.
- `F14` defines a future contradiction-driven packet shape and audit shape
  without authorizing either one.
- `P23` updates the control surfaces so later agents can see that the current
  admissible work is still planning-only, now at family-first preactivation
  granularity rather than only at the `F10` family-matrix level.
