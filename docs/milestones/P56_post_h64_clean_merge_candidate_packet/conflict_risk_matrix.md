# P56 Conflict Risk Matrix

| Path or surface | Risk | Source of truth | Resolution rule |
| --- | --- | --- | --- |
| `README.md` | medium | current restrained repo landing page | keep `H64` active, add `P56/P57/P58/P59` only as operational follow-through |
| `STATUS.md` | medium | current control snapshot | preserve `H64` active and keep runtime closed |
| `docs/publication_record/current_stage_driver.md` | high | `P59` control sync | let `P59` own the final wording |
| `docs/publication_record/*.md` release and archive surfaces | high | `P57/P58` sidecars | keep paper/submission and archive/release wording synchronized |
| `docs/milestones/README.md` | medium | `P59` control sync | update only after `P56/P57/P58` are all landed |
| `docs/plans/README.md` | medium | `P59` control sync | point to the new design, handoff, and startup prompt only after they exist |
| `tmp/active_wave_plan.md` | high | `P59` control sync | preserve `H64` as active and describe `P56/P57/P58/P59` as operational follow-through |
| `.gitignore` | low | `P54` artifact policy | do not weaken raw-row ignore rules |
| `scripts/export_release_preflight_checklist_audit.py` | high | standing audit | update together with its test and dependent docs |
| `scripts/export_p10_submission_archive_ready.py` | high | standing audit | update together with its test and dependent docs |
| `scripts/export_p56_*` through `scripts/export_p59_*` | medium | packet-local sidecars | keep packet-local invariants explicit and future-proof |
| `tests/test_export_p56_*` through `tests/test_export_p59_*` | medium | packet-local verification | keep them aligned with the exporter summaries |
| `results/P56_*` through `results/P59_*` | medium | exporter outputs | regenerate after the docs are stable |
| `results/release_*` and `results/P10_*` | high | standing audits | regenerate only after the full sidecar quartet lands |

Never resolve any of the high-risk rows from dirty root `main`. Use the clean
source branch, clean `main` scratch worktree, and current packet docs as the
only admissible operational references.
