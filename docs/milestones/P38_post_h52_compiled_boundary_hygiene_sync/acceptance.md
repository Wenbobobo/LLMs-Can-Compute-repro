# Acceptance

- `P38` remains operational/docs-only.
- `H54` remains the current active docs-only packet.
- `H53` remains the preserved prior compiled-boundary reentry packet.
- Raw row dumps and artifacts above roughly `10 MiB` stay out of git by
  default.
- Compact summaries, manifests, stop rules, and first-fail digests stay in
  git.
- `uv` remains the default execution path for exporters and focused tests.
- Merge back to `main` does not occur during this wave.
