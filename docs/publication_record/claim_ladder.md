# Claim Ladder

| Stage | Status | Artifacts | Scope |
| --- | --- | --- | --- |
| P63 Published successor promotion prep | validated as the current published successor promotion-prep wave | `results/P63_post_p62_published_successor_promotion_prep/summary.json`, `results/P63_post_p62_published_successor_promotion_prep/claim_packet.json` | promotes `wip/p63-post-p62-tight-core-hygiene` as the live published successor while preserving the prior `P60/P61/P62` stack |
| P64 Release hygiene rebaseline | validated as the current release hygiene rebaseline wave | `results/P64_post_p63_release_hygiene_rebaseline/summary.json`, `results/P64_post_p63_release_hygiene_rebaseline/claim_packet.json` | reanchors release hygiene, preflight, and archive-ready posture on the published successor branch |
| P65 Merge-prep control sync | validated as the current merge-prep control sync wave | `results/P65_post_p64_merge_prep_control_sync/summary.json`, `results/P65_post_p64_merge_prep_control_sync/claim_packet.json` | synchronizes current driver, indexes, active-wave state, and next-entrypoint docs to the successor stack while keeping runtime closed |
