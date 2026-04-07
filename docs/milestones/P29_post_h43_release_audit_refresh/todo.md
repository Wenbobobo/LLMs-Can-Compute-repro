# P29 Todo

- refresh `release_preflight_checklist_audit` so it reports current `H43`
  release-control state rather than historical `H25/H23`;
- refresh `P5_public_surface_sync` so it reports the current `H43/P28`
  publication surface rather than historical `H25/H23/H27`;
- refresh `H2_bundle_lock_audit` and `P10_submission_archive_ready` so they
  stop treating `H19` as the current paper phase;
- refresh the canonical `release_worktree_hygiene_snapshot` on the clean `P29`
  worktree and remove orphan legacy hygiene outputs;
- refresh the release/public ledgers that still describe `H40` or `H32/H34`
  as current; and
- record the wave in the active handoff and index surfaces.
