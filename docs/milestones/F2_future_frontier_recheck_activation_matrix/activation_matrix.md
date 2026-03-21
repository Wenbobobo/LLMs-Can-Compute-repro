# Activation Matrix

`F2` is planning-only. It does not authorize any widened run by itself. The
matrix below exists so a later agent can decide whether frontier review is even
plan-worthy without rereading the full `H19 -> H21` packet.

## Trigger Matrix

| Condition | Current post-`H21` state | Required for any future frontier-plan draft | Why it still matters |
| --- | --- | --- | --- |
| Same-endpoint runtime packet is coherent | satisfied | keep satisfied | `H19`, `R22`, `R23`, and `H21` now describe one bounded same-endpoint story rather than conflicting partial follow-ups |
| Mechanism story is claim-relevant | satisfied | keep satisfied | `R20` shows the target path stays exact while bounded negative controls fail, and `R23` keeps the exactness/runtime comparison on the full positive `D0` systems suite explicit |
| True executor boundary is localized | not satisfied | at least one reproducible bounded failure or a principled stop reason beyond “extended grids stayed exact” | `R22` executed `102/102` planned candidates without exposing a failure, so widening now would still be underinformed |
| Current-scope systems story is materially positive | not satisfied | a later bounded lane would need to overturn the mixed systems gate on the current endpoint first | `R23` reran the full positive `D0` systems universe and still ended at `systems_still_mixed`; exactness alone is not end-to-end systems closure |
| Scope-lift thesis is explicitly re-authorized | not satisfied | a later refreeze would need to replace the standing no-widening state with an explicit new decision | `H21` keeps frontier review `planning_only_conditionally_reviewable`, not `authorized` |

## Non-goals

- Do not treat `R19` generalization, `R20` mechanism support, or `R21`
  no-break-observed status as automatic authorization for widened demos,
  frontends, or frontier headlines.
- Do not restate a planning matrix as if it were a landed experimental result.
- Do not use `F2` to backdoor a broader “LLMs are computers” claim.

## Minimum Evidence Bundle

Any later frontier-plan draft should require, at minimum:

1. the frozen inputs `results/H17_refreeze_and_conditional_frontier_recheck/summary.json`,
   `results/H18_post_h17_mainline_reopen_guard/summary.json`, and
   `results/H19_refreeze_and_next_scope_decision/summary.json`;
2. the landed same-endpoint packet
   `results/R19_d0_pointer_like_surface_generalization_gate/summary.json`,
   `results/R20_d0_runtime_mechanism_ablation_matrix/summary.json`, and
   `results/R21_d0_exact_executor_boundary_break_map/summary.json`;
3. the landed post-`H19` follow-up packet
   `results/H20_post_h19_mainline_reentry_and_hygiene_split/summary.json`,
   `results/R22_d0_true_boundary_localization_gate/summary.json`,
   `results/R23_d0_same_endpoint_systems_overturn_gate/summary.json`, and
   `results/H21_refreeze_after_r22_r23/summary.json`;
4. the standing no-widening control
   `results/M7_frontend_candidate_decision/decision_summary.json`;
5. the standing mixed systems gate
   `results/R2_systems_baseline_gate/summary.json` and
   `results/E1b_systems_patch/summary.json`.

## Smallest Acceptable Widened-Probe Shape

If a later explicit plan ever becomes justified, the first widened probe should
still be narrower than a new frontend:

- one explicitly named contradiction or gap, not a broad exploratory sweep;
- one small comparator set tied back to `H21` unsupported/disconfirmed rows;
- one fixed success/failure criterion decided before execution;
- one explicit stop condition that prevents an open-ended repair loop.
