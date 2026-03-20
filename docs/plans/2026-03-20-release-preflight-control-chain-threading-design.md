# Release-Preflight Control-Chain Threading Design

## Goal

Thread the new `release_preflight_checklist_audit` more explicitly into the
current post-`H12` control chain without creating an exporter dependency cycle.

## Constraint

`release_preflight_checklist_audit` already depends on:

- `results/P5_public_surface_sync/summary.json`
- `results/P5_callout_alignment/summary.json`
- `results/H2_bundle_lock_audit/summary.json`
- `results/V1_full_suite_validation_runtime_timing_followup/summary.json`

Because of that, `P5` and `H2` must not start consuming the
`release_preflight_checklist_audit` summary directly. Doing so would make the
control chain cyclic and would break deterministic regeneration order.

## Selected approach

Use a split strategy.

1. Tighten `P5` and `H2` only at the document-anchor level.
   - `P5` should keep `docs/publication_record/README.md` explicit about the
     human `release_preflight_checklist.md` and its machine-readable audit.
   - `H2` should require `release_candidate_checklist.md` to list the new audit
     alongside the older standing guards.
2. Thread the new audit summary into `H11`.
   - `H11` does not sit on the dependency path of the release-preflight audit,
     so it can consume `results/release_preflight_checklist_audit/summary.json`
     directly.
   - This makes the active post-`H12` stage guard explicitly depend on the
     outward-sync control reference now used by `H13`.

## Intended outputs

- refreshed `docs/publication_record/release_candidate_checklist.md`
- refreshed `scripts/export_p5_public_surface_sync.py`
- refreshed `scripts/export_h2_bundle_lock_audit.py`
- refreshed `scripts/export_h11_post_h9_mainline_rollover_guard.py`
- refreshed targeted tests and regenerated result summaries

## Acceptance

- no new exporter cycle is introduced;
- `release_candidate_checklist.md` lists
  `results/release_preflight_checklist_audit/summary.json`;
- `P5` and `H2` stay green on current docs while checking the new anchor;
- `H11` stays green while requiring a green
  `release_preflight_checklist_audit` summary;
- regeneration order remains straightforward:
  `P5/H2/V1 timing -> release_preflight -> H11/P10`.
