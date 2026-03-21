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

## Immediate Execution Order

### Wave 0: `H21` closeout and doc sync

- Save this design before new edits or new worktrees.
- Refresh `tmp/active_wave_plan.md`.
- Align milestone docs, root docs, and publication ledgers to the landed
  `H21` state.
- Re-export `H21` once the docs reflect the landed state so the machine summary
  no longer reports stale milestone-doc blockers.

Acceptance:

- `results/H21_refreeze_after_r22_r23/summary.json` reports zero blocked items;
- root/publication docs no longer treat `H19 -> P13` as the current state;
- the mixed `R23` result is recorded explicitly rather than softened.

### Wave 1: `P12_manuscript_and_manifest_maintenance`

- Update `claim_ladder.md`, `claim_evidence_table.md`,
  `negative_results.md`, `experiment_manifest.md`,
  `review_boundary_summary.md`, and related publication ledgers.
- Record three core consequences:
  - `R22` strengthens bounded no-break evidence but still does not localize the
    true executor boundary;
  - `R23` strengthens exactness and mechanism relevance but fails the
    same-endpoint systems overturn goal;
  - `H21` keeps scope locked and routes the next priority to conservative
    manuscript/manifest maintenance.
- Reserve any figure/table placeholders for `R22/R23/H21` as negative-or-mixed
  evidence, not as widened-claim staging.

Acceptance:

- claim/evidence ledgers reflect `R22/R23/H21`;
- negative or mixed evidence is first-class in the manuscript-facing records;
- no public-safe prose outruns the new ledgers.

### Wave 2: `P13_public_surface_sync_and_repo_hygiene`

- Keep `P13` limited to outward-sync hygiene and commit splitting.
- Only run it after `P12` has stabilized the post-`H21` ledgers.
- If the tree is still too mixed for a clean split, keep recording the split as
  blocked rather than forcing a low-quality commit.

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
keep the mixed systems result explicit, and wait for a later explicit plan
before any new mainline science beyond `P12/P13/F2`.

## Validation

- `uv run pytest tests/test_export_r23_d0_same_endpoint_systems_overturn_gate.py tests/test_export_h21_refreeze_after_r22_r23.py -q`
- `uv run python scripts/export_h21_refreeze_after_r22_r23.py`
- `pytest --collect-only -q`
- `git diff --check`

## Defaults

- Stay on the current tiny typed-bytecode `D0` endpoint.
- Treat `R23` mixed/negative evidence as claim-bearing, not incidental.
- Preserve `H19` and `H20` as historical control stages underneath `H21`.
- Prefer path-scoped commits and worktrees once the current doc batch is saved.
