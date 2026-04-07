# Post-H41 P27 Explicit Merge Wave Design

`P27_post_h41_clean_promotion_and_explicit_merge_packet` is the operational
follow-through wave required after the landed `F20 -> H41` control override.
It does not add scientific evidence. Its purpose is to freeze one explicit
promotion posture around the current clean post-`H41` source branch,
`wip/h41-r43-mainline`, while keeping dirty `main` out of the control surface.

The branch model is fixed. `wip/h41-r43-mainline` remains the clean scientific
source branch carrying the landed `F20/H41` state. `wip/p27-promotion-merge`
is the dedicated operational packet branch where merge posture is recorded and
reviewed. `main` remains the eventual target branch only. `P27` therefore
stages an explicit merge wave instead of drifting into `main` by momentum.
`P27` must keep dirty `main` out of the control surface.

The packet must record four things. First, it must preserve the clean source
branch and the explicit merge branch as separate roles. Second, it must make
merge criteria explicit: confirm that the clean source branch is synced to
`origin`, review one coherent packet range, and keep oversized or dirty-tree-
only artifacts outside the promotion set. Third, it must keep execution
ordering explicit by leaving `R43_origin_bounded_memory_small_vm_execution_gate`
as the next exact lane and `R45_origin_dual_mode_model_mainline_gate` as the
coequal model lane. Fourth, it must keep `main` untouched inside this wave:
`P27` does not merge `main`, does not execute `R43`, and does not execute
`R45`.

Deliverables are the completed `P27` milestone packet, one exporter plus one
focused test, regenerated result summaries, and refreshed control surfaces
(`current_stage_driver`, `active_wave_plan`, `README`, `STATUS`, and index
docs). Acceptance requires `promotion_mode = explicit_merge_wave`,
`merge_executed = false`, explicit large-artifact handling, and an updated
forward ladder of `R43 -> R45 -> H42 -> conditional R44`.
