# 2026-03-26 Post-H60 Archive-First Consolidation Design

## Purpose

Convert the post-`H60` planning-only state into an explicit archive-first
control wave on a clean successor worktree.

This wave does not reopen runtime science. It consolidates the honest endpoint,
records a clean-descendant integration posture, and sharpens the only still
admissible future route into a qualification-only dossier with hard stop
conditions.

## Starting State

The starting stack is:

`F31 -> H57 -> R62 -> H58 -> F32 -> H59 -> F34 -> H60`

with active sidecars and planning support:

- `P41_post_h58_publication_and_archive_sync`
- `P42_post_h59_gptpro_reinterview_packet`
- `P43_post_h59_repo_graph_hygiene_and_merge_map`
- `P44_post_h59_publication_surface_and_claim_lock`
- `F35_post_h59_far_future_model_and_weights_horizon_log`

The repo meaning at start:

- narrow mechanistic reproduction is real;
- broader headline reproduction did not land;
- the same executor-value lane is closed enough to treat same-lane reopen as
  inadmissible;
- only
  `compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route`
  remains alive on paper; and
- dirty root `main` stays quarantined.

## Selected Wave

This wave adds four packets:

1. `P45_post_h60_clean_descendant_integration_readiness`
   records clean-descendant integration posture and successor-line readiness.
2. `F36_post_h60_conditional_compiled_online_reopen_qualification_bundle`
   keeps the one admissible future family on paper only and converts it into a
   strict qualification gate rather than a loose idea.
3. `H61_post_h60_archive_first_position_packet`
   becomes the active docs-only packet and selects archive-first
   consolidation as the default live posture.
4. `P46_post_h60_archive_first_publication_sync`
   refreshes outward wording to archive-first plus executor-value partial
   falsification framing.

## Hard Constraints

- No runtime gate opens during this wave.
- No new same-lane executor-value probe is admissible.
- `F27`, `R53`, and `R54` remain blocked.
- Dirty root `main` remains excluded from scientific integration.
- No merge is executed during this wave.
- Large raw row dumps stay out of git by default.

## Design Rules

### P45 clean-descendant posture

- Record the current worktree and branch identity.
- Preserve `clean_descendant_only_never_dirty_root_main`.
- Keep the clean successor line explicit without claiming a merge occurred.
- Make later clean-descendant promotion possible without routing through the
  dirty root checkout.

### F36 qualification-only future route

- Preserve the one admissible route family from `F34`.
- Fix a useful-case target and comparator discipline before any runtime.
- Require a material cost-model change relative to the closed `R62/H58` lane.
- Make stop rules explicit enough that future reopen can be rejected quickly if
  the route collapses back into renamed same-lane work.

### H61 archive-first active packet

- Preserve `H60` as the prior active packet.
- Move the repo meaning from "planning-only / archive / stop is allowed" to
  "archive-first consolidation is the default live posture".
- Keep the downstream scientific lane non-runtime and preserve later explicit
  authorization as the only reopen path.

### P46 publication sync

- Replace stale reopen-era wording with archive-first wording.
- Make "narrow mechanistic reproduction plus executor-value partial
  falsification" the public shorthand.
- Remove `E1a/E1b/E1c` patch-lane language from live reopen protocol.

## Files To Add Or Refresh

New exporters and tests:

- `scripts/export_p45_post_h60_clean_descendant_integration_readiness.py`
- `scripts/export_f36_post_h60_conditional_compiled_online_reopen_qualification_bundle.py`
- `scripts/export_h61_post_h60_archive_first_position_packet.py`
- `scripts/export_p46_post_h60_archive_first_publication_sync.py`
- matching focused tests under `tests/`

New milestone directories:

- `docs/milestones/P45_post_h60_clean_descendant_integration_readiness/`
- `docs/milestones/F36_post_h60_conditional_compiled_online_reopen_qualification_bundle/`
- `docs/milestones/H61_post_h60_archive_first_position_packet/`
- `docs/milestones/P46_post_h60_archive_first_publication_sync/`

Control surfaces to refresh:

- `README.md`
- `STATUS.md`
- `tmp/active_wave_plan.md`
- `docs/publication_record/current_stage_driver.md`
- `docs/plans/README.md`
- `docs/milestones/README.md`
- `docs/publication_record/README.md`
- `docs/claims_matrix.md`
- `docs/publication_record/experiment_manifest.md`

Publication-facing docs to refresh:

- `docs/publication_record/release_summary_draft.md`
- `docs/publication_record/conditional_reopen_protocol.md`
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/claim_evidence_table.md`
- `docs/publication_record/review_boundary_summary.md`
- `docs/publication_record/paper_bundle_status.md`
- `docs/publication_record/archival_repro_manifest.md`
- `docs/publication_record/submission_packet_index.md`

## Verification

- run the four new exporters with `uv run python ...`
- run focused `uv run pytest` on the four new exporter tests
- run `git diff --check`

## Expected Outcome

After this wave the repo should say, cleanly and repeatedly:

- the strongest honest result is narrow mechanistic reproduction plus
  executor-value partial falsification;
- archive-first consolidation is the default active posture;
- one compiled-online route survives only on paper and only behind a later
  explicit authorization packet; and
- clean-descendant integration remains possible later without touching dirty
  root `main`.
