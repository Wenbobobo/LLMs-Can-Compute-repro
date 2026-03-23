# Release Candidate Checklist

State: `standing_gate`.

This checklist defines the minimum outward-facing sync required for a restrained
release-candidate state after the current submission-candidate bundle lock on
the current `H32` active / `H34` docs-only current-control /
`H33-R39-H31-H30` preserved question-selection-and-decision /
`H29` preserved-upstream-refreeze / `H27-H28`
preserved-closeout-and-pivot stack.

## Wording and scope

- [ ] `README.md` keeps the narrow endpoint and blocked non-goals explicit.
- [ ] `STATUS.md` matches the same frozen scope and the current next action
  recorded by active `H32` plus current docs-only `H34`.
- [ ] `release_summary_draft.md` remains the short public-surface source.
- [ ] `P20`, `F5`, and `F6` remain aligned with the same no-reopen
  interpretation and do not imply a new evidence wave.
- [ ] `F7`, `F8`, `F10`, `F12`, `F13`, `F14`, and `P23` remain aligned with
  that same planning-only no-reopen interpretation, while `P21/P22` stay
  preserved prior syncs, `F9` stays blocked, `F11` stays new-substrate, and
  none of them imply a new evidence wave, `H35`, or a broadened runtime
  family.
- [ ] No outward wording implies a new evidence wave or broader compiled scope.

## Paper-facing dependencies

- [ ] `submission_candidate_criteria.md` is satisfied on the current repo state.
- [ ] `paper_bundle_status.md`, `layout_decision_log.md`, and
  `publication_record/README.md` all describe the same `H32` active /
  `H34` current docs-only control / `H33-R39-H31-H30-H29-H27-H28`
  preserved current control package.
- [ ] `plans/README.md`, the saved post-`P20/F5/F6` handoff surfaces, and the
  saved post-`H34` planning-wave surface still present docs/planning
  maintenance as admissible while runtime remains inactive by default.
- [ ] `publication_record/README.md` and the saved post-`H34` planning-wave
  surfaces present the preserved `F7/F8/P21` wave, the preserved `F10/P22`
  bridge wave, and the current `F12/F13/F14/P23` family-first wave while
  keeping `F9` blocked and `F11` new-substrate.
- [ ] The blocked-blog rule remains explicit in both `blog_release_rules.md`
  and `blog_outline.md`.

## Machine-audited guards

- [ ] `results/P1_paper_readiness/summary.json` still reports `10/10` ready
  items on the frozen scope.
- [ ] `results/H32_post_r38_compiled_boundary_refreeze/summary.json`
  reports the current active routing/refreeze packet without widening scope.
- [ ] `results/H34_post_r39_later_explicit_scope_decision_packet/summary.json`
  reports the current docs-only freeze-complete-for-now control packet without
  reopening a downstream runtime lane.
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
  records the current Origin-core pivot packet.
- [ ] `results/R36_origin_long_horizon_precision_scaling_gate/summary.json`
  still records the current narrow precision-boundary follow-up.
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
