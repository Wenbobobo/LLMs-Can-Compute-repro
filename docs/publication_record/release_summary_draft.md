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

The current evidence chain runs through four gates. `P3` freezes the paper
scope and its unsupported claims. `R1` keeps the precision result positive but
bounded:
float32 single-head fails on `12/25` tracked real/organic trace streams, with
`7/25` failing already at `1x`, while at least one decomposition stays exact on
`25/25` tracked streams in the validated suite. `R2` remains mixed rather than
triumphant: geometry retains a strong asymptotic retrieval win, but the lowered
`exec_trace` path is still about `1.82x` slower than the best current
reference/oracle path on positive `D0` suites. `M7` therefore blocks frontend
widening, and `P4` keeps the blog blocked while allowing a restrained
repository landing page.

## Current endpoint and non-goals

The compiled endpoint on current evidence is tiny typed bytecode `D0`. It is
backed by deterministic verifier coverage, exact-trace / exact-final-state
agreement on the frozen starter suite, appendix-level memory-surface
diagnostics, and one stress/reference follow-up. This endpoint should be read
as a current boundary, not as a bridge to arbitrary C, general LLM
computation, or broader demo-first claims. Those broader readings remain
explicitly unsupported on the current paper scope.

## Current paper-facing follow-up

The current frozen scope now has a locked submission-candidate bundle and a
restrained release-candidate public surface. `P8` closed the manuscript,
appendix, and ledger lock on the same frozen endpoint, `H2` remains the
standing bundle-lock and release-hygiene gate, and `P9` keeps outward wording
downstream of the locked bundle. The next major change should come from a
later full plan-mode stage or a named `E1` patch lane, not from claim
expansion.

## Reproducibility pointers

- `README.md`
- `STATUS.md`
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/manuscript_bundle_draft.md`
- `results/P1_paper_readiness/summary.json`
