# 2026-03-21 Post-H19 Mainline Reentry Design

## Summary

The scientific target remains narrow and reproduction-first. `H19` already
froze one stronger same-endpoint `D0` packet:

- `R19` confirmed same-endpoint runtime generalization inside the declared
  admitted-plus-heldout envelope;
- `R20` supported the mechanism with claim-relevant negative-control failures;
- `R21` did not find a failure inside its bounded executor grid.

That result is strong enough to keep the mainline moving, but not strong
enough to widen scope. Two frontier-activation conditions remain unsatisfied:

1. the true executor boundary is still not localized; and
2. the current-scope systems story is still mixed rather than materially
   positive.

The next wave should therefore stay entirely inside the current tiny
typed-bytecode `D0` endpoint and do three things in order:

1. isolate the mixed dirty tree into reviewable buckets;
2. run one harder executor-boundary localization lane and one same-endpoint
   systems-overturn lane in parallel;
3. refreeze the result into one new machine-readable state before any later
   outward sync.

## Execution Protocol

- Save this plan before implementation work starts and refresh
  `tmp/active_wave_plan.md`.
- Keep `H19_refreeze_and_next_scope_decision` as the current frozen scientific
  input until `H21_refreeze_after_r22_r23` lands.
- Use isolated write sets:
  - `main`: integration, validation, final commit and push.
  - `wt-h20`: `H20` hygiene split and reentry guard only.
  - `wt-r22`: `R22` boundary localization only.
  - `wt-r23`: `R23` systems overturn gate only.
  - `wt-p12`: `P12` claim/evidence/manifest upkeep only.
- Do not mix prior-wave closeout, new runtime science, and outward sync in one
  commit.
- Do not widen the endpoint, frontend surface, or claim wording in this wave.

## Wave Order

### Wave 0: `H20_post_h19_mainline_reentry_and_hygiene_split`

- Save this design and refresh `tmp/active_wave_plan.md`.
- Scaffold `H20`, `R22`, `R23`, and `H21`.
- Export one machine-readable `H20` reentry guard that records:
  - `H19` as the frozen input;
  - the current dirty-tree release block;
  - the required worktree split; and
  - the downstream order `H20 -> R22 -> R23 -> H21 -> P13`.
- Treat the current tree as three explicit buckets:
  - prior-wave `H18/H19/P13` closeout and guarded doc sync;
  - next-wave runtime science for `R22/R23/H21`;
  - background ledger upkeep for `P12`.

Acceptance:

- `H19` remains the current frozen stage;
- `H20` exports a machine-readable reentry/hygiene summary;
- `R22`, `R23`, and `H21` milestone directories exist with actionable todos;
- the current dirty tree is described as an operational split problem rather
  than a scientific contradiction.

### Wave 1: `R22_d0_true_boundary_localization_gate`

- Extend the current executor grid beyond `R21` without changing the endpoint
  semantics.
- Prioritize the hardest currently admitted families and the most
  failure-likely address/horizon/checkpoint combinations.
- Export positive rows, failure rows, and first-fail diagnostics.
- End with exactly one verdict:
  - `first_boundary_failure_localized`,
  - `no_failure_in_extended_grid`, or
  - `resource_limited_without_failure`.

Acceptance:

- all carried-forward positive controls remain exact;
- any new failure is reproducible and localized to one first-fail digest;
- no repair lane is opened inside `R22`.

### Wave 2: `R23_d0_same_endpoint_systems_overturn_gate`

- Re-run the systems gate on the same positive `D0` suites using the landed
  `pointer_like_exact` runtime as a first-class candidate.
- Compare:
  - current best reference/spec path;
  - lowered `exec_trace`;
  - imported `linear_exact`;
  - imported current accelerated;
  - current `pointer_like_exact`.
- Keep exactness, full-program runtime, per-step runtime, and component
  attribution explicit.
- End with exactly one verdict:
  - `systems_materially_positive`,
  - `systems_still_mixed`, or
  - `systems_negative_under_same_endpoint`.

Acceptance:

- all selected positive rows remain exact under every exact-designated path;
- the systems verdict is driven by measured runtime rather than prose;
- no widened frontend or compiled-language claim appears.

### Wave 3: `H21_refreeze_after_r22_r23`

- Freeze the `R22/R23` outcomes into one machine-readable post-`H19` state.
- Reclassify `supported_here`, `unsupported_here`, and `disconfirmed_here`.
- Re-evaluate the `F2` trigger matrix without executing any widened probe.
- Keep README/root/publication outward wording downstream until this refreeze
  lands cleanly.

Acceptance:

- `H21` lands only after `R22` and `R23` each export an explicit verdict;
- the `F2` unsatisfied conditions are either narrowed or explicitly unchanged;
- no widened scope is implied by the refreeze itself.

## Background Lanes

### `P12_manuscript_and_manifest_maintenance`

- Keep `docs/claims_matrix.md`, `docs/risk_register.md`,
  `docs/publication_record/claim_evidence_table.md`, and
  `docs/publication_record/experiment_manifest.md` aligned with landed
  evidence.
- Record `R22/R23/H21` implications without upgrading claim scope.
- Do not convert manuscript maintenance into public-surface sync.

### `P13_public_surface_sync_and_repo_hygiene`

- Keep commit split and reviewability as the only remaining open item from the
  `H19` closeout.
- Do not expand `P13` into a new science lane.

## Validation

- `H20`: run its focused exporter tests plus `git diff --check`.
- `R22`: rerun exactness regression on carried-forward positives and repeat any
  discovered first-fail case deterministically.
- `R23`: rerun systems profiles with fixed seeds/environment and verify that
  exact-designated paths stay exact.
- `H21`: rerun targeted guard and outward-control exporters after the refreeze
  lands.

## Defaults

- Stay on the current tiny typed-bytecode `D0` endpoint.
- Do not reopen `F2` as an active experimental lane.
- Do not let paper/blog/README wording outrun landed evidence.
- Treat negative or null results in `R22` and `R23` as first-class outputs.
