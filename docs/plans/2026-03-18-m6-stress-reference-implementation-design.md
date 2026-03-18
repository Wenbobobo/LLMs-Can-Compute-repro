# M6 Stress/Reference Implementation Design

> Status note (2026-03-19): completed. The stress/reference implementation
> batch described here has landed; keep this file as historical context only.

## Purpose

This is the next-stage execution plan after the current planning-only stage is
complete. It does not reopen scope. It converts the frozen `D0` boundary into
one concrete implementation batch.

## Scope lock

- keep the current tiny typed-bytecode semantics;
- keep static-target non-recursive control flow;
- keep memory-surface diagnostics as a companion layer;
- do not add Wasm-like frontend work, arbitrary C claims, or new runtime
  features.

## Execution phases

### Phase 1 — standalone Python spec interpreter

- implement a spec interpreter for the frozen bytecode surface that does not
  reuse lowering logic;
- support the current positive and negative suites first;
- expose trace/final-state outputs plus deterministic rejection metadata.

### Phase 2 — branch-selected helper checkpoint braid suite

- add one branch-selected helper checkpoint braid family with:
  `2` medium exact-trace rows on distinct helper/checkpoint paths,
  `1` long exact-final-state row,
  `2` matched negatives.

### Phase 3 — oracle agreement harness

- compare:
  verifier,
  current bytecode interpreter,
  lowered `exec_trace` path,
  standalone Python spec interpreter;
- keep memory-surface agreement as a companion comparison between current
  bytecode and lowered paths.

### Phase 4 — export and ledger sync

- export one dedicated result bundle for the follow-up;
- update `P1` table sources and renders;
- update `P2` release ledger and root docs only after the result bundle is
  stable.

## Parallelization

- Phase 1 and Phase 2 can proceed in parallel once the comparison schema is
  frozen.
- Phase 3 starts only after both land.
- Phase 4 stays last.

## Stop conditions

- if the stress family needs a new semantic feature, stop and return to
  `M6_boundary_freeze`;
- if the standalone spec interpreter disagrees on the frozen pre-existing
  suite, stop and debug before adding stress rows;
- if `P1` wording needs broader claims to describe the result, stop and narrow
  the implementation target instead.
