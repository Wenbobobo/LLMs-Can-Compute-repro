# Post-M6 Boundary Freeze Design

> Status note (2026-03-19): completed/superseded after the `M6-E`
> stress/reference closure. Use `tmp/2026-03-18-next-stage-plan.md` and the
> `P3`/`R1`/`R2`/`M7` milestone docs for the current next-stage plan.

## Why this plan exists

`M6_typed_bytecode_harness`, `M6_memory_surface_followup`, and the latest `P1`
sync changed the gating logic again. The repository now has:

- a concrete tiny typed-bytecode verifier / lowering / differential harness;
- a narrow control-flow-first widening with static-target non-recursive
  `call/ret`;
- an appendix-level memory-surface diagnostic layer that still preserves the
  same `D0` claim row rather than creating a new layer.

That means the next phase should not jump to Wasm, arbitrary C, or public demo
polish. The right move is to treat the current `D0` slice as almost frozen and
close the last pre-demo uncertainty: whether this boundary survives one serious
stress family plus an external reference comparison.

## Option comparison

### Option A — start compiled demos now

Benefit:
- fast visible progress.

Problem:
- this would turn the current narrow `D0` evidence into presentation pressure
  before the mechanism is closed tightly enough.

Verdict:
- rejected.

### Option B — freeze `D0`, add one stress family, add one external reference

Benefit:
- keeps the scientific target narrow;
- answers the most important remaining question without inventing a broader
  language surface;
- produces a stronger paper-safe stop/go gate for any later compiled demo.

Cost:
- slower than jumping directly to presentation artifacts.

Verdict:
- recommended.

### Option C — stop experiments and do packaging only

Benefit:
- cheapest documentation path.

Problem:
- leaves one obvious mechanistic gap open: the current harness still has no
  third oracle path and no single “serious stress” that pressures the frozen
  bytecode boundary.

Verdict:
- too early.

## Chosen near-term tracks

### Track A — `M6-D` boundary freeze

Purpose:
- treat the current control-flow + memory-surface slice as the last pre-demo
  widening unless a concrete contradiction appears.

Required outputs:
- synced README / STATUS / milestone docs;
- explicit note that memory-surface diagnostics are `D0`-supporting only;
- a stop/go rule for any later frontend surface.

### Track B — `M6-E` one serious stress + external reference

Purpose:
- pressure the tiny-bytecode boundary without broadening the language.

Default decisions:
- stay inside current types (`i32`, `addr`, `flag`);
- stay non-recursive and static-target;
- choose a stress family that combines loop, branch, helper call, and
  frame/heap touches rather than adding new runtime features;
- add an external reference interpreter comparison before any compiled demo
  narrative.

Exit conditions:
- stress family has deterministic verifier status and exact differential
  results on the agreed comparison target;
- the external reference path agrees on the current positive and negative
  suites.

### Track C — `P2` public packaging

Purpose:
- keep public-safe packaging ledger-first while `M6-D/E` closes.

Required outputs:
- a public/restricted artifact ledger;
- exact reproduction commands for `P1` and `M6` exports under Python 3.12 +
  `uv`;
- blocked blog triggers tied to claim and experiment state, not intuition.

## Parallelization rules

- `Track A` and `Track C` can proceed immediately and in parallel because they
  are documentation / ledger work.
- `Track B` starts with spec and acceptance work first; actual implementation
  should stay inside the tiny-bytecode surface.
- broader compiled demos remain blocked until `Track B` finishes and `P1`
  stays synchronized without widening the claim language.

## Non-goals

- no Wasm subset yet;
- no arbitrary C claim;
- no new claim layer beyond current `D0` / `C2h` / `C3e`;
- no blog-first framing;
- no reopening `M5` unless the fair comparison surface changes materially.
