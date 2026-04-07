# Artifact Policy

- Keep compact summaries, checklists, manifests, stop rules, timing digests,
  and first-fail localizations in git.
- Treat raw row dumps, per-read dumps, trace rows, and any artifact above
  roughly `10 MiB` as out-of-git by default.
- If a large non-summary JSON such as a detailed surface report grows past the
  threshold, slim it into a compact digest rather than force it into git.
- Git LFS remains inactive by default.
- `uv` remains the default path for exporter and test execution.
