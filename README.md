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
| `M4-M5` | exact retrieval/executor branches, staged-pointer caveats, and softmax negative controls remain recorded without widening |
| `M6-M7` | the tiny typed-bytecode boundary is implemented and validated; widening remains blocked |
| `P1-P10` | paper bundle, public-safe packaging, bundle-lock audits, and archive handoff remain active |
| `H4-H5` | bounded return packet completed and preserved as historical scientific baseline |
| `H6-H7` | bounded exactness/mechanism packet completed and preserved as the deeper baseline underneath the current stage |
| `H8-H9` | completed bounded `D0` long-horizon packet: `H8` replaced the driver, `R6` completed the long-horizon scaling gate, `R7` preserved the full `8`-family exact-admitted surface but profiled only the top `4` heaviest representatives, and `H9` refroze the packet |
| `H10-H12` | completed bounded `D0` retrieval-pressure packet: `H10` reconciles `R7` to artifact-backed wording, `H11` replaces the driver, `R8` stresses higher retrieval pressure on the same endpoint, `R9` keeps real-trace precision companion-only, `R10` attributes same-endpoint costs, and `H12` refreezes the packet |
| `H13-V1` | completed governance/runtime handoff preserved as a control baseline: `H13` kept the completed checkpoint explicit, `V1` classified the slow full-suite `pytest -q` gate as `healthy_but_slow`, and outward-sync audits were tightened without widening scope |
| `H14-H15` | completed bounded core-first reopen/refreeze packet: `H14` locked the reopened lane to exact 2D retrieval plus append-only/latest-write execution, `R11/R12` landed on bounded evidence, `R13` stayed inactive, `R14` stayed unjustified, and `H15` refroze the repo on the same endpoint |

## Current Gate Outcome

- The current active stage still starts from the locked submission-candidate
  bundle and restrained release-candidate checkpoint created by `P8/P9`.
- The precision story remains bounded rather than broad: float32 single-head
  fails on `12/25` tracked real/organic streams, `7/25` already at `1x`, while
  at least one decomposition stays exact on `25/25` tracked streams in the
  validated suite.
- The systems gate remains mixed: geometry is strongly positive, but the
  lowered path is still about `1.82x` slower than the best current
  reference/oracle path on positive `D0` suites.
- `R6` keeps the completed long-horizon packet positive on the same endpoint:
  `24/24` fixed-multiplier rows stay admitted, `8/8` longer-row decode-parity
  checks match exactly, and the narrow multiplier-`8` precision companion
  finds `4/8` boundary-bearing streams while the weaker control fails on `2/4`
  of those boundary-bearing rows.
- `R7` preserved the full `8`-family exact-admitted `R6` index but only
  profiled the top `4` heaviest family representatives on the same endpoint;
  all `4/4` profiled rows stayed exact, accelerated Hull decode reached only
  about `0.973x` of linear on median, and it still ran about `1980.3x` slower
  per step than the lowered path.
- `R8` stresses higher retrieval pressure on the same endpoint and is now
  closed on a bounded harder-family gate: `4/4` exact rows remain admitted,
  the bounded top-`2` decode-parity probe matches on `2/2` rows, and
  retrieval pressure grows to about `1.249x` max events and `1.560x` max
  total candidate depth versus the admitted `R6` `8x` source rows.
- `R9` keeps real-trace precision companion-only and is now closed on the
  admitted `R8` memory streams: all `4/4` screened streams stay
  `effective_here`, one `single_head` `tie_collapse` appears at `1x` on the
  helper-checkpoint-braid-long stream, the default decomposition grid still
  passes there, and the weaker negative control does not fail.
- `R10` attributes same-endpoint costs and is now closed on representative
  admitted rows: median exact-versus-lowered runtime is still about
  `2429.1x`, median retrieval share is about `99.8%`, harness share is
  effectively negligible, and retrieval dominates on `4/4` profiled rows.
- `H8/R6/R7/H9` now sits as the completed direct same-endpoint baseline, while
  `H6/R3/R4/(inactive R5)/H7` remains the older exactness/mechanism baseline
  underneath it.
- `H10/H11/R8/R9/R10/H12` is now the latest completed same-endpoint follow-up
  packet rather than the active science lane. It keeps the same endpoint
  fixed, closes `R8/R9/R10` on bounded evidence, and leaves `H12` as the
  completed refreeze lane for the current scientific checkpoint.
- `H13/V1` remains preserved as the completed governance/runtime handoff:
  `pytest --collect-only -q` succeeds on the current suite, the bounded top-`6`
  timing follow-up classifies full `pytest -q` as healthy but multi-minute,
  and outward-sync control remains machine-audited.
- The current active post-`P9` stage is `H15_refreeze_and_decision_sync`.
  It does not open a new science lane; it keeps the repo refrozen after one
  explicit reopen wave on the same narrow mechanism path.
- `H14_core_first_reopen_and_scope_lock` is now the completed reopened packet
  rather than the active stage. That packet kept work bounded to exact `2D`
  geometry plus append-only/latest-write execution, ran `R11` before `R12`,
  left `R13` inactive, and left `R14` downstream rather than authorizing
  compiled widening by wording alone.
