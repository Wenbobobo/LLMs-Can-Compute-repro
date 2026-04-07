# P36 Artifact Policy

- compact summaries, checklists, manifests, stop rules, and first-fail digests
  stay in git;
- raw per-read dumps, full probe rows, and large exploratory scratch outputs
  stay out of git by default;
- any artifact above roughly `10 MiB` should be treated as out-of-git unless
  it is review-critical and compact alternatives are insufficient;
- Git LFS remains inactive by default for this wave; and
- if LFS becomes necessary later, the trigger must be stated explicitly in a
  later packet rather than inferred from convenience.
