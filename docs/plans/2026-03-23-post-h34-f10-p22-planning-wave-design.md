# 2026-03-23 Post-H34 F10/P22 Planning-Wave Design

This design captures the next planning-only wave after the landed
`F7/F8/P21` post-`H34` handoff.

The key control point is unchanged:

- `H32_post_r38_compiled_boundary_refreeze` remains the active routing packet;
- `H34_post_r39_later_explicit_scope_decision_packet` remains the current
  docs-only control packet;
- there is still no active downstream runtime lane.

## Why This Wave Exists

The first post-`H34` planning wave solved three immediate problems:

- `F7` made future same-substrate reopen criteria mechanical;
- `F8` stored beyond-Origin milestone families without activating them;
- `P21` synchronized the top-level control surfaces to that no-reopen state.

One planning gap still remains. The repo now stores several future families,
but it still lacks one explicit answer to a narrower scientific question:

- what extra executor-visible value family would a broader lane actually add
  beyond the current Origin-core line;
- what semantic obligations would that richer family need to satisfy before it
  counts as a scientific delta rather than vocabulary drift;
- which future families remain blocked even after those obligations are written
  down.

That makes `F10`, not `F9` or `F11`, the next admissible planning wave.

## Wave Structure

### `F10_post_h34_executor_value_comparator_matrix`

Purpose:

- define the nearest planning-only bridge between the current Origin-core line
  and any later richer semantic family.

Required outputs:

- `value_family_matrix.md`
- `obligation_matrix.md`
- `comparator_catalog.md`
- `activation_boundary.md`

Constraints:

- stay docs-only;
- do not authorize runtime execution;
- do not relabel `F10` as a restricted-Wasm or hybrid-system lane;
- make explicit why `F9` remains `blocked_by_scope` and `F11` still
  `requires_new_substrate`.

### `F8/F9/F11` refresh

Purpose:

- refresh the saved beyond-Origin roadmap so it reflects `F10` as the current
  near-term bridge surface.

Required outputs:

- update `F8` ladder and family matrix;
- update `F9` so any later semantic-boundary family is explicitly downstream of
  `F10`;
- update `F11` so any later planner/executor bridge stays outside the current
  substrate.

### `F2_future_frontier_recheck_activation_matrix` refresh

Purpose:

- prevent any later frontier-review draft from bypassing the semantic-delta
  clarification that `F10` is supposed to provide.

Required outputs:

- refresh `README.md`, `status.md`, `activation_matrix.md`,
  `blocked_hypotheses.md`, and `artifact_index.md` so they depend on
  `H33/R39/H34` plus the completed `F10/P22` planning wave.

### `P22_post_f10_planning_surface_sync`

Purpose:

- align the driver, handoff, and entrypoint surfaces to the new `F10`-led
  planning interpretation.

Required outputs:

- `docs/publication_record/current_stage_driver.md`
- `tmp/active_wave_plan.md`
- minimal `README.md` / `STATUS.md` / publication-index / milestone-index /
  plan-index updates

## Execution Rules

- start from a clean successor worktree forked from
  `wip/f7-f8-p21-planning`;
- do not develop on dirty `main`;
- do not merge back into dirty `main` by momentum;
- keep `H32/H34` as the live control state;
- keep `F10` planning-only and comparator-only;
- keep `F9` blocked, `F11` new-substrate, `F2` planning-only, `F3` blocked,
  and `R29` blocked;
- do not create `H35`, `R40`, a restricted-Wasm execution lane, or a hybrid
  planner/executor runtime lane by wording alone.

## Acceptance

- `F10` states the smallest richer value families that would count as a real
  semantic delta beyond the current Origin-core line.
- `F10` pairs those families with explicit comparator and obligation rules.
- `F8` records `F10` as the current near-term bridge while leaving `F9/F11`
  inactive.
- `F2` cannot be used to bypass `F10`.
- `P22` updates the control surfaces so later agents can see that the current
  admissible work is still planning-only and that runtime remains inactive.
