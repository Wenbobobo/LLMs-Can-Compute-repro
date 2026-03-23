# Release Candidate Checklist

State: `standing_gate`.

This checklist defines the minimum outward-facing sync required for a restrained
release-candidate state after the current submission-candidate bundle lock on
the current `H38` docs-only decision / `H36` preserved-active /
`P26-F16-F17-F15` current-control-support / `H37-P25`
preserved immediate-predecessor support / `H35-H34-H33-H32-H31-H30`
preserved question-selection-and-decision /
`H29` preserved-upstream-refreeze / `H27-H28`
preserved-closeout-and-pivot stack.

## Wording and scope

- [ ] `README.md` keeps the narrow endpoint and blocked non-goals explicit.
- [ ] `STATUS.md` matches the same frozen scope and the current next action
  recorded by `H38`, preserved `H36`, completed `P26`, current `F16/F17`,
  preserved `H37/P25`, and current `F15`.
- [ ] `release_summary_draft.md` remains the short public-surface source.
- [ ] `P20`, `F5`, and `F6` remain aligned with the same no-reopen
  interpretation and do not imply a new evidence wave.
- [ ] `F7`, `F8`, `F10`, `F12`, `F13`, `F14`, and `P23` remain aligned with
  that same planning-only no-reopen interpretation, while `P21/P22` stay
  preserved prior syncs, `F9` stays blocked, `F11` stays new-substrate, and
  none of them imply a new evidence wave, `R41`, merge authorization, or a
  broadened runtime family.
- [ ] No outward wording implies a new evidence wave or broader compiled scope.

## Paper-facing dependencies

- [ ] `submission_candidate_criteria.md` is satisfied on the current repo state.
- [ ] `paper_bundle_status.md`, `layout_decision_log.md`, and
  `publication_record/README.md` all describe the same `H38` current /
  `H36` preserved active / `P26-F16-F17-F15` current support /
  `H37-P25` preserved immediate-predecessor support /
  `H35-H34-H33-H32-H31-H30-H29-H27-H28` preserved current control package.
- [ ] `plans/README.md`, the saved post-`P20/F5/F6` handoff surfaces, and the
  saved post-`H34` planning-wave surface still present docs/planning
  maintenance as admissible while runtime remains inactive by default.
- [ ] `publication_record/README.md` and the saved planning-wave surfaces
  present the completed `F16/H38/P26/F17` wave, the preserved `P25/F15/H37`
  wave, the preserved `F7/F8/P21` wave, the preserved `F10/P22` bridge wave,
  and the preserved `F12/F13/F14/P23` family-first wave while keeping `F9`
  blocked and `F11` new-substrate.
- [ ] The blocked-blog rule remains explicit in both `blog_release_rules.md`
  and `blog_outline.md`.

## Machine-audited guards

- [ ] `results/P1_paper_readiness/summary.json` still reports `10/10` ready
  items on the frozen scope.
- [ ] `results/H38_post_f16_runtime_relevance_reopen_decision_packet/summary.json`
  reports the current docs-only decision packet, `keep_h36_freeze`, and no
  active downstream runtime lane.
- [ ] `results/P26_post_h37_promotion_and_artifact_hygiene_audit/summary.json`
  reports the completed operational audit lane and `audit_only` merge posture.
- [ ] `results/H37_post_h36_runtime_relevance_decision_packet/summary.json`
  reports the preserved prior docs-only decision packet and
  `keep_h36_freeze`.
- [ ] `results/H36_post_r40_bounded_scalar_family_refreeze/summary.json`
  reports the preserved active routing/refreeze packet without widening scope.
- [ ] `results/P25_post_h36_clean_promotion_prep/summary.json` reports the
  preserved prior operational prep lane and `prepare_only` merge posture.
- [ ] `results/H35_post_p23_bounded_scalar_family_runtime_decision_packet/summary.json`
  records the preserved prior docs-only bounded-scalar runtime authorization
  packet.
- [ ] `results/R40_origin_bounded_scalar_locals_and_flags_gate/summary.json`
  records the completed bounded-scalar runtime gate and does not imply broader
  value semantics.
- [ ] `results/H34_post_r39_later_explicit_scope_decision_packet/summary.json`
  records the preserved earlier freeze-complete-for-now control packet.
- [ ] `results/H32_post_r38_compiled_boundary_refreeze/summary.json`
  reports the preserved earlier compiled-boundary routing/refreeze packet
  without widening scope.
- [ ] `results/R39_origin_compiler_control_surface_dependency_audit/summary.json`
  reports one declared helper-body permutation with target renumbering only
  and does not imply broader compiler support.
- [ ] `results/H33_post_h32_conditional_next_question_packet/summary.json`
  records the preserved prior docs-only question-selection packet.
- [ ] `results/R38_origin_compiler_control_surface_extension_gate/summary.json`
  reports one richer same-substrate compiled control family only and does not
  imply broader compiler support.
- [ ] `results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json`
  records the preserved explicit later-decision packet.
- [ ] `results/H30_post_r36_r37_scope_decision_packet/summary.json`
  records the preserved prior compiled-boundary refreeze packet without
  widening scope.
- [ ] `results/R37_origin_compiler_boundary_gate/summary.json` reports one
  tiny compiled-boundary gate only and does not imply broader compiler support.
- [ ] `results/H29_refreeze_after_r34_r35_origin_core_gate/summary.json`
  remains available as the preserved upstream Origin-core refreeze packet.
- [ ] `results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`
  still records the preserved negative same-endpoint closeout.
- [ ] `results/H28_post_h27_origin_core_reanchor_packet/summary.json` still
  records the preserved Origin-core pivot packet.
- [ ] `results/R36_origin_long_horizon_precision_scaling_gate/summary.json`
  still records the preserved narrow precision-boundary follow-up.
- [ ] `results/H15_refreeze_and_decision_sync/summary.json` reports zero
  blocked items on the preserved earlier refrozen control surface.
- [ ] `results/H14_core_first_reopen_guard/summary.json` reports zero blocked
  items on the preserved earlier core-first reopen control surface.
- [ ] `results/H13_post_h12_governance_stage_health/summary.json` reports zero
  blocked items on the preserved governance/runtime handoff.
- [ ] `results/P5_public_surface_sync/summary.json` reports zero blocked items.
- [ ] `results/P5_callout_alignment/summary.json` reports zero blocked rows.
- [ ] `results/H2_bundle_lock_audit/summary.json` reports zero blocked items.
- [ ] `results/release_worktree_hygiene_snapshot/summary.json` classifies
  whether the current worktree blocks an outward sync commit.
- [ ] `results/release_preflight_checklist_audit/summary.json` reports
  `docs_and_audits_green` with zero blocked items.
- [ ] `results/V1_full_suite_validation_runtime_timing_followup/summary.json`
  reports `healthy_but_slow` with zero timed-out files.

## Release hygiene

- [ ] `results/release_worktree_hygiene_snapshot/summary.json` is checked
  before the outward sync commit.
- [ ] No local-only source material under `docs/Origin/` or `docs/origin/`
  appears in public-facing docs or release notes.
- [ ] Blog work remains blocked unless this checklist and
  `blog_release_rules.md` are both satisfied in full.
