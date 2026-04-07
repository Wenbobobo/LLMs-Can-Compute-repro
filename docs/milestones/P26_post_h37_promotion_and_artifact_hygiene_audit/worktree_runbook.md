# Worktree Runbook

1. Start from `wip/f16-h38-p26-exec`, not dirty `main`.
2. Confirm the branch is clean with `git status --short --branch`.
3. Inspect `git diff --stat main..wip/f16-h38-p26-exec`.
4. Review the recommended packet split in `commit_split_manifest.md`.
5. Reconcile or isolate dirty `main` work before any promotion attempt.
6. Do not let `P26` justify `R41` activation or broader scope lift.
