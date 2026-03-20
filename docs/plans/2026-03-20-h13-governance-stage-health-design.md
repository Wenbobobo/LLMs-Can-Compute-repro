# H13 Governance Stage-Health Design

## Goal

Add one machine-readable `H13` stage-health audit that collapses the current
governance-only control chain into a single unattended entrypoint.

## Why this is the next useful step

The current post-`H12` repo state is intentionally governance-only:

- `H12` is the latest completed same-endpoint scientific checkpoint;
- `H13` keeps that checkpoint explicit without reopening scope;
- `V1` classifies the slow full-suite validation gate operationally;
- `release_preflight_checklist_audit` keeps outward sync machine-audited;
- `P10` keeps the archive handoff green;
- `H10/H11/H8/H6` preserve the packet and older baselines.

These controls already exist, but unattended continuation still requires
reading several summaries manually before deciding whether the stage is healthy
enough to keep running without intervention.

## Non-goal

Do not create a new science lane, a new claim layer, or a replacement for the
underlying standing guards. This audit should summarize them, not outrank them.

## Selected approach

Create one top-level `H13` stage-health export that reads:

- `docs/publication_record/current_stage_driver.md`
- `docs/milestones/H13_post_h12_rollover_and_next_stage_staging/`
- `results/V1_full_suite_validation_runtime_audit/summary.json`
- `results/V1_full_suite_validation_runtime_timing_followup/summary.json`
- `results/H10_r7_reconciliation_guard/summary.json`
- `results/H11_post_h9_mainline_rollover_guard/summary.json`
- `results/H8_driver_replacement_guard/summary.json`
- `results/H6_mainline_rollover_guard/summary.json`
- `results/P5_public_surface_sync/summary.json`
- `results/H2_bundle_lock_audit/summary.json`
- `results/release_preflight_checklist_audit/summary.json`
- `results/P10_submission_archive_ready/summary.json`
- `results/M7_frontend_candidate_decision/decision_summary.json`

The new audit should pass only when the current stage is still governance-only,
the preserved baseline guards are green, `V1` remains bounded and healthy but
slow, outward sync remains green, archive handoff remains green, and `M7`
still blocks widening.

## Doc updates

Synchronize the new audit into:

- `README.md` as a `Start Here` entry and regeneration command;
- `STATUS.md` as the first unattended `H13` control reference;
- `docs/publication_record/current_stage_driver.md` as a standing gate and
  active bounded lane;
- `docs/milestones/H13_post_h12_rollover_and_next_stage_staging/` so the
  milestone records its own control surface;
- `docs/publication_record/experiment_manifest.md` and `scripts/README.md`.

## Acceptance

- the new `H13` stage-health summary is green on the current repo state;
- no exporter dependency cycle is introduced;
- future unattended rounds can check one summary first, then drill down only if
  that summary reports blocked items.
