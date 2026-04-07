# P35 Artifact Inventory

## Tracked Current Packet Artifacts

- milestone-local docs, summaries, checklists, claim packets, and snapshots;
- narrow runtime summaries for `R46`, `R47`, `R48`, and `H47`;
- current handoff surfaces:
  `README.md`,
  `STATUS.md`,
  `docs/publication_record/current_stage_driver.md`,
  `docs/publication_record/experiment_manifest.md`, and
  `tmp/active_wave_plan.md`.

## Large-Artifact Rule

- raw artifacts above `10 MiB` do not enter git by default;
- tracked summaries stay preferred over row-complete dumps;
- if a raw artifact is required later, first prefer:
  compression,
  sampling,
  external storage reference, or
  a later explicit hygiene packet;
- current tracked useful-case artifacts remain below that threshold, so no new
  LFS rule is authorized here.

## Immediate Practical Consequence

`results/R20_d0_runtime_mechanism_ablation_matrix/probe_read_rows.json`
remains ignored and is the standing example for the default out-of-git policy.
