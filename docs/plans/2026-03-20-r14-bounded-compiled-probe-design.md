# R14 Bounded Compiled Probe Design

## Goal

Define the only compiled follow-up allowed inside the reopened stage: a bounded
probe that remains on tiny typed bytecode `D0` and downstream of the core
mechanistic closure work.

## Scope

- same fixed `D0` endpoint only;
- no arbitrary C;
- no frontend widening;
- no prose that implies general compiled-language closure.

## Preconditions

- `R11` has refreshed geometry/fast-path wording on current code;
- `R12` has pushed append-only/latest-write execution farther on the same
  endpoint;
- if needed, `R13` has clarified whether a small trainable bridge changes the
  interpretation of remaining executor gaps.

## Expected reads

- `src/bytecode/__init__.py`
- `src/bytecode/datasets.py`
- `results/M6_typed_bytecode_harness/`
- `results/R3_d0_exact_execution_stress_gate/summary.json`
- `results/R10_d0_same_endpoint_cost_attribution/summary.json`

## Acceptance

- any compiled probe remains demonstrably downstream of the reopened core;
- claim language stays bounded to tiny typed bytecode `D0`;
- the stage can still refreeze cleanly under `H15` without widening.
