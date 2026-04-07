# P35 Root Dirty Quarantine

Dirty root `main` is out of scope for the active scientific line.

Representative quarantined areas include:

- release/public-surface sync files under `results/P5_*` and
  `results/release_*`;
- older milestone/doc/result bundles from the earlier `H22-H27` and
  `R26-R33` same-endpoint line;
- helper doc surfaces under `docs/publication_record/`;
- temporary handoff files under `tmp/`.

Operational rule:

- do not reset, revert, or “clean up” dirty root `main` by momentum;
- continue scientific work only from clean worktrees;
- treat root `main` as a quarantine ledger until a later explicit hygiene or
  promotion packet handles it deliberately.
