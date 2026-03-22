# Activation Matrix

`F2` is planning-only. It does not authorize any widened run by itself. The
matrix below exists so a later agent can decide whether frontier review is even
plan-worthy without rereading the current `H27 -> H32` Origin-core packet and
the preserved same-endpoint control stack.

## Trigger Matrix

| Condition | Current `H32` active state | Required for any future frontier-plan draft | Why it still matters |
| --- | --- | --- | --- |
| Origin-core evidence chain is coherent | satisfied | keep satisfied | `H28`, `H29`, `R36`, `R37`, `H30`, `H31`, `R38`, and `H32` now describe one narrow append-only / exact-retrieval / small-VM story rather than a broad compiler claim |
| The current compiled-boundary line is explicitly delimited | satisfied | keep satisfied | `H30/H31/R38/H32` name one admitted extension row, one boundary probe, the same opcode surface, and the standing no-widening rule |
| A concrete post-`H32` substrate gap is isolated | satisfied | keep satisfied through `H33` and any future `R39` execution discipline | `H33` now isolates one narrow same-substrate question instead of letting post-`H32` work drift into broad compiled momentum |
| Compiler/runtime boundary remains claim-relevant | satisfied | keep satisfied | the current materials still identify "compiler does all the work" and "accelerating only the easy part" as the main unresolved scientific risks after `H32` |
| Broader compiled or new-substrate work is explicitly reauthorized | not satisfied | a later explicit packet would need to replace the standing `H32` no-widening state with one named new question | `H32` ends at `new_plan_required_before_any_further_compiled_boundary_or_scope_lift` |
| Systems or frontier story changes materially | not satisfied | a later packet would need to move beyond the current narrow Origin-core result in a coherent way | the project still does not have a materially positive broad systems or general-computer story |
| The active downstream order is exhausted or explicitly superseded | not satisfied | `R39_origin_compiler_control_surface_dependency_audit` would need to run and be interpreted by a later explicit packet first | `F2` must stay downstream of `H33` and must not be used to skip over the current same-substrate audit requirement |

## Non-goals

- Do not treat `H32` or `R38` as implicit authorization for another compiled
  family, a new substrate, or frontier review.
- Do not treat the saved post-`H33` `R39` design or the `R39` scaffold as if
  they were already landed evidence.
- Do not restate a planning matrix as if it were a landed experimental result.
- Do not use `F2` to backdoor a broader “LLMs are computers” claim.

## Minimum Evidence Bundle

Any later frontier-plan draft should require, at minimum:

1. the preserved same-endpoint control chain
   `results/H17_refreeze_and_conditional_frontier_recheck/summary.json`,
   `results/H19_refreeze_and_next_scope_decision/summary.json`,
   `results/H21_refreeze_after_r22_r23/summary.json`,
   `results/H23_refreeze_after_r26_r27_r28/summary.json`,
   `results/H25_refreeze_after_r30_r31_decision_packet/summary.json`, and
   `results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`;
2. the current Origin-core packet
   `results/H28_post_h27_origin_core_reanchor_packet/summary.json`,
   `results/H29_refreeze_after_r34_r35_origin_core_gate/summary.json`,
   `results/R34_origin_retrieval_primitive_contract_gate/summary.json`,
   `results/R35_origin_append_only_stack_vm_execution_gate/summary.json`,
   `results/R36_origin_long_horizon_precision_scaling_gate/summary.json`,
   `results/R37_origin_compiler_boundary_gate/summary.json`,
   `results/H30_post_r36_r37_scope_decision_packet/summary.json`,
   `results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json`,
   `results/R38_origin_compiler_control_surface_extension_gate/summary.json`,
   and `results/H32_post_r38_compiled_boundary_refreeze/summary.json`;
3. the current downstream planning surfaces
   `docs/plans/2026-03-23-post-h32-conditional-next-packet-design.md`,
   `results/H33_post_h32_conditional_next_question_packet/summary.json`,
   `docs/plans/2026-03-23-post-h33-r39-origin-core-substrate-question-design.md`,
   `docs/milestones/R39_origin_compiler_control_surface_dependency_audit/`,
   and `docs/milestones/F3_post_h23_scope_lift_decision_bundle/decision_gate.md`;
4. the standing no-widening controls
   `results/M7_frontend_candidate_decision/decision_summary.json`;
5. the standing mixed systems gate
   `results/R2_systems_baseline_gate/summary.json` and
   `results/E1b_systems_patch/summary.json`.

## Smallest Acceptable Widened-Probe Shape

If a later explicit plan ever becomes justified, the first widened probe should
still be narrower than a new frontend or a new general compiled family:

- one explicitly named contradiction or gap tied back to the current
  `H32/H31/H30/H29` unsupported or disconfirmed rows, not a broad exploratory
  sweep;
- one small comparator set tied back to the current admitted row and boundary
  probe rather than a new endpoint family;
- one fixed success/failure criterion decided before execution;
- one explicit stop condition that prevents an open-ended repair loop.
