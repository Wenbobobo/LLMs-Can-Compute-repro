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
uv run python scripts/export_p5_public_surface_sync.py
uv run python scripts/export_p5_callout_alignment.py
uv run python scripts/export_h2_bundle_lock_audit.py
uv run python scripts/export_p10_submission_archive_ready.py
uv run pytest -q
```

## Integrity checks

- `results/P1_paper_readiness/summary.json` shows `10/10` ready figure/table
  items and no blocked or partial rows
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
computation, or current-scope end-to-end systems superiority.
