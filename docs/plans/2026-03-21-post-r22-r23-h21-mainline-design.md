# 2026-03-21 Post-R22 R23 H21 Mainline Design

## Summary

The scientific target remains narrow and reproduction-first. The project is
still trying to validate one bounded chain:

1. append-only traces can encode deterministic execution;
2. exact latest-write / stack-like retrieval can operate on those traces;
3. those retrievals can support a tiny exact executor on the fixed `D0`
   endpoint; and
4. any systems claim must be earned on the same endpoint rather than inferred
   from mechanism-only evidence.

`R22` and `R23` sharpen that chain without widening it. `R22` extended the
bounded executor-boundary grid to `102/102` executed candidates and still did
not localize a failure. `R23` reran the full current positive `D0` systems
universe, kept `pointer_like_exact` exact on `25/25` rows, but still failed to
overturn the mixed systems gate: `pointer_like_exact` remained about `4.16x`
slower than the best current reference path. `H21` therefore refreezes the
repo in a stronger but still blocked state: the same-endpoint mechanism story
is clearer, the same-endpoint systems story is still mixed, and frontier
activation remains blocked.

The next phase should therefore split cleanly:

- preserved completed post-`H21` closeout:
  `P12_manuscript_and_manifest_maintenance`;
- current planning-only reopen prelay:
  `R24_d0_boundary_localization_zoom_followup`;
- parked planning-only systems notes:
  `R25_d0_same_endpoint_systems_recovery_hypotheses`;
- later outward-sync / hygiene lane:
  `P13_public_surface_sync_and_repo_hygiene`;
- still-blocked widened review discipline:
  `F2_future_frontier_recheck_activation_matrix`.

## Execution Protocol

- Save this design before any new execution batch or new worktree.
- Refresh `tmp/active_wave_plan.md` at the start of each unattended wave.
- Use isolated write sets:
  - `main`: integration, root docs, validation, commit and push.
  - `wt-p12`: optional follow-up only if a later outward/publication mismatch
    requires a small post-closeout correction.
  - `wt-r24`: boundary-first reopen planning only.
  - `wt-r25`: parked systems-recovery notes only.
  - `wt-p13`: later outward-sync and hygiene after the planning-only prelay is
    saved.
- Do not let `R24` or `R25` become backdoor execution lanes. They exist to
  save future context, not to bypass the frozen `H21` state.
- Keep path-scoped commits. Do not mix preserved `P12` closeout, future-lane
  planning, and outward-sync cleanup in one batch.

## Automatic Continue Algorithm

1. Read `tmp/active_wave_plan.md`,
   `docs/publication_record/current_stage_driver.md`, `git status --short`,
   and the current docs for `R24`, `R25`, `P13`, and preserved `P12`.
2. Keep `P12` preserved as the completed post-`H21` closeout unless a later
   outward/publication mismatch exposes a real ledger inconsistency.
3. Continue with `R24` planning-only scoping and then `R25` parked notes rather
   than opening a new runtime lane.
4. Only return to `P13` after the planning-only `R24/R25` packet is saved or a
   concrete outward-sync need appears.
5. Do not reopen science execution from inside this plan. A later explicit
   reopen plan is required first.

## Wave Order

### Wave A: `P12_manuscript_and_manifest_maintenance` preserved closeout

- Preserve the already-landed `P12` closeout outputs in `claim_ladder.md`,
  `claim_evidence_table.md`, `negative_results.md`,
  `experiment_manifest.md`, `review_boundary_summary.md`, and related
  publication ledgers.
- Keep three core consequences explicit in those preserved records:
  - `R22` strengthens bounded no-break evidence but still does not localize the
    true executor boundary;
  - `R23` strengthens exactness and mechanism relevance but fails the
    same-endpoint systems overturn goal;
  - `H21` keeps scope locked and the downstream manuscript/manifest closeout is
    now preserved-complete rather than the current active lane.
- Treat any figure/table placeholders for `R22/R23/H21` as historical mixed or
  negative evidence scaffolding, not as widened-claim staging.

Acceptance:

- already satisfied by the landed `P12` packet unless a later outward-sync doc
  reveals a concrete ledger mismatch;
- negative or mixed evidence remains first-class in the manuscript-facing
  records;
- no outward-safe prose outruns the preserved ledgers.

### Wave B: `R24_d0_boundary_localization_zoom_followup` planning-only prelay

- Draft a tighter boundary-localization follow-up around the hardest surviving
  `R21/R22` rows instead of broadening scope by momentum.
- Define one bounded candidate core built from the strongest no-break rows plus
  the nearest-to-failure hypotheses now visible after `R22`.
- Predeclare the zoom axes before execution, for example address fanout,
  horizon extension, checkpoint-braid depth, hot-address skew, read/write
  interleaving, and control-flow density.
- Specify first-fail artifacts, stop rules, and final verdict vocabulary before
  any later run.

Acceptance:

- one executable future matrix is written down;
- every proposed axis is justified from landed `R21/R22/H21` evidence;
- success, mixed, and principled-stop outcomes are explicit;
- no run is started from this planning lane.

### Wave C: `R25_d0_same_endpoint_systems_recovery_hypotheses` parked notes

- Record why `R23` remained mixed on the current endpoint rather than treating
  the result as an almost-positive.
- Decompose the same-endpoint systems gap into concrete hypotheses such as
  fixed overhead, retrieval-total concentration, comparator choice, or bounded
  runtime-path inefficiencies.
- Separate hypotheses that are still same-endpoint and scientifically honest
  from ideas that would secretly widen scope.
- Predefine what later evidence would count as `systems_materially_positive`
  versus another `systems_still_mixed` outcome.

Acceptance:

- hypotheses, thresholds, and disconfirmers are written explicitly;
- the mixed `R23` result remains claim-bearing;
- no repair loop or execution lane is opened here.

### Wave D: `P13_public_surface_sync_and_repo_hygiene`

- Keep `P13` limited to outward-sync hygiene and commit splitting.
- Only run it after the preserved `P12` closeout and the planning-only
  `R24/R25` packet are both saved.
- Keep future outward commits reviewable and path-scoped.

Acceptance:

- root/publication wording stays downstream of the landed `H21` evidence;
- commit boundaries remain reviewable;
- no new science lane is opened inside `P13`.

## Frontier Discipline

`F2` stays planning-only. The current unsatisfied conditions are:

- `true_executor_boundary_localization`
- `current_scope_systems_story_materially_positive`
- `scope_lift_thesis_explicitly_reauthorized`

This means the next unattended effort should not drift into widened demos,
frontend resurrection, or broad “LLMs are computers” prose. The only
scientifically honest near-term default is to preserve the fixed `D0` endpoint,
keep the mixed systems result explicit, preserve the completed `P12` closeout,
and maintain only planning-level `R24/R25/F2` material until a later explicit
reopen plan exists.

## Validation

- `pytest --collect-only -q`
- `git diff --check`
- run targeted exporter tests only if the touched batch changes machine-readable
  milestone or stage-driver summaries.

## Defaults

- Stay on the current tiny typed-bytecode `D0` endpoint.
- Treat `R23` mixed/negative evidence as claim-bearing, not incidental.
- Preserve `H19` and `H20` as historical control stages underneath `H21`.
- Prefer saved plans, path-scoped commits, and worktrees before unattended
  execution continues.
