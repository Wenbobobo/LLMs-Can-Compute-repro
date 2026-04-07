# Worktree Runbook

## Purpose

This runbook exists so `P17` can be executed without re-deciding clean-worktree
mechanics during the actual closeout batch.

The immediate goal is not to commit from the integrated dirty tree. The
immediate goal is to use one already-created clean worktree, copy only one
approved closeout subset into it, verify the copied subset there, and keep the
path set small enough for review.

## Recommended Worktree

- path:
  `D:/zWenbo/AI/LLMCompute-worktrees/h30-clean`
- branch:
  `wip/p17-h30-clean`
- starting point:
  `wip/h27-promotion` at commit `eaa4fb0`

Current status:

- this worktree has already been created;
- the copied `P17` review subset has already been committed here;
- the focused `P17` checks already passed once in this worktree.

## Open Procedure

1. Save the current `H30` plan/handoff docs on the integrated tree.
2. Inspect the committed subset in the clean worktree:
   `git -C D:/zWenbo/AI/LLMCompute-worktrees/h30-clean status --short`
3. If a fresh retry is needed, recreate the scaffold instead of mixing in
   unrelated changes.
4. Copy only one approved packet from `commit_split_manifest.md` into the clean
   worktree.
5. Run the packet-specific checks below.
6. Run `git diff --check` in the clean worktree.
7. Inspect `git status --short` in the clean worktree before any staging.

## Packet 1 Checks

Use these after copying `origin-core-h28-to-h30-packet`:

```powershell
uv run pytest -q `
  tests/test_model_exact_hardmax.py `
  tests/test_model_free_running_executor.py `
  tests/test_trace_interpreter.py `
  tests/test_export_h28_post_h27_origin_core_reanchor_packet.py `
  tests/test_export_r34_origin_retrieval_primitive_contract_gate.py `
  tests/test_export_r35_origin_append_only_stack_vm_execution_gate.py `
  tests/test_export_h29_refreeze_after_r34_r35_origin_core_gate.py `
  tests/test_export_r36_origin_long_horizon_precision_scaling_gate.py `
  tests/test_export_r37_origin_compiler_boundary_gate.py `
  tests/test_export_h30_post_r36_r37_scope_decision_packet.py
```

## Packet 2 Checks

Use these after copying `h30-entrypoint-closeout`:

```powershell
rg -n "current active post-|current active operational decision packet|current frozen same-endpoint state" `
  README.md STATUS.md docs/publication_record/README.md `
  docs/publication_record/current_stage_driver.md tmp/active_wave_plan.md
git diff --check
```

The `rg` command should return no matches for those stale phrases.

## Guardrails

- Do not commit from the integrated dirty tree.
- Do not copy unrelated runtime/result churn into `h30-clean`.
- Do not start a later explicit packet from `h30-clean` until the `P17`
  closeout commits are either promoted elsewhere or explicitly abandoned.
- Do not relabel docs-only closeout as scientific progress.
