# Family Scope

Selected family:

- `bounded_scalar_locals_and_flags`

Included semantics:

- exact booleans used as branch-visible flags;
- bounded integer-like loop counters with explicit finite range;
- literal local cells whose value is fully visible to the executor;
- single-cell reads and writes that can still be phrased as latest-write over a
  named local slot or flag slot.

Explicit exclusions:

- typed multi-cell records;
- symbolic labels or indirect targets as value payloads;
- external effects or host-environment values;
- planner-produced objects or latent summaries;
- heap-like aliasing, dynamic shape growth, or any value family that needs a
  new opcode surface.

Working interpretation:

- this family is still close to the current executor floor;
- it is richer than the current baseline because the values are no longer only
  event ids, addresses, stack slots, or return targets;
- it must still remain legible as bounded scalar state rather than richer data
  structure semantics.
