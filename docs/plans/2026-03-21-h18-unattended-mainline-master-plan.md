# 2026-03-21 H18 Unattended Mainline Master Plan

## Summary

The scientific target remains narrow and falsifiable:

1. deterministic computation can be encoded as an append-only execution trace;
2. exact latest-write and stack-like retrieval can be implemented on that trace;
3. those retrievals can support a small exact free-running executor;
4. the current tiny typed-bytecode `D0` boundary is the only compiled endpoint
   in scope;
5. systems claims must stay honest and comparator-bounded.

`H17_refreeze_and_conditional_frontier_recheck` is the current frozen state.
`R18b` is a strong same-endpoint positive result, but it is still a narrow
comparator-only repair result. The next unattended wave should therefore stay
inside the same `D0` endpoint and answer three harder questions:

- does the pointer-like runtime result generalize inside the admitted surface;
- is the win mechanistically tied to latest-write retrieval rather than an
  implementation accident;
- where does the current exact executor stop working.

## Execution Protocol

- Save this plan before any new execution batch and refresh
  `tmp/active_wave_plan.md` at the start of each wave.
- Keep `H17` as the current frozen scientific state until `H18` exports a
  machine-readable reopen guard.
- Use isolated write sets:
  - `main`: integration, root docs, final verification, commit and push.
  - `wt-r19`: `H18` and `R19`.
  - `wt-r20`: `R20`.
  - `wt-r21`: `R21`.
  - optional `wt-f2`: `F2` and `P12`.
- Do not mix prior-wave closeout, new runtime experiments, and public-surface
  syncs in a single commit.
- Treat high-quality negative results as first-class outputs. Record them in
  the milestone docs before deciding whether to continue.

## Automatic Continue Algorithm

1. Read `tmp/active_wave_plan.md`, `STATUS.md`,
   `docs/publication_record/current_stage_driver.md`, the current wave
   milestone docs, and `git status --short`.
2. Finish the current wave before opening the next one.
3. If one lane blocks, switch to another unblocked lane in the same wave.
4. If the whole wave blocks, use the time for `F2` or `P12` rather than going
   idle.
5. Only enter the next wave after the current wave acceptance is met.

## Wave Order

### Wave 0: `H18_post_h17_mainline_reopen_and_scope_lock`

- Save the new master plan and active-wave plan.
- Scaffold `H18`, `R19`, `R20`, `R21`, `H19`, `F2`, and `P12`.
- Split the current dirty tree into:
  - prior-wave `H16-H17` sync work;
  - new mainline experiment work;
  - later public-surface sync work.
- Keep `frontier_recheck_decision = conditional_plan_required` explicit.

Acceptance:

- `H17` is still described as the frozen current state.
- the next execution order is explicit:
  `H18 -> R19 -> R20 -> R21 -> H19 -> P13`;
- all next-wave milestone directories exist with actionable todos.

### Wave 1: `R19_d0_pointer_like_surface_generalization_gate`

- Build a held-out same-endpoint matrix from the admitted `R17` surface.
- For each admitted family, add two held-out seeds or the smallest equivalent
  same-envelope variant if two seeds are unavailable.
- Compare `linear_exact`, `R17` accelerated, and `R18b` pointer-like exact on
  the original admitted rows and the held-out rows.
- Export row-level exactness, runtime ratios, and address profiles.

Acceptance:

- the original admitted `8/8` rows remain exact;
- held-out rows inside the declared envelope are either exact or explicitly
  logged as failures with first-fail artifacts;
- the lane ends with one verdict:
  `generalizes_inside_envelope`, `mixed_inside_envelope`, or
  `fails_to_generalize`.

### Wave 2: `R20_d0_runtime_mechanism_ablation_matrix`

- Compare:
  - `linear_exact`;
  - `R17` accelerated;
  - `pointer_like_exact`;
  - `pointer_like_shuffled`;
  - `address_oblivious_control`.
- Keep the sample set bounded to the admitted rows plus the most informative
  `R19` held-out rows.
- Record per-read retrieval correctness, latest-write distance, hot-address
  hit rate, and runtime decomposition.

Acceptance:

- `pointer_like_exact` stays exact where `linear_exact` is exact;
- at least one negative control breaks the speed-and-exactness combination;
- the lane ends with one verdict:
  `mechanism_supported`, `speed_only_without_mechanism_support`, or
  `mechanism_not_supported`.

### Wave 3: `R21_d0_exact_executor_boundary_break_map`

- Run a bounded boundary scan across:
  - `unique_address_count = {6, 8, 12, 16}`;
  - `horizon_multiplier = {1.0, 1.5, 2.0}`;
  - `checkpoint_depth = {baseline, plus_one}`;
  - `hot_address_skew = {baseline, flattened}`;
  - `2` deterministic seeds per grid point.
- Stop expanding any branch after two exactness failures in that branch.
- Save both positive and negative rows, plus the first-fail reason.

Acceptance:

- the lane exports an explicit boundary map;
- first-fail cases are minimized and reproducible;
- no silent repair loop is started inside `R21`.

### Wave 4: `H19_refreeze_and_next_scope_decision`

- Freeze the `R19-R21` outputs into one machine-readable state.
- Reclassify claims into `supported_here`, `unsupported_here`, and
  `disconfirmed_here`.
- Decide whether any later frontier review remains blocked or becomes
  conditionally reviewable.

Acceptance:

- `H19` becomes the new frozen state only after `R19-R21` are explicit;
- frontier review remains blocked unless the same-endpoint evidence moved
  materially in a coherent way.

### Wave 5: `P13_public_surface_sync_and_repo_hygiene`

- Update `README.md`, `STATUS.md`, and publication ledgers after `H19`.
- Split and stage commits so prior-wave closeout, runtime experiments, and
  outward-facing syncs remain reviewable.
- Keep public wording strictly downstream of the landed `H19` evidence.

### Background Lane: `F2_future_frontier_recheck_activation_matrix`

- Maintain a planning-only matrix for future frontier review.
- Define triggers, non-goals, and the minimum evidence required before any
  widened probe is even considered.
- Do not execute widened experiments in this lane.

### Background Lane: `P12_manuscript_and_manifest_maintenance`

- Keep claim ladders, evidence tables, negative-result ledgers, and experiment
  manifests aligned with the currently landed evidence.
- Do not let manuscript or README prose outrun the active evidence state.

## Validation

- At the end of each wave, run the lane-local exporter tests and any focused
  executor/runtime tests touched by that lane.
- Recheck the admitted `8/8` surface whenever `R19`, `R20`, or `R21` changes
  runtime behavior or sample composition.
- Reserve full `pytest -q` and the heavier release/preflight audits for long
  unattended windows or wave closeout.

## Defaults

- Stay on the same `D0` endpoint.
- Do not reopen `M5`, `M6`, `R13`, `R14`, `E1`, or `F1` unless current-wave
  evidence explicitly justifies it.
- Keep README, STATUS, and publication ledgers downstream of evidence.
- Treat future frontier work as conditional planning only until a later
  refreeze says otherwise.
