# Current Stage Driver

## Active driver

The current active stage is:

- `H4_reproduction_mainline_return`
- `E1a_precision_patch`
- `E1b_systems_patch`
- `H5_repro_sync_and_refreeze`

This stage starts from the locked submission-candidate bundle and restrained
release-candidate checkpoint created by `P8` and `P9`, but it returns active
engineering work to the reproduction mainline rather than continuing
consolidation-first packaging. The `H3` / `P10` / `P11` / `F1` packet remains
the completed baseline for documentation, archive, and derivative controls.

## Execution order

The logical lane order remains `E1a_precision_patch` -> `E1b_systems_patch`.

1. Preserve the full current-round plan in `tmp/`.
2. Switch the canonical stage wording to a scientific-return packet.
3. Run `E1a_precision_patch` on the current bounded precision suite only.
4. Run `E1b_systems_patch` on the current mixed systems gate only.
5. Activate `E1c_compiled_boundary_patch` only if `E1a` or `E1b` exposes a
   real `D0` contradiction.
6. Refreeze through `H5` on the same narrow endpoint.

## Standing gates

- `results/P1_paper_readiness/summary.json`
- `results/P5_public_surface_sync/summary.json`
- `results/P5_callout_alignment/summary.json`
- `results/H2_bundle_lock_audit/summary.json`
- `results/P10_submission_archive_ready/summary.json`
- `results/H4_reproduction_return_guard/summary.json`
- `results/E1a_precision_patch/summary.json`
- `results/E1b_systems_patch/summary.json`
- `pytest -q`
- `git diff --check`

## Active bounded lanes

- `E1a_precision_patch` is active only for bounded `C3d` / `C3e` sharpening on
  the current validated suites.
- `E1b_systems_patch` is active only for same-scope systems attribution on the
  current positive `D0` suites.
- `M7` no-widening remains in force throughout both lanes.

## Conditional reopen path

`E1c` remains conditional only. `E1c_compiled_boundary_patch` may activate
only if the current `E1a` or `E1b` work exposes a concrete contradiction in
the frozen tiny typed-bytecode `D0` boundary.

## Historical-complete references

These remain the completed baseline while the current stage returns active
work to the reproduction mainline.

- `docs/milestones/H3_stage_driver_consolidation_and_plan_index/result_digest.md`
- `docs/milestones/P10_submission_packet_and_archival_repro_bundle/result_digest.md`
- `docs/milestones/P11_manuscript_targeting_and_derivative_controls/result_digest.md`
- `docs/milestones/F1_future_evidence_playbooks/result_digest.md`
- `docs/publication_record/paper_package_plan.md`
- `docs/milestones/P8_submission_candidate_and_bundle_lock/result_digest.md`
- `docs/milestones/P9_release_candidate_and_public_surface_freeze/result_digest.md`
- `docs/milestones/H2_release_hygiene_and_audit_promotion/result_digest.md`
