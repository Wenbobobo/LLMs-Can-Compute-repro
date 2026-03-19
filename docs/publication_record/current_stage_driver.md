# Current Stage Driver

## Active driver

The current active stage is:

- `H3_stage_driver_consolidation_and_plan_index`
- `P10_submission_packet_and_archival_repro_bundle`
- `P11_manuscript_targeting_and_derivative_controls`
- `F1_future_evidence_playbooks`

This stage starts from the locked submission-candidate bundle and restrained
release-candidate checkpoint created by `P8` and `P9`.

## Execution order

1. Preserve the full current-round plan in `tmp/`.
2. Clarify which docs are active drivers, standing gates, dormant protocols,
   and historical-complete references.
3. Build a venue-agnostic submission/archive packet and audit it.
4. Prepare derivative-only writing material without widening scope.
5. Pre-author future `E1` patch playbooks without activating them.

## Standing gates

- `results/P1_paper_readiness/summary.json`
- `results/P5_public_surface_sync/summary.json`
- `results/P5_callout_alignment/summary.json`
- `results/H2_bundle_lock_audit/summary.json`
- `pytest -q`
- `git diff --check`

## Dormant reopen path

No `E1` patch lane is active on the current repo state. Any future reopen must
pass through `docs/publication_record/conditional_reopen_protocol.md`.

## Historical-complete references

- `docs/publication_record/paper_package_plan.md`
- `docs/milestones/P8_submission_candidate_and_bundle_lock/result_digest.md`
- `docs/milestones/P9_release_candidate_and_public_surface_freeze/result_digest.md`
- `docs/milestones/H2_release_hygiene_and_audit_promotion/result_digest.md`
