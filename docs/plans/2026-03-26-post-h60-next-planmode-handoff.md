# 2026-03-26 Post-H60 Next Plan-Mode Handoff

## Purpose

This note is the shortest safe entrypoint for the next plan-mode pass after the
post-`H59` archive/reopen-screen wave landed cleanly.

Use it to avoid reconstructing the current repo state from older execution
waves.

## Current Locked State

The current active docs-only packet is
`H60_post_f34_next_lane_decision_packet`.

The current repo meaning is:

- the narrow positive mechanism result is real and remains worth preserving;
- the broader headline reproduction did not land;
- the current executor-value lane is closed enough to treat same-lane reopen as
  inadmissible;
- the only still-recorded future family is
  `compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route`;
- that family is planning-only and not runtime-authorized; and
- the current downstream lane remains `planning_only_or_project_stop`.

## What Just Landed

The clean worktree `D:/zWenbo/AI/wt/f34-post-h59-archive-and-reopen-screen`
now contains a complete docs/control wave:

- `P43_post_h59_repo_graph_hygiene_and_merge_map`
- `P44_post_h59_publication_surface_and_claim_lock`
- `F34_post_h59_compiled_online_retrieval_reopen_screen`
- `H60_post_f34_next_lane_decision_packet`
- `F35_post_h59_far_future_model_and_weights_horizon_log`

Validation state at handoff time:

- focused exporter tests passed: `5 passed`;
- `git diff --check` was clean;
- `P44` locked all `12/12` audited files with `blocked_count = 0`; and
- the branch is currently committed clean at
  `46c115560c782889497985f68e4eebf25b951fdc`.

## Branch And Merge Posture

- current branch: `wip/f34-post-h59-archive-and-reopen-screen`
- current worktree: `D:/zWenbo/AI/wt/f34-post-h59-archive-and-reopen-screen`
- dirty root repo remains parked separately as
  `wip/root-main-parking-2026-03-24`
- root repo `main` is not the integration target for scientific work
- merge posture remains `clean_descendant_only_never_dirty_root_main`
- this branch now tracks
  `origin/wip/f34-post-h59-archive-and-reopen-screen`

That upstream is operational only. It is not a reason to merge into dirty root
`main`.

## Hard Constraints For The Next Plan

Do not plan any of the following as the next execution wave:

- another `R62`-like executor-value microvariant on the same cost structure;
- transformed/trainable entry through `F27`, `R53`, or `R54`;
- broad Wasm or arbitrary `C` scope lift;
- any merge-back plan that assumes dirty root `main` becomes the clean source
  of truth; or
- any plan that treats GPTPro advisory material as evidence.

If a future wave is proposed, it must first beat the stop/archive option.

## Recommended Next Plan-Mode Questions

### 1. Stop-or-archive decision

The next planner should first decide whether the project has already earned its
strongest honest endpoint:

- narrow positive mechanistic reproduction;
- broader headline negative;
- executor-value lane locally falsified.

If yes, the correct next phase is archival packaging, repo hygiene, and maybe a
paper-facing partial-falsification writeup rather than another execution wave.

### 2. Conditional compiled-online route screen

If the planner believes one future route remains scientifically credible, it
should stay inside `F34`'s boundary and answer these before authorizing any
runtime:

- what exact useful-case target survives as the comparator?
- what exact cost model is materially different from `R62`?
- what simpler baselines must it beat?
- what failure conditions stop the lane immediately?
- why is this not just the current lane under a renamed implementation?

The bar should be high. A vague "attention coprocessor might help" story is not
enough.

### 3. Hygiene and integration phase

If science remains planning-only, the next plan can justify a dedicated hygiene
phase:

- branch graph and worktree normalization;
- selective push/upstream setup for clean descendant branches;
- archive-surface slimming and large-artifact policy checks; and
- later merge planning only between clean descendants, never through dirty root
  `main`.

## Recommended Reading Order

Read these first:

1. `docs/publication_record/current_stage_driver.md`
2. `tmp/active_wave_plan.md`
3. `docs/plans/2026-03-26-post-h59-archive-and-reopen-screen-design.md`
4. `docs/plans/2026-03-26-post-h59-far-future-horizon-log.md`
5. `results/H60_post_f34_next_lane_decision_packet/summary.json`
6. `results/F34_post_h59_compiled_online_retrieval_reopen_screen/summary.json`
7. `results/P44_post_h59_publication_surface_and_claim_lock/summary.json`
8. `results/P43_post_h59_repo_graph_hygiene_and_merge_map/summary.json`
9. `results/F35_post_h59_far_future_model_and_weights_horizon_log/summary.json`

Read these only after the current stack is clear:

- `docs/plans/2026-03-25-post-h59-gptpro-reinterview-dossier.md`
- `docs/Origin/QA1.md`
- `docs/Origin/QA2.md`

## Default Recommendation

Default recommendation for the next plan-mode pass:

- start from `H60`, not from older execution momentum;
- prefer stop/archive/hygiene unless a materially different compiled-online
  route can be specified concretely; and
- require a new explicit authorization packet before any runtime work resumes.
