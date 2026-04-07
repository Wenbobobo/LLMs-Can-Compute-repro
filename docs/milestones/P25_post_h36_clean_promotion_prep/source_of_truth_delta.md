# Source-Of-Truth Delta

`main` currently lacks the landed branch window from
`e7d741b` through `0b7b56c` on `wip/h35-r40-p24-exec`.

Grouped delta inventory:

## Group 1: Same-Endpoint Closeout

- `H24`, `R30`, `R31`, `H25`
- `P16`, `R32`, `H26`, `R33`, `H27`

## Group 2: Origin-Core Pivot And Refreeze

- `H28`, `R34`, `R35`, `H29`
- `R36`, `R37`, `H30`

## Group 3: Later Explicit Extension Chain

- `P17`, `H31`, `R38`, `H32`
- `P18`, `H33`, `R39`, `H34`, `P20`

## Group 4: Family-First And Bounded-Scalar Stack

- `F5`, `F6`, `F7`, `F8`
- `F10`, `F12`, `F13`, `F14`
- `P21`, `P22`, `P23`
- `H35`, `R40`, `H36`, `P24`
- saved deferred `R41` design

Promotion rule:

- inventory the full packet chain;
- promote only from the clean prep branch;
- do not treat the presence of this delta inventory as authorization to merge.
