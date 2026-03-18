# Research Notes

## Stress-family options

1. Branch-heavy helper braid.
   Stresses call/ret scheduling and branch predicates, but may under-pressure
   heap/frame alias surfaces.
2. Frame/heap checkpoint braid.
   Stresses helper reuse plus memory surfaces, but may be too memory-centric.
3. Branch-selected helper checkpoint braid.
   Main loop branches on a selector, calls one of two static helpers, both
   helpers touch frame and heap differently, and the main path periodically
   replays heap checkpoints back into frame state.

Recommended option:
- option 3, because it exercises the current boundary more completely without
  introducing new semantics.

## External-reference options

1. Standalone Python spec interpreter with no lowering reuse.
2. Golden trace fixtures only.
3. Separate systems-language interpreter.

Recommended option:
- option 1. It is independent enough for this narrow slice and far cheaper
  than introducing a second implementation language.

## Comparison schema

For positive rows:

- verifier pass/fail;
- current bytecode interpreter vs external reference:
  exact trace on medium rows,
  exact final state on long rows;
- lowered `exec_trace` path vs external reference on the same target;
- current bytecode interpreter vs lowered `exec_trace` path on the same target;
- memory-surface diagnostic agreement remains a companion check between the
  current bytecode path and the lowered path.

For negative rows:

- verifier rejection class and first error location;
- external reference rejection class or equivalent contract failure;
- agreement label: matched rejection / mismatched rejection.

## Stop/go rule

Broader compiled demos stay blocked unless all of the following are true:

1. `M6_boundary_freeze` remains valid with no triggered contradiction.
2. All positive stress rows agree across verifier, current bytecode path,
   lowered path, and external reference on the declared target.
3. All negative rows fail deterministically with matched contract-level
   rejection.
4. `P1` and `P2` ledgers remain synchronized without widening the claim
   language.
