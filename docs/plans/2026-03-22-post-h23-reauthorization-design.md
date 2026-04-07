# 2026-03-22 Post-H23 Reauthorization Design

## Summary

`H23` remains the current frozen scientific state on the fixed tiny
typed-bytecode `D0` endpoint. The bounded post-`H21` reopen packet strengthened
the same narrow execution-substrate story, but it still left two critical
questions unresolved:

1. the true executor boundary is still not localized inside the bounded `D0`
   envelope; and
2. the same-endpoint systems story is still mixed even after the bounded
   mechanism-contract audit.

The next phase should therefore avoid two bad moves:

- do not widen scope by momentum toward arbitrary compiled-language or
  frontier/demo claims;
- do not keep running new science lanes without first deciding which
  post-`H23` question is still worth executing.

The correct next packet is a bounded reauthorization wave:

- operational split:
  `H24_post_h23_reauthorization_and_hygiene_split`;
- boundary decision packet:
  `R30_d0_boundary_reauthorization_packet`;
- systems decision packet:
  `R31_d0_same_endpoint_systems_recovery_reauthorization_packet`;
- refreeze:
  `H25_refreeze_after_r30_r31_decision_packet`;
- background planning/doc lanes:
  `F4_post_h23_origin_claim_delta_matrix`,
  `P15_internal_claim_and_handoff_sync_after_h25`.

## Execution Protocol

- Save this design before creating the new packet.
- Refresh `tmp/active_wave_plan.md` to show that `H22 -> R26 + R28 ->
  conditional R27 -> H23 -> P14` is complete and that the next wave is a
  post-`H23` reauthorization packet.
- Keep write sets isolated:
  - `main`: integration, root/publication driver sync, focused validation.
  - `wt-r30`: boundary reauthorization packet only.
  - `wt-r31`: systems reauthorization packet only.
  - `wt-f4p15`: origin-claim delta matrix and internal handoff/docs only.
- Do not activate `R29` or `F3` inside this wave.
- Do not treat hygiene cleanup or internal-doc maintenance as scientific
  progress.
- Keep commits path-scoped:
  - `H24` scaffold / split guard;
  - `R30` packet;
  - `R31` packet;
  - `H25` refreeze and driver sync;
  - optional `F4/P15` internal-doc packet.

## Wave Order

### Wave A: `H24_post_h23_reauthorization_and_hygiene_split`

- Save this design and refresh the active-wave handoff.
- Create the bounded post-`H23` decision packet skeleton.
- Keep `H23` explicit as the frozen scientific state and `P14` explicit as the
  completed downstream outward-sync lane.
- Preserve `R29` and `F3` as blocked future lanes.

### Wave B: `R30_d0_boundary_reauthorization_packet`

- Start from the landed `R21`, `R22`, `R24`, `R26`, `R27`, `H21`, and `H23`
  evidence chain.
- Decide whether the project should authorize one more bounded
  family-local sharp zoom, or instead stop the boundary line on principled
  no-localization grounds.
- Reuse the `R24` candidate core and zoom-discipline rather than inventing a
  new wide grid.

### Wave C: `R31_d0_same_endpoint_systems_recovery_reauthorization_packet`

- Start from the landed `R2`, `E1b`, `R17`, `R18`, `R20`, `R23`, `R25`,
  `R28`, and `H23` evidence chain.
- Separate mechanism success from systems competitiveness.
- Decide whether any later same-endpoint recovery story is still honest, or
  whether the honest next step is a narrower non-retrieval overhead audit.

### Wave D: `H25_refreeze_after_r30_r31_decision_packet`

- Freeze `R30` and `R31` into one machine-readable control packet.
- Preserve `H23` as the frozen scientific evidence state.
- Authorize at most one next science lane as primary, and one deferred audit as
  secondary.

### Background Lane: `F4_post_h23_origin_claim_delta_matrix`

- Tag major origin-facing claims as:
  `reproduced_here`, `narrowed_here`, `unsupported_here`,
  `blocked_by_scope`, or `requires_new_substrate`.

### Background Lane: `P15_internal_claim_and_handoff_sync_after_h25`

- Sync internal-only claims, blocked blog skeleton, and handoff notes to the
  landed `H25` packet.

## Defaults

- Stay on the fixed `D0` endpoint.
- Preserve `H23` as the current frozen scientific state.
- Preserve `R29` and `F3` as blocked future lanes.
- Treat broader compiled demos, arbitrary `C`, frontier wording, and blog-first
  presentation as blocked.
