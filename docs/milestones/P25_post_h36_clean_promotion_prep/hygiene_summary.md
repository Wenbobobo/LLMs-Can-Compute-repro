# Hygiene Summary

- `wip/h35-r40-p24-exec` is the clean scientific source of truth for the
  current bounded-scalar stack.
- `wip/p25-f15-h37-exec` is the clean promotion-prep branch created from that
  source state.
- `main` remains dirty and behind the current packet chain.
- promotion is therefore inventory-only in this lane.
- any later merge attempt must start from the clean prep branch, not from the
  dirty integrated tree.
