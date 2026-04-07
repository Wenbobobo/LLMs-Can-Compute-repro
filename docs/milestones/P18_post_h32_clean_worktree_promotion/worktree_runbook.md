# Worktree Runbook

## Purpose

This runbook exists so `P18` can be executed without re-deciding clean-worktree
mechanics during the post-`H32` closeout batch.

The immediate goal is to keep the `H31/R38/H32` packet reviewable inside one
clean successor worktree and avoid promoting from dirty `main` or dirty
`wip/h27-promotion`.

## Recommended Worktree

- path:
  `D:/zWenbo/AI/LLMCompute-worktrees/h31-later-explicit`
- branch:
  `wip/h31-later-explicit`
- starting point:
  `wip/p17-h30-clean` at commit `a74d218`

Current status:

- this worktree has already been created;
- it is the intended implementation and promotion lane for `H31/R38/H32/P18`;
- no second clean-copy lane is required for the current batch.

## Open Procedure

1. Save the current `H31/R38/H32` plan and control docs on this clean branch.
2. Inspect `git status --short`.
3. Run the packet-specific checks below.
4. Run `git diff --check`.
5. Inspect `git status --short` again before any staging or commit.

## Packet 1 Checks

Use these after editing the scientific/runtime packet:

```powershell
uv run pytest -q `
  tests/test_bytecode_harness.py `
  tests/test_export_r37_origin_compiler_boundary_gate.py `
  tests/test_export_h30_post_r36_r37_scope_decision_packet.py `
  tests/test_export_h31_post_h30_later_explicit_boundary_decision_packet.py `
  tests/test_export_r38_origin_compiler_control_surface_extension_gate.py `
  tests/test_export_h32_post_r38_compiled_boundary_refreeze.py
```

## Packet 2 Checks

Use these after editing the current-facing doc sweep:

```powershell
rg -n "H30 is now the current active packet|current active H30 routing/refreeze packet|later explicit packet required before any compiled-boundary extension" `
  README.md STATUS.md docs/publication_record/README.md `
  docs/publication_record/current_stage_driver.md tmp/active_wave_plan.md
git diff --check
```

The `rg` command should return no matches for the stale pre-`H32` phrases.

## Guardrails

- Do not commit from dirty `main`.
- Do not reopen dirty `wip/h27-promotion` for this packet.
- Do not widen the opcode surface or reuse this branch as a broader compiler
  sandbox.
- Do not treat `R38` as arbitrary-language evidence.
