# Unattended Aggressive Multiwave Design

This design turns the current post-`M6-E` repository state into a durable
execution protocol for repeated unattended `Continue` turns.

## Scientific target

Keep the target narrow:

- append-only execution traces as the computation substrate;
- exact retrieval as the mechanism under test;
- free-running exact execution as the success criterion;
- tiny typed-bytecode `D0` as the current compiled-frontend boundary.

Do not drift into:

- “LLMs are computers” rhetoric;
- arbitrary C claims;
- demo-first frontend widening;
- treating companion diagnostics as new claim layers.

## Worktree layout

Once the dirty tree is consolidated into a clean checkpoint, use:

- `main` as the integration tree;
- `paper` worktree for `H0`, `P3`, and `P4`;
- `precision` worktree for `R1`;
- `systems` worktree for `R2`.

The helper script is `scripts/setup_unattended_worktrees.ps1`.

Default branch names:

- `wip/p3-paper-freeze`
- `wip/r1-precision-closure`
- `wip/r2-systems-gate`

## Wave order

1. `H0_repo_consolidation_and_release_hygiene`
2. `P3_paper_freeze_and_evidence_mapping`
3. `R1_precision_mechanism_closure`
4. `R2_systems_baseline_gate`
5. `M7_frontend_candidate_decision`
6. `P4_blog_release_gate`

Only after `P3`, `R1`, and `R2` close may `M7` revisit frontend widening.

## Continue protocol

Every unattended continuation should do the following:

1. Read `STATUS.md`, `tmp/2026-03-18-next-stage-plan.md`, and the current
   milestone `todo.md` files.
2. Finish the earliest unblocked wave before starting a later one.
3. Prefer three parallel lanes:
   - publication/doc sync;
   - precision closure;
   - systems baseline.
4. For every batch, leave behind:
   - updated milestone status/todo files;
   - artifact paths;
   - manifest entries;
   - tests or export commands that reproduce the change.
5. If a lane blocks, switch to another lane instead of idling.

## Default judgments

- Aggressive unattended time should be used to saturate experiments and ledgers,
  not to widen scope casually.
- Negative results are first-class outputs and must be written into
  `docs/publication_record/negative_results.md` or the relevant
  `blocked_hypotheses.md`.
- README/blog wording is downstream of paper-grade evidence.
- `M5` remains frozen unless the fair comparison surface changes materially.
