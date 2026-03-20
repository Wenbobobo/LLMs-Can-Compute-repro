# Release Summary Draft

## Narrow target

This repository reproduces a narrow execution-substrate claim rather than a
broad “LLMs are computers” thesis. On the current validated scope, the project
supports three linked statements: deterministic computation can be encoded as an
append-only execution trace; exact latest-write retrieval over that trace can
be implemented with structured 2D hard-max retrieval; and those primitives are
enough for a small exact executor plus a tiny typed-bytecode `D0` compiled
endpoint.

## Current gate chain

The current evidence chain still runs through four fixed gates. `P3` freezes
the paper scope and its unsupported claims. `R1` keeps the precision result
positive but bounded rather than broad. `R2` remains mixed rather than
triumphant: geometry retains a strong asymptotic retrieval win, but the lowered
`exec_trace` path is still not enough to authorize frontend widening. `M7`
therefore keeps widening blocked, and `P4` keeps the blog blocked while
allowing a restrained repository landing page.

## Current endpoint and non-goals

The compiled endpoint on current evidence is tiny typed bytecode `D0`. It is
backed by deterministic verifier coverage, exact-trace / exact-final-state
agreement on the frozen starter suite, appendix-level memory-surface
diagnostics, one stress/reference follow-up, one harder-suite `R3` exactness
gate, and one bounded `R4` mechanistic-closure bundle. This endpoint should be
read as a current boundary, not as a bridge to arbitrary C, general LLM
computation, or broader demo-first claims. Those broader readings remain
explicitly unsupported on the current paper scope.

## Current paper-facing follow-up

The current frozen scope has a locked submission-candidate bundle. `P8` closed
the manuscript, appendix, and ledger lock on the same frozen endpoint. `H2`
remains the standing bundle-lock and release-hygiene gate. `P9` keeps outward
wording downstream of the locked bundle. The completed `H8/R6/R7/H9` packet
now sits as the direct same-endpoint baseline: `R6` keeps `24/24`
fixed-multiplier rows admitted, while `R7` preserves the full `8`-family
exact-admitted surface but profiles only the top `4` heaviest representatives,
stopping at `stop_decode_gain_not_material` with `0.973x` median
accelerated-vs-linear speedup and a `1980.3x` accelerated-vs-lowered ratio.
The older `H6/R3/R4/(inactive R5)/H7` packet remains the deeper
exactness/mechanism baseline on the same endpoint. `H10/H11/R8/R9/R10/H12` is
now the latest completed same-endpoint follow-up packet rather than the active
science lane. `H10` reconciles the prior packet. `H11` replaces the driver.
`R8` opens a higher retrieval-pressure gate. `R9` keeps real-trace precision
companion-only. `R10` attributes same-endpoint costs. `H12` completes the
refreeze on the same endpoint. Within that packet, `R8` now closes with `4/4`
admitted exact rows plus a bounded `2/2` decode-parity probe match, `R9` now
closes with `4/4` screened streams still `effective_here`, and `R10` now
closes with retrieval dominating representative admitted rows while median
exact-versus-lowered ratio stays around `2429.1x`. `H13/V1` is now the
preserved governance/runtime handoff rather than the active science lane. `V1`
records that `pytest --collect-only -q` succeeds on the current suite, and the
bounded top-`6` per-file timing follow-up classifies full `pytest -q` as
healthy but multi-minute rather than discovery-broken. The current active
post-`P9` stage is `H15_refreeze_and_decision_sync`, which keeps the repo
refrozen after one explicit reopen wave:
`H14_core_first_reopen_and_scope_lock`,
`R11_geometry_fastpath_reaudit`,
`R12_append_only_executor_long_horizon`,
optional `R13_small_model_executor_reactivation`,
bounded `R14_bounded_compiled_probe`,
then `H15_refreeze_and_decision_sync`. `E1c` remains conditional only and
contradiction-only on current evidence. `R11` re-audited the geometry fast
path without reopening same-endpoint speedup wording, `R12` exported exact
current executor closure plus explicit harder-slice inventory, `H14` is now
the completed reopened packet rather than the active stage, and the current
`H15` refreeze export records `R13` as inactive with `R14` unjustified.

## Reproducibility pointers

- `README.md`
- `STATUS.md`
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/manuscript_bundle_draft.md`
- `results/P1_paper_readiness/summary.json`
