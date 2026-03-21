# H16 Post-H15 Same-Scope Reopen Design

## Goal

Reopen the repo after `H15` without changing the scientific target. `H16`
should switch the active driver from refreeze bookkeeping back to same-scope
mechanism work on the fixed `D0` endpoint.

## Inputs

- `results/H15_refreeze_and_decision_sync/summary.json`
- preserved `H14/R11/R12` reopen packet
- preserved same-endpoint baselines `H10/H11/R8/R9/R10/H12` and `H8/R6/R7/H9`
- preserved `H13/V1` governance/runtime handoff

## Output expectations

- root and publication docs expose `H16` as the active stage;
- one machine-readable guard records the stage switch and preserved controls;
- concrete design docs and milestone scaffolds exist for `R15/R16/R17/R18/H17`;
- the reopened lane remains same-scope and no-widening throughout.

## Acceptance

- `H16` is the canonical active driver everywhere that matters;
- `H15`, `H14`, `H13/V1`, and older same-endpoint baselines remain preserved;
- the next execution order is explicit and bounded to
  `R15 -> R16 -> R17 -> optional R18 -> H17`;
- frontier recheck remains unauthorized until an explicit later decision.
