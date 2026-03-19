# llms-can-compute-repro

Careful reproduction of a narrowed execution-substrate reading of Percepta's
field note _Can LLMs Be Computers?_

This repository tracks a paper-grade endpoint:

1. deterministic computation can be encoded as an append-only execution trace;
2. exact latest-write retrieval over that trace can be implemented with
   structured 2D hard-max retrieval;
3. on the current validated scope, those primitives support a small exact
   executor and a tiny typed-bytecode `D0` compiled endpoint.

This repository does **not** claim that general LLMs are computers, that
arbitrary C has been reproduced, or that demo-first presentation is evidence.

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

- The current paper scope is frozen, and the paper-readiness export reports `10/10` ready figure/table items on that scope.
- The precision story is closed as a narrowed boundary: float32 single-head fails on `12/25` tracked real/organic trace streams, `7/25` already at `1x`, while at least one decomposition stays exact on `25/25` tracked streams.
- The systems gate remains mixed: geometry is strongly positive, but the lowered path is still about `1.82x` slower than the best current reference/oracle path on positive `D0` suites.
- The compiled endpoint stays at the current tiny typed-bytecode boundary.
- The restrained public surface remains downstream of the locked submission-candidate bundle, and broader blog/demo release stays blocked.
- The active post-`P9` stage is checkpoint consolidation and archive packaging: `H3` fixes driver/gate semantics, `P10` builds a venue-agnostic submission/archive packet, `P11` prepares downstream-only derivative material, and `F1` preauthors dormant `E1` patch playbooks.
- No `E1` patch lane is active; any new evidence still routes through `docs/publication_record/conditional_reopen_protocol.md`.

## Start Here

- `STATUS.md` — current repository state and immediate gates
- `docs/publication_record/current_stage_driver.md` — canonical active-stage driver
- `docs/publication_record/submission_packet_index.md` — venue-agnostic submission/archive handoff
- `docs/publication_record/claim_ladder.md` — claim boundary summary
- `docs/publication_record/claim_evidence_table.md` — artifact-to-claim map
- `docs/publication_record/manuscript_bundle_draft.md` — current manuscript section draft
- `docs/milestones/P1_paper_readiness/` — current paper bundle staging area

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
uv run python scripts/export_p5_public_surface_sync.py
uv run python scripts/export_h2_bundle_lock_audit.py
uv run python scripts/export_p10_submission_archive_ready.py
```

## Repository Layout

- `docs/` — milestone logs, plans, claim ledgers, publication notes
- `src/` — geometry, trace execution, model branches, typed-bytecode harness
- `scripts/` — export and rendering entrypoints
- `tests/` — regression and artifact tests
- `results/` — tracked benchmark summaries and milestone outputs

## Public Material Policy

`docs/Origin/` and `docs/origin/` contain local-only source material and stay
out of version control. The public repository stores derived notes, code,
benchmark outputs, claim ledgers, and explicit accounting of what was and was
not reproduced.
