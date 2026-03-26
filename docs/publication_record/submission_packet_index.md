# Submission Packet Index

This file lists the current packet set that should be handed to future review,
archive, or submission preparation work.

## Core packets

- `../milestones/H61_post_h60_archive_first_position_packet/`
- `../milestones/P45_post_h60_clean_descendant_integration_readiness/`
- `../milestones/F36_post_h60_conditional_compiled_online_reopen_qualification_bundle/`
- `../milestones/P46_post_h60_archive_first_publication_sync/`
- `../milestones/F35_post_h59_far_future_model_and_weights_horizon_log/`
- `../milestones/H60_post_f34_next_lane_decision_packet/`
- `../milestones/F34_post_h59_compiled_online_retrieval_reopen_screen/`
- `../milestones/H59_post_h58_reproduction_gap_decision_packet/`
- `../milestones/H58_post_r62_origin_value_boundary_closeout_packet/`
- `../milestones/F32_post_h58_closeout_certification_bundle/`
- `../milestones/H43_post_r44_useful_case_refreeze/`

## Result summaries

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

## Publication-facing docs

- `release_summary_draft.md`
- `conditional_reopen_protocol.md`
- `claim_ladder.md`
- `claim_evidence_table.md`
- `review_boundary_summary.md`
- `paper_bundle_status.md`
- `archival_repro_manifest.md`

## Exporters

- `scripts/export_p45_post_h60_clean_descendant_integration_readiness.py`
- `scripts/export_f36_post_h60_conditional_compiled_online_reopen_qualification_bundle.py`
- `scripts/export_h61_post_h60_archive_first_position_packet.py`
- `scripts/export_p46_post_h60_archive_first_publication_sync.py`

## Current control interpretation

Venue-specific formatting may fork from this packet, but that formatting must
not widen claims or outrun the locked archive-first stack.

The current repo control state is `H61` as the active docs-only decision
packet, with `H60` preserved as the prior active packet, `H59` preserved as the
prior reproduction-gap packet, `H58` preserved as the prior closeout, `F32`
preserved as the prior closeout certification bundle, `F36` as the current
qualification-only future bundle, `P46` as the current publication/docs sync
wave, `P45` as the current repo-hygiene sidecar, `F35` as the current
far-future horizon log, `F34` as the preserved prior reopen screen, `P44/P43`
as the preserved prior wording-lock and repo-hygiene layer, `P42` preserved as
the prior advisory dossier sidecar, `P41` preserved as the prior publication
archive sync sidecar, and `H43` preserved as the paper-grade useful-case
refreeze packet.

No active downstream runtime lane exists after `H61`. Same-lane executor-value
reopen remains closed. The only future family still alive on paper is
`compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route`,
and it remains qualification-only until a later explicit authorization packet.
