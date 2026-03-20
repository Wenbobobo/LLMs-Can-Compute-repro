# Release Worktree Hygiene Snapshot Design

## Goal

Replace the remaining manual git-state release check with one machine-readable
operational snapshot, without turning the current dirty unattended tree into a
false red on the scientific or documentation control chain.

## Constraint

The current `H13/V1` stage explicitly allows a dirty working tree between
release-facing commits. The repo is not expected to stay clean during
unattended batching.

Because of that:

- a dirty tree should block a release-facing commit;
- a dirty tree should not automatically mark `release_preflight`, `P10`, or
  `H13` as evidence-chain failures.

## Selected approach

Create one independent export:

- `scripts/export_release_worktree_hygiene_snapshot.py`
- `results/release_worktree_hygiene_snapshot/summary.json`

The snapshot should read the live git worktree only and report:

- branch name;
- changed/staged/unstaged/untracked counts;
- grouped changed-path counts using the existing `H0`-style review buckets;
- `release_commit_state`, with two allowed values:
  - `clean_worktree_ready_if_other_gates_green`
  - `dirty_worktree_release_commit_blocked`
- `git_diff_check_state`, with:
  - `clean`
  - `warnings_only`
  - `content_issues_present`

The snapshot is an operational truth source, not a paper/result gate.

## Integration points

1. `release_preflight_checklist.md`
   - require checking the snapshot before any outward sync commit;
   - keep the actual clean-tree requirement attached to the commit event, not
     to the current unattended run.
2. `release_preflight_checklist_audit`
   - verify the checklist points to the snapshot;
   - verify the snapshot exists and reports one allowed state;
   - stop claiming that manual git-state inspection is the only control left.
3. `P10_submission_archive_ready`
   - require packet docs to name the snapshot and its regeneration command;
   - require the snapshot to exist and report an allowed state, but do not
     require the current tree to be clean;
   - surface the snapshot classification in the packet summary so later
     unattended governance rollups do not need to infer it indirectly.
4. `H13_post_h12_governance_stage_health`
   - include the snapshot as part of the unattended entrypoint;
   - surface the current `release_commit_state` directly in the summary.

## Low-risk principle

Do not make `release_preflight`, `P10`, or `H13` fail merely because the
current unattended tree is dirty. Fail only if the dirty-or-clean state is not
recorded explicitly.

## Acceptance

- one machine-readable snapshot exists for the live git tree;
- `release_preflight`, `P10`, and `H13` all reference that snapshot;
- diff-check warnings/content issues are classified explicitly;
- current dirty-tree state is represented as operationally blocked for release
  commits but does not collapse the broader governance chain;
- targeted tests remain green.
