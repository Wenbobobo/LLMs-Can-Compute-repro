# Plans Index

This directory stores planning-only design documents, unattended master plans,
and packet-specific handoff notes. These files are routing aids, not
claim-bearing evidence. When a plan and a landed result differ, trust the
current stage driver, the milestone/result artifacts, and the machine-readable
`results/` summaries first.

## Current Start Points

- `2026-03-22-post-h30-explicit-next-wave-design.md` — the current saved
  post-`H30` planning surface: docs-only closeout first, then only a later
  explicit packet before any further compiler-boundary extension.
- `2026-03-22-post-r36-explicit-next-wave-design.md` — the saved post-`R36`
  explicit-next-wave handoff that led to the landed `R37 -> H30` packet; keep
  it as the pre-execution rationale rather than the current machine state.
- `2026-03-22-post-unattended-r32-mainline-design.md` — preserved historical
  same-endpoint handoff for the earlier `P16 -> R32 -> H26 -> R33/H27` route.
- `2026-03-21-h18-unattended-mainline-master-plan.md` — broad unattended
  master plan for the mainline reproduction program.
- `2026-03-22-post-h23-reauthorization-design.md` — the design that landed the
  preserved prior `H24/R30/R31/H25` reauthorization/refreeze packet.
- `2026-03-22-post-h25-r32-r33-near-term-design.md` — preserved historical
  near-term handoff for `R32` first and deferred `R33` second on the old
  same-endpoint route.

## Use With

- `../publication_record/current_stage_driver.md` — canonical current stage,
  routing order, and standing gates.
- `../../tmp/active_wave_plan.md` — short current-wave handoff and closeout
  notes.
- `2026-03-22-post-h30-explicit-next-wave-design.md` — current design surface
  for the later explicit packet required after `H30`.
- `../milestones/P17_h30_commit_hygiene_and_clean_worktree_promotion/` —
  completed docs-only closeout lane for clean-worktree packet packaging after
  `H30`.
- `../milestones/H30_post_r36_r37_scope_decision_packet/` — current active
  routing/refreeze packet for the Origin-core line.
- `../milestones/R37_origin_compiler_boundary_gate/` — landed tiny
  compiled-boundary gate on the active substrate.
- `../milestones/P16_h25_commit_hygiene_and_clean_worktree_promotion/` —
  immediate operational closeout lane before any new runtime batch.
- `../milestones/R32_d0_family_local_boundary_sharp_zoom/execution_manifest.md`
  — first-pass `R32` execution manifest.
- `../milestones/R33_d0_non_retrieval_overhead_localization_audit/component_localization_manifest.md`
  — first-pass `R33` audit manifest.

## Historical Plan Groups

- `2026-03-21-*` and `2026-03-22-*` — current post-`H30` / post-`R36` design
  pair plus the preserved post-`H19`, post-`H21`, post-`H23`, and post-`H25`
  design stack.
- `2026-03-20-*` — `H10` through `H17`, `R8` through `R18`, and release/control
  audit design set.
- `2026-03-19-*` — `H1` through `H9`, `R3` through `R7`, `P5` through `P10`,
  and early unattended governance/master-plan set.
- `2026-03-17-*` and `2026-03-18-*` — earliest bootstrap, exact hard-max,
  trainable latest-write, and first compiled-boundary planning set.

## Reading Rule

For current work, start with the newest plan in the relevant lane, then confirm
its status against:

1. `../publication_record/current_stage_driver.md`
2. `../../tmp/active_wave_plan.md`
3. the corresponding milestone `README.md` / `status.md`
4. the corresponding `results/<lane>/summary.json`

Do not treat an older plan as authorization to reopen a blocked lane.
When a saved plan and the current `H30/R37` packet differ, trust the landed
packet.
