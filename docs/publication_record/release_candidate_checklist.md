# Release Candidate Checklist

State: `standing_gate`.

This checklist defines the minimum outward-facing sync required for a restrained
release-candidate state after the current submission-candidate bundle lock.

## Wording and scope

- [ ] `README.md` keeps the narrow endpoint and blocked non-goals explicit.
- [ ] `STATUS.md` matches the same frozen scope and current next action.
- [ ] `release_summary_draft.md` remains the short public-surface source.
- [ ] No outward wording implies a new evidence wave or broader compiled scope.

## Paper-facing dependencies

- [ ] `submission_candidate_criteria.md` is satisfied on the current repo state.
- [ ] `paper_bundle_status.md`, `layout_decision_log.md`, and
  `publication_record/README.md` all describe the same post-`P7` control
  package.
- [ ] The blocked-blog rule remains explicit in both `blog_release_rules.md`
  and `blog_outline.md`.

## Machine-audited guards

- [ ] `results/P1_paper_readiness/summary.json` still reports `10/10` ready
  items on the frozen scope.
- [ ] `results/H15_refreeze_and_decision_sync/summary.json` reports zero
  blocked items on the current refrozen control surface.
- [ ] `results/H14_core_first_reopen_guard/summary.json` reports zero blocked
  items on the preserved core-first reopen control surface.
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
