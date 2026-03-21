# Archival Repro Manifest

Status: archival manifest for the current locked checkpoint. This file records
what should be archived, how to regenerate core artifacts, and what must stay
out of the public bundle.

## Environment baseline

- Python `3.12`
- `uv` for environment and command orchestration
- current reproducibility summaries are generated from the repo-local virtual
  environment recorded in result JSON files
- CUDA is optional for archive readers; result bundles already record whether
  GPU support was present when exports ran

## Archive payload

- repository source under `src/`, `scripts/`, and `tests/`
- publication ledgers under `docs/publication_record/`
- milestone logs under `docs/milestones/`
- machine-readable outputs under `results/`
- top-level control surface: `README.md`, `STATUS.md`, `pyproject.toml`,
  `uv.lock`

## Canonical regeneration commands

```bash
uv sync --group dev
uv run python scripts/export_p1_figure_table_sources.py
uv run python scripts/render_p1_paper_artifacts.py
uv run python scripts/export_p1_paper_readiness.py
uv run python scripts/export_h18_post_h17_mainline_reopen_guard.py
uv run python scripts/export_r19_d0_pointer_like_surface_generalization_gate.py
uv run python scripts/export_r20_d0_runtime_mechanism_ablation_matrix.py
uv run python scripts/export_r21_d0_exact_executor_boundary_break_map.py
uv run python scripts/export_h19_refreeze_and_next_scope_decision.py
uv run python scripts/export_h20_post_h19_mainline_reentry_and_hygiene_split.py
uv run python scripts/export_r22_d0_true_boundary_localization_gate.py
uv run python scripts/export_r23_d0_same_endpoint_systems_overturn_gate.py
uv run python scripts/export_h21_refreeze_after_r22_r23.py
uv run python scripts/export_h15_refreeze_and_decision_sync.py
uv run python scripts/export_h14_core_first_reopen_guard.py
uv run python scripts/export_h13_post_h12_governance_stage_health.py
uv run python scripts/export_v1_full_suite_validation_runtime_audit.py
uv run python scripts/export_v1_full_suite_validation_runtime_timing_followup.py
uv run python scripts/export_p5_public_surface_sync.py
uv run python scripts/export_p5_callout_alignment.py
uv run python scripts/export_h2_bundle_lock_audit.py
uv run python scripts/export_release_worktree_hygiene_snapshot.py
uv run python scripts/export_release_preflight_checklist_audit.py
uv run python scripts/export_p10_submission_archive_ready.py
uv run pytest -q
```

## Integrity checks

- `results/P1_paper_readiness/summary.json` shows `10/10` ready figure/table
  items and no blocked or partial rows
- `results/H21_refreeze_after_r22_r23/summary.json` records the current
  refrozen same-endpoint state, keeps future frontier review planning-only,
  and points the next downstream lane at `P12`
- `results/H19_refreeze_and_next_scope_decision/summary.json` remains the
  preserved pre-`R22/R23` refrozen same-endpoint control state
- `results/H15_refreeze_and_decision_sync/summary.json` records the current
  preserved prior refrozen stage, leaves `R13` inactive, leaves `R14`
  unjustified, and shows zero blocked items
- `results/H14_core_first_reopen_guard/summary.json` shows zero blocked items
  on the preserved core-first reopen control surface
- `results/H13_post_h12_governance_stage_health/summary.json` shows zero
  blocked items on the preserved governance/runtime handoff
- `results/V1_full_suite_validation_runtime_audit/summary.json` records a
  successful collect-only inventory on the current suite
- `results/V1_full_suite_validation_runtime_timing_followup/summary.json`
  reports `healthy_but_slow` with zero timed-out files
- `results/release_worktree_hygiene_snapshot/summary.json` reports either
  `dirty_worktree_release_commit_blocked` or
  `clean_worktree_ready_if_other_gates_green`, and does not report
  `content_issues_present`
- `results/release_preflight_checklist_audit/summary.json` reports
  `docs_and_audits_green`
- `results/P5_public_surface_sync/summary.json` shows zero blocked items
- `results/P5_callout_alignment/summary.json` shows zero blocked rows
- `results/H2_bundle_lock_audit/summary.json` shows zero blocked items
- `results/P10_submission_archive_ready/summary.json` shows zero blocked items

## Restricted-source exclusion

Local-only source material under `docs/Origin/` and `docs/origin/` stays out of
the archival/public packet. The current public-safe docs mention those paths
only as excluded inputs, never as required release artifacts.

## Archive interpretation rule

This archive is evidence for a narrow mechanistic endpoint: append-only traces,
exact latest-write retrieval, bounded precision, and a tiny typed-bytecode
`D0` compiled boundary. It is not evidence for arbitrary C, general LLM
computation, or current-scope end-to-end systems superiority. The landed
`H21` packet strengthens same-endpoint runtime support inside the fixed `D0`
boundary, but it still does not localize the true executor boundary and still
does not overturn the mixed same-endpoint systems gate.
