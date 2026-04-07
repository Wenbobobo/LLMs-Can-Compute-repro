# Artifact Policy

- `probe_read_rows.json`, `per_read_rows.json`, `trace_rows.json`, and
  `step_rows.json` stay out of git by default
- large variants above roughly `10 MiB` remain local-only or move to
  explicit-LFS-only handling in a later review-critical packet
- `surface_report.json` follows the same rule when it grows beyond review-sized
  scope
- Git LFS remains inactive by default for this wave
- no artifact-policy rule in this wave authorizes runtime reopening, claim
  widening, or dirty-root integration