- `R11` has now closed on a bounded current-code re-audit: the geometry parity
  slice stays exact on `5/5` audited cases, preserved cache-versus-bruteforce
  speedup ranges from about `42.8x` to `249.2x`, and same-endpoint lowered-path
  speedup wording remains blocked.
- `R12` has now closed on a bounded reopened executor export: current
  `exact_linear`, `exact_accelerated`, and bounded `trainable_stack` modes all
  remain exact on the exported suites, the longest heldout countdown still
  reaches `104` steps, and the next harder-slice inventory is explicit across
  `24` staged `R6` rows plus `4` staged `R8` rows.
- Current `H15` refreeze state is `direct_refreeze_complete`: `R13` remained
  inactive because no bounded executor gap was exposed, and `R14` remained
  unjustified because no compiled follow-up need was shown on the fixed `D0`
  endpoint.
- V1 remains a standing operational reference under the preserved `H13`
  handoff rather than an active science lane.
- The compiled endpoint remains tiny typed bytecode `D0`; no active lane
  authorizes frontend widening, arbitrary compiled-language claims, or a
  broader “LLMs are computers” thesis.
- `E1c` stays conditional only and contradiction-only throughout the packet.

## Start Here

- `STATUS.md` — current repository state and immediate gates
- `docs/publication_record/current_stage_driver.md` — canonical current refrozen-stage driver
- `tmp/2026-03-20-h14-core-first-reopen-master-plan.md` — saved execution order for the current reopened lane
- `results/H15_refreeze_and_decision_sync/summary.json` — one-file entrypoint for the current `H15` refrozen state, explicit `R13/R14` decisions, and synchronized control surface
- `results/H14_core_first_reopen_guard/summary.json` — preserved guard for the completed `H14` core-first reopen packet, preserved `H13/V1` handoff, and standing controls
- `results/H13_post_h12_governance_stage_health/summary.json` — preserved governance/runtime handoff reference for the completed `H13/V1` control stack
- `results/V1_full_suite_validation_runtime_audit/summary.json` — bounded runtime-classification audit for the full-suite validation gate
- `results/V1_full_suite_validation_runtime_timing_followup/summary.json` — bounded top-`6` per-file timing classification for the full-suite validation gate
- `results/release_worktree_hygiene_snapshot/summary.json` — machine-readable snapshot of whether the current worktree blocks a release-facing commit
- `results/release_preflight_checklist_audit/summary.json` — machine-readable outward release-preflight audit over release-facing docs, frozen paper-facing ledgers, and standing summaries
- `results/H10_r7_reconciliation_guard/summary.json` — reconciliation guard for the corrected `R7` top-`4` profile wording
- `results/H11_post_h9_mainline_rollover_guard/summary.json` — driver-alignment guard for the current retrieval-pressure packet under the reopened stage
- `results/R8_d0_retrieval_pressure_gate/summary.json` — completed bounded heavier-family retrieval-pressure gate on the same fixed `D0` endpoint
- `results/R9_d0_real_trace_precision_boundary_companion/summary.json` — completed bounded real-trace precision companion on admitted `R8` memory streams
- `results/R10_d0_same_endpoint_cost_attribution/summary.json` — completed representative-row same-endpoint cost attribution on admitted `R6/R8` rows
- `results/R7_d0_same_endpoint_runtime_bridge/summary.json` — completed same-endpoint runtime bridge on the preserved `8`-family admitted surface with bounded top-`4` profiling
- `results/R6_d0_long_horizon_scaling_gate/summary.json` — completed fixed-multiplier long-horizon exactness gate on current scalable `D0` families
- `results/R3_d0_exact_execution_stress_gate/summary.json` — preserved harder-suite exactness baseline on the current `D0` endpoint
- `results/R4_mechanistic_retrieval_closure/summary.json` — preserved mechanistic-closure baseline on the current positive `D0` suites
- `docs/publication_record/submission_packet_index.md` — venue-agnostic submission/archive handoff
- `docs/publication_record/claim_ladder.md` — claim boundary summary
- `docs/publication_record/claim_evidence_table.md` — artifact-to-claim map
- `docs/publication_record/manuscript_bundle_draft.md` — current manuscript section draft
- `docs/milestones/H15_refreeze_and_decision_sync/` — current refrozen-stage staging area
- `docs/milestones/H14_core_first_reopen_and_scope_lock/` — preserved reopen-packet staging area

## Quickstart

The intended workflow uses Python `3.12` and `uv`.

```bash
uv sync --group dev
uv run pytest -q
```

Common export commands:

```bash
uv run python scripts/export_h14_core_first_reopen_guard.py
uv run python scripts/export_h15_refreeze_and_decision_sync.py
uv run python scripts/export_h10_r7_reconciliation_guard.py
uv run python scripts/export_h11_post_h9_mainline_rollover_guard.py
uv run python scripts/export_h8_driver_replacement_guard.py
uv run python scripts/export_h6_mainline_rollover_guard.py
uv run python scripts/export_v1_full_suite_validation_runtime_audit.py
uv run python scripts/export_v1_full_suite_validation_runtime_timing_followup.py
uv run python scripts/export_h13_post_h12_governance_stage_health.py
uv run python scripts/export_release_worktree_hygiene_snapshot.py
uv run python scripts/export_release_preflight_checklist_audit.py
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
