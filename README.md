# llms-can-compute-repro

Careful reproduction of the core execution-substrate claims behind Percepta's
field note _Can LLMs Be Computers?_

This repository does **not** try to validate the headline literally.
The working target is narrower and more falsifiable:

1. Can long exact computation be encoded as an append-only execution trace?
2. Can critical reads over that trace be reduced from linear scan to sublinear
   geometric retrieval under a 2D hard-max regime?
3. Are those primitives sufficient to support a small exact executor?

## Current Status

| Milestone | Scope | Status |
| --- | --- | --- |
| M0 | Public-safe scaffold, repo policy, research docs | complete |
| M1 | Claims/scope lock, acceptance criteria, ambiguity register | complete |
| M2 | Exact 2D hard-max geometry core | benchmarked correctness-first implementation |
| M3 | Append-only trace DSL and reference executor | stack plus bounded-RAM reference semantics recorded |
| M4 | Exact hard-max model branch | free-running exact executor plus narrow trainable slice |
| M5 | Standard 2D-head softmax baseline | scaffold started |
| M6 | Restricted compiled-program demos | planned |

## Reproduction Stance

- Treat the public source as a field note, not a complete artifact release.
- Prioritize mechanistic clarity over resemblance to blog demos.
- Keep exact hard-max, standard softmax, and approximate branches separate.
- Judge success by free-running exact execution, not token plausibility.
- Narrow claims when evidence is narrow.

## Public Material Policy

Raw source materials are kept in a local-only `docs/Origin/` directory and are
excluded from version control. The public repository stores:

- structured notes,
- claim decomposition,
- implementation artifacts,
- benchmark outputs,
- and explicit accounting of what was or was not reproduced.

## Repository Layout

- `docs/` — design docs, claim matrices, milestone logs
- `src/geometry/` — exact hard-max reference path and accelerated cache
- `src/exec_trace/` — append-only trace DSL, interpreter, replay
- `src/model/` — later model branches
- `src/benchmarks/` — benchmark helpers
- `tests/` — unit tests and regression tests
- `scripts/` — runnable benchmark and smoke-test entrypoints
- `results/` — tracked benchmark summaries and milestone outputs

## Near-Term Acceptance Criteria

- `HullKVCache` matches brute-force hard-max exactly, including ties.
- Geometry benchmarks show clearly sublinear query growth against history size.
- The trace interpreter and replay engine agree on final state exactly.
- The free-running exact executor reproduces reference traces by length bucket.
- The project remains honest about unsupported claims and unresolved ambiguity.

## Environment

The intended workflow uses Python 3.12 and `uv`.

```bash
uv sync --group dev
pytest
python scripts/benchmark_geometry.py
```

Optional `M5` scaffold work can use:

```bash
uv sync --group dev --group m5
```
