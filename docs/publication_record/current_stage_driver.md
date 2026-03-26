# Current Stage Driver

## Active Driver

The current active stage is:

- `H64_post_p53_p54_p55_f38_archive_first_freeze_packet`

The preserved prior active packet is:

- `H63_post_p50_p51_p52_f38_archive_first_closeout_packet`

The current paper/archive claim-sync wave is:

- `P53_post_h63_paper_archive_claim_sync`

The current repo hygiene sidecar is:

- `P54_post_h63_clean_descendant_hygiene_and_artifact_slimming`

The current promotion-prep wave is:

- `P55_post_h63_clean_descendant_promotion_prep`

The current dormant future dossier is:

- `F38_post_h62_r63_dormant_eligibility_profile_dossier`

The default downstream lane is:

- `archive_or_hygiene_stop`

## Current Machine-State Meaning

- `P53` locks paper/review/archive/submission wording to the `H64`
  archive-first freeze state.
- `P54` keeps clean-descendant-only hygiene, artifact-slimming, and merge-prep
  explicit while dirty root `main` remains quarantined.
- `P55` keeps clean-descendant promotion-prep and the next handoff explicit
  while merge execution remains absent.
- merge posture remains `clean_descendant_only_never_dirty_root_main`.
- `F38` records the only surviving future family as a dormant no-go dossier and
  leaves the key cost-profile fields unresolved.
- `H64` is now the current active docs-only packet and selects
  `archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant`.
- archive-first freeze is now the active route.
