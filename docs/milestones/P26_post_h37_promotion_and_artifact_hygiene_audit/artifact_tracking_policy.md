# Artifact Tracking Policy

## Current default

Treat large raw result files as operational artifacts unless they are clearly
claim-bearing and irreducible.

## User-mentioned file

Path under discussion:

- `results/R20_d0_runtime_mechanism_ablation_matrix/probe_read_rows.json`

Current status on the clean source branch:

- not present on `wip/f16-h38-p26-exec`

Current policy consequence:

- do not add a `.gitignore` rule as part of this wave;
- do not treat the missing file as part of the current promotion bundle;
- if the file reappears later on a clean source branch and is still larger than
  `10 MiB`, classify it before merge as one of:
  `claim_bearing_keep`,
  `reproducible_raw_move_or_ignore`, or
  `replace_with_compact_summary`.

## Rule

- if an artifact is non-claim-bearing and reproducible from tracked inputs,
  prefer moving it out of the tracked promotion bundle or ignoring it later;
- if an artifact is claim-bearing, replace the raw payload with a compact
  summary plus regeneration instructions before choosing ignore.
