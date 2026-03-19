# Decision-Complete Handoff

## Preconditions

- `P8` has locked the submission-candidate bundle;
- `H2` audits are green;
- no `E1` patch lane is active.

## Recommended execution order

### Lane A: restrained outward sync

Write set:
- `README.md`
- `STATUS.md`
- `docs/publication_record/release_summary_draft.md`

Task:
- keep outward wording short, downstream, and explicit about blocked claims.

### Lane B: blocked-blog derivative control

Write set:
- `docs/publication_record/blog_outline.md`
- `docs/publication_record/blog_release_rules.md`

Task:
- preserve the blocked-blog state and make any future derivative path traceable
  to the locked manuscript bundle.

### Lane C: release-candidate gate refresh

Write set:
- refreshed `results/P5_public_surface_sync/`
- refreshed `results/H2_bundle_lock_audit/`
- `docs/publication_record/release_candidate_checklist.md`

Task:
- rerun the narrow outward audits and keep the release-candidate checklist in
  sync with them.

## Integration gate

Only integrate a `P9` batch after:

1. `P8` is satisfied on the current repo state;
2. `P5` public-surface and `H2` bundle-lock audits are green;
3. `pytest -q` passes;
4. `git diff --check` passes.
