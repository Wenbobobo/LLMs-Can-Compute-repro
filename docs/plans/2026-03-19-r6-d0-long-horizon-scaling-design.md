# R6 D0 Long-Horizon Scaling Design

## Goal

Test whether the already-admitted `D0` endpoint remains exact under fixed
long-horizon scaling without changing semantics or widening the frontend.

## Intended outputs

- one fixed `{2,4,8}` multiplier grid over current scalable `D0` families;
- exactness rows against bytecode / lowered / spec agreement;
- linear-vs-Hull decode parity rows on the same lowered programs;
- growth rows comparing step/event/read/write counts to preserved baseline
  seeds;
- one narrow precision companion on exact-admitted largest-horizon rows only.

## Scope lock

- current `D0` endpoint only;
- current admitted families only;
- no open-ended search over new seeds or new semantics;
- precision follow-up remains companion-only and does not become a broad
  robustness claim.

## Acceptance

- either the scaled rows stay exact or failures are typed as true
  contradictions;
- linear and accelerated Hull decode parity remains explicit on every tested
  row;
- growth is recorded quantitatively rather than described loosely.
