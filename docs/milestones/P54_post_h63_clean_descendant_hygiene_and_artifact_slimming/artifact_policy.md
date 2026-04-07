# Artifact Policy

- `probe_read_rows.json`, `per_read_rows.json`, `trace_rows.json`, and
  `step_rows.json` remain local-only by default
- `surface_report.json` may be archived only when compact and review-useful;
  large variants above roughly `10 MiB` stay local or go to LFS-only handling
- the clean descendant line should keep zero normally tracked artifacts at or
  above roughly `10 MiB`
- summary tables and manifest rows are preferred over raw row dumps
