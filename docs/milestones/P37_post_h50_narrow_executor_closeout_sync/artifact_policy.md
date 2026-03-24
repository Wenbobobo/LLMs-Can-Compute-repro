# P37 Artifact Policy

- compact summaries, checklists, manifests, stop rules, first-fail digests,
  and branch/run ledgers stay in git;
- raw step rows, trace rows, `probe_read_rows.json`, `per_read_rows.json`,
  and similarly large row dumps stay out of git by default;
- any artifact above roughly `10 MiB` should be treated as out-of-git unless
  it is review-critical and no compact substitute is sufficient;
- Git LFS remains inactive by default for the closed wave; and
- if LFS becomes necessary later, the trigger must be stated explicitly in a
  later packet rather than inferred from convenience.
