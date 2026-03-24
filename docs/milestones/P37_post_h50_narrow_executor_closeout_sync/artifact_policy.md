# P37 Artifact Policy

- compact summaries, checklists, manifests, stop rules, first-fail digests,
  and branch/run ledgers stay in git;
- raw step rows, trace rows, `probe_read_rows.json`, `per_read_rows.json`,
  and similarly large row dumps stay out of git by default;
- `.gitignore` carries the concrete raw-row ignore patterns for the clean
  worktree rather than leaving that policy implicit;
- any artifact above roughly `10 MiB` should be treated as out-of-git unless
  it is review-critical and no compact substitute is sufficient;
- clean worktrees should track no artifacts at or above roughly `10 MiB`
  unless a later explicit packet makes one review-critical exception;
- Git LFS remains inactive by default for the closed wave; and
- if LFS becomes necessary later, the trigger must be stated explicitly in a
  later packet rather than inferred from convenience.
