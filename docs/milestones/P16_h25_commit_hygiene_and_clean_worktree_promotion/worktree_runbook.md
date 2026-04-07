# Worktree Runbook

## Purpose

This runbook exists so `P16` can be executed without re-deciding the clean
worktree mechanics during the actual closeout batch.

The immediate goal is not to create a release commit from the integrated dirty
tree. The immediate goal is to open one isolated worktree, copy only the
reviewable closeout subset into it, regenerate the state-dependent outputs
there, and keep the path set small enough for review.

## Recommended Worktree

- path:
  `D:/zWenbo/AI/LLMCompute-worktrees/h25-clean`
- branch:
  `wip/p16-h25-clean`
- starting point:
  `main` at the current local `HEAD`

Current status:

- this worktree has already been created;
- it is still a clean scaffold and does not yet contain the intended closeout
  subset from the integrated tree.

## Open Procedure

1. Save the current plan/handoff docs on `main`.
2. Create the isolated worktree:
   `git worktree add -b wip/p16-h25-clean D:/zWenbo/AI/LLMCompute-worktrees/h25-clean main`
3. Confirm the new worktree is clean before copying any closeout files.
4. Copy only one of the approved closeout subsets from the integrated tree into
   the clean worktree.
5. Re-run the state-dependent exporters in the clean worktree.
6. Run the focused test subset in the clean worktree.
7. Inspect `git status --short` in the clean worktree before any staging.

## State-Dependent Commands

Run these only inside the clean worktree after the intended subset has been
copied:

```powershell
uv run python scripts/export_release_worktree_hygiene_snapshot.py
uv run python scripts/export_release_preflight_checklist_audit.py
```

Focused validation for the closeout subset:

```powershell
uv run pytest `
  tests/test_export_r30_d0_boundary_reauthorization_packet.py `
  tests/test_export_r31_d0_same_endpoint_systems_recovery_reauthorization_packet.py `
  tests/test_export_h25_refreeze_after_r30_r31_decision_packet.py `
  tests/test_export_p5_public_surface_sync.py `
  tests/test_export_release_preflight_checklist_audit.py
```

## Guardrails

- Do not commit from the integrated dirty tree.
- Do not copy unrelated runtime/result churn into the clean worktree.
- Do not start `R32` from this worktree until the `P16` closeout subset is
  either committed or explicitly abandoned.
- Do not regenerate state-dependent outputs before the intended subset is
  copied; otherwise the clean worktree can reflect the wrong path set.
