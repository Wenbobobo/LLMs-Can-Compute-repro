# Archival Repro Manifest

This file records what should be archived, how to regenerate the current
archive-first control packet, and how to interpret the current endpoint.

## Environment

- use the repo-local `uv` workflow for script and test execution;
- CUDA is optional for archive readers because the packet exporters are
  docs/control only; and
- the current wave is expected to run from a clean descendant worktree under
  `D:/zWenbo/AI/wt/`.

## Regeneration commands

```bash
uv run python scripts/export_p45_post_h60_clean_descendant_integration_readiness.py
uv run python scripts/export_f36_post_h60_conditional_compiled_online_reopen_qualification_bundle.py
uv run python scripts/export_h61_post_h60_archive_first_position_packet.py
uv run python scripts/export_p46_post_h60_archive_first_publication_sync.py
uv run pytest -q tests/test_export_p45_post_h60_clean_descendant_integration_readiness.py tests/test_export_f36_post_h60_conditional_compiled_online_reopen_qualification_bundle.py tests/test_export_h61_post_h60_archive_first_position_packet.py tests/test_export_p46_post_h60_archive_first_publication_sync.py
```

## Required archive payload

- `results/H61_post_h60_archive_first_position_packet/summary.json`
- `results/P45_post_h60_clean_descendant_integration_readiness/summary.json`
- `results/F36_post_h60_conditional_compiled_online_reopen_qualification_bundle/summary.json`
- `results/P46_post_h60_archive_first_publication_sync/summary.json`
- `results/F35_post_h59_far_future_model_and_weights_horizon_log/summary.json`
- `results/H60_post_f34_next_lane_decision_packet/summary.json`
- `results/F34_post_h59_compiled_online_retrieval_reopen_screen/summary.json`
- `results/H59_post_h58_reproduction_gap_decision_packet/summary.json`
- `results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json`
- `results/F32_post_h58_closeout_certification_bundle/summary.json`
- `results/R62_origin_native_useful_kernel_value_discriminator_gate/summary.json`
- `docs/publication_record/current_stage_driver.md`
- `docs/publication_record/release_summary_draft.md`
- `docs/publication_record/conditional_reopen_protocol.md`
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/claim_evidence_table.md`
- `docs/publication_record/review_boundary_summary.md`
- `docs/publication_record/submission_packet_index.md`

## Exporters

- `scripts/export_p45_post_h60_clean_descendant_integration_readiness.py`
- `scripts/export_f36_post_h60_conditional_compiled_online_reopen_qualification_bundle.py`
- `scripts/export_h61_post_h60_archive_first_position_packet.py`
- `scripts/export_p46_post_h60_archive_first_publication_sync.py`

## Archive interpretation rule

This archive is evidence for a narrow mechanistic endpoint: append-only traces,
exact latest-write retrieval, bounded precision, and a narrow useful-case
execution stack whose strongest current executor-value lane closes negative.

It is not evidence for arbitrary `C`, general LLM computation, or
current-scope end-to-end systems superiority.

The current active docs-only control packet is `H61`, above the preserved prior
active packet `H60`, the preserved reproduction-gap packet `H59`, the
preserved value-negative closeout `H58`, the preserved closeout certification
bundle `F32`, the current qualification-only bundle `F36`, the current
publication/docs wave `P46`, the current repo-hygiene sidecar `P45`, the
current far-future horizon log `F35`, the preserved prior reopen screen `F34`,
the preserved prior publication/claim-lock wave `P44`, the preserved prior
repo-hygiene sidecar `P43`, the preserved advisory dossier sidecar `P42`, the
preserved publication/archive sync sidecar `P41`, and the preserved paper-grade
endpoint `H43`.

Archive-first consolidation is now the default live posture. The only future
route still alive on paper is
`compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route`,
and it remains qualification-only rather than runtime-authorized.
