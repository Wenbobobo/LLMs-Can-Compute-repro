# Promotion Manifest

## Purpose

Prepare one reviewable promotion inventory from the true landed `H27 -> H36`
stack without touching dirty `main` directly.

## Fixed Branches

- scientific source of truth:
  `wip/h35-r40-p24-exec`
- clean promotion-prep branch:
  `wip/p25-f15-h37-exec`
- protected target branch:
  `main`

## Promotion Mode

- `prepare_only`
- no direct merge inside `P25`
- no commit from dirty `main`

## Included Packet Window

- same-endpoint closeout and Origin-core pivot:
  `P16`, `R32`, `H26`, `R33`, `H27`, `H28`, `R34`, `R35`, `H29`
- explicit compiled-boundary packet chain:
  `R36`, `R37`, `H30`, `P17`, `H31`, `R38`, `H32`, `P18`, `H33`, `R39`,
  `H34`, `P20`
- current family-first and bounded-scalar stack:
  `F10`, `F12`, `F13`, `F14`, `P23`, `H35`, `R40`, `H36`, `P24`
- deferred future design surface:
  `R41_origin_runtime_relevance_threat_stress_audit`

## Excluded Actions

- direct merge into `main`
- new runtime execution
- README/blog widening
- unrelated dirty-tree cleanup from `main`
