# llms-can-compute-repro

Careful reproduction of the execution-substrate claims behind Percepta's field
note _Can LLMs Be Computers?_

This repository tests a narrow thesis:

1. deterministic computation can be encoded as an append-only execution trace;
2. exact “latest relevant write” retrieval over that trace can be implemented
   with specialized mechanisms, including structured 2D hard-max retrieval;
3. those primitives may be sufficient for a small exact executor.

This repository does **not** claim that general LLMs are computers, that
arbitrary C has been reproduced, or that presentation-first demos are evidence.

## Current Boundary

| Track | Current state |
| --- | --- |
| `M0-M3` | repo scaffold, claim discipline, geometry core, and append-only trace executor are in place |
| `M4` | exact retrieval/executor branches, staged-pointer caveats, and real-trace precision boundaries are exported |
| `M5` | matched softmax baselines remain negative controls rather than positive evidence |
| `M6` | the tiny typed-bytecode boundary is implemented and validated with a memory-surface diagnostic companion and a stress/reference follow-up |
| `P1-P2` | paper bundle and public-safe packaging ledgers are active |
| `P3-R2` | claim freeze, precision closure, and systems gate are exported; the systems result is mixed rather than triumphant |
| `M7-P4` | the project stays on tiny typed bytecode, frontend widening is not authorized, and the blog remains blocked |

## Current Gate Outcome

- `P3` freezes the current paper scope without blocked figure/table items.
- `R1` closes the precision story as a narrowed boundary, not a broad robustness claim.
- `R2` stays mixed: geometry is strongly positive, but the lowered path is not yet competitive on current `D0` suites.
- `M7` keeps the compiled endpoint at the current tiny typed-bytecode boundary.
- `P4` allows the README to remain a restrained landing page and keeps the blog blocked.

The next engineering work is paper-lane assembly and any future systems revisit,
not frontend widening or demo-first expansion.

## Start Here

- `STATUS.md` — current repository state and immediate gates
- `docs/publication_record/claim_ladder.md` — claim boundary summary
- `docs/publication_record/claim_evidence_table.md` — artifact-to-claim map
- `docs/milestones/P1_paper_readiness/` — current paper bundle staging area
- `docs/milestones/P2_public_research_packaging/` — public-safe packaging ledger

## Quickstart

The intended workflow uses Python `3.12` and `uv`.

```bash
uv sync --group dev
uv run pytest -q
```

Common export commands:

```bash
uv run python scripts/export_p1_figure_table_sources.py
uv run python scripts/render_p1_paper_artifacts.py
uv run python scripts/export_p1_paper_readiness.py
uv run python scripts/export_m7_frontend_candidate_decision.py
uv run python scripts/export_p4_blog_release_gate.py
```

## Repository Layout

- `docs/` — milestone logs, plans, claim ledgers, publication notes
- `src/` — geometry, trace execution, model branches, typed-bytecode harness
- `scripts/` — export and rendering entrypoints
- `tests/` — regression and artifact tests
- `results/` — tracked benchmark summaries and milestone outputs

## Public Material Policy

`docs/Origin/` contains local-only source material and stays out of version
control. The public repository stores derived notes, code, benchmark outputs,
claim ledgers, and explicit accounting of what was and was not reproduced.
