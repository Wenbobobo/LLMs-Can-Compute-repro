# Submission Packet Index

Status: venue-agnostic packet index for the locked checkpoint. This document is
downstream of `manuscript_bundle_draft.md` and does not widen scientific scope.

## Canonical manuscript bundle

- `manuscript_bundle_draft.md`
- `manuscript_section_map.md`
- `figure_table_narrative_roles.md`
- `caption_candidate_notes.md`
- `main_text_order.md`

## Canonical appendix and companion bundle

- `appendix_companion_scope.md`
- `appendix_boundary_map.md`
- `appendix_stub_notes.md`
- `experiment_manifest.md`
- `paper_bundle_status.md`

## Canonical claim and boundary ledgers

- `claim_ladder.md`
- `claim_evidence_table.md`
- `negative_results.md`
- `threats_to_validity.md`
- `review_boundary_summary.md`

## Canonical control docs

- `current_stage_driver.md`
- `planning_state_taxonomy.md`
- `submission_candidate_criteria.md`
- `release_candidate_checklist.md`
- `conditional_reopen_protocol.md`

## Required audit anchors

- `results/P1_paper_readiness/summary.json`
- `results/H21_refreeze_after_r22_r23/summary.json`
- `results/H20_post_h19_mainline_reentry_and_hygiene_split/summary.json`
- `results/R22_d0_true_boundary_localization_gate/summary.json`
- `results/R23_d0_same_endpoint_systems_overturn_gate/summary.json`
- `results/H19_refreeze_and_next_scope_decision/summary.json`
- `results/H15_refreeze_and_decision_sync/summary.json`
- `results/H14_core_first_reopen_guard/summary.json`
- `results/H13_post_h12_governance_stage_health/summary.json`
- `results/V1_full_suite_validation_runtime_audit/summary.json`
- `results/V1_full_suite_validation_runtime_timing_followup/summary.json`
- `results/release_worktree_hygiene_snapshot/summary.json`
- `results/release_preflight_checklist_audit/summary.json`
- `results/P5_public_surface_sync/summary.json`
- `results/P5_callout_alignment/summary.json`
- `results/H2_bundle_lock_audit/summary.json`
- `results/P10_submission_archive_ready/summary.json`

## Regeneration anchors

- `scripts/export_p1_figure_table_sources.py`
- `scripts/render_p1_paper_artifacts.py`
- `scripts/export_p1_paper_readiness.py`
- `scripts/export_h20_post_h19_mainline_reentry_and_hygiene_split.py`
- `scripts/export_r22_d0_true_boundary_localization_gate.py`
- `scripts/export_r23_d0_same_endpoint_systems_overturn_gate.py`
- `scripts/export_h21_refreeze_after_r22_r23.py`
- `scripts/export_h19_refreeze_and_next_scope_decision.py`
- `scripts/export_h15_refreeze_and_decision_sync.py`
- `scripts/export_h14_core_first_reopen_guard.py`
- `scripts/export_h13_post_h12_governance_stage_health.py`
- `scripts/export_v1_full_suite_validation_runtime_audit.py`
- `scripts/export_v1_full_suite_validation_runtime_timing_followup.py`
- `scripts/export_release_worktree_hygiene_snapshot.py`
- `scripts/export_release_preflight_checklist_audit.py`
- `scripts/export_p5_public_surface_sync.py`
- `scripts/export_p5_callout_alignment.py`
- `scripts/export_h2_bundle_lock_audit.py`
- `scripts/export_p10_submission_archive_ready.py`

## Restricted-source boundary

This packet is public-safe. It does not depend on any local-only source
material. Private planning sources may exist outside the packet, but they are
not part of the public submission/archive handoff.

## Handoff rule

Venue-specific formatting may fork from this packet, but that formatting must
not widen claims, activate an `E1` patch lane, or outrun the locked manuscript
bundle. The current packet is anchored on landed `H21` rather than the
preserved prior `H19` refreeze.
