# P27 Main Delta Summary

The current comparison target remains `main`. The current clean source branch
for the aggressive long-arc line is `wip/h41-r43-mainline`.

`P27` records the delta between those two branches without treating the mere
presence of a delta as authorization to merge. Exact commit and file counts are
captured in the machine-readable `results/P27.../summary.json` exporter output.
The only guaranteed posture in this packet is that the delta is nonzero and
reviewable from a clean branch.

The reviewable merge set is the coherent post-`H36` packet window carried by
the clean source branch:

- `P25 -> F15 -> H37 -> F16 -> H38 -> P26 -> F17 -> F18 -> F19 -> H40 -> R42 -> F20 -> H41 -> P27`

Dirty `main` remains untouched in this wave. Do not treat this delta inventory
as authorization to:

- merge `main` immediately;
- execute `R43`;
- execute `R45`; or
- widen the restricted semantic-boundary claim surface.
