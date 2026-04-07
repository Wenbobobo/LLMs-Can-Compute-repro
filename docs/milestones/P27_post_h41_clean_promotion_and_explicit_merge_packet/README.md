# P27 Post-H41 Clean Promotion And Explicit Merge Packet

Completed operational merge packet after the landed `F20 -> H41` control
override.

`P27` exists to preserve the clean scientific source branch
`wip/h41-r43-mainline`, stage one explicit merge wave on
`wip/p27-promotion-merge`, and define when a later merge to `main` is mature
enough to review. It is an operational lane, not a scientific gate, and it
does not merge `main` inside this packet.

Execution details are fixed in:

- `merge_wave_manifest.md`
- `main_delta_summary.md`
- `artifact_tracking_policy.md`
- `worktree_runbook.md`
