# Release Summary Outline

Status: downstream companion to the manuscript bundle. This file is for future
release-facing summaries that must stay shorter than the manuscript bundle and
must not redefine claims.

## Purpose

The manuscript bundle is now large enough that it should remain the primary
paper-facing draft. Future release-facing updates should therefore use a
separate short summary rather than repeatedly compressing the manuscript bundle
back into `README.md`-style prose. This keeps the long-form paper argument and
the short public-facing repository summary aligned without forcing them to be
the same document.

## Scope

This summary should contain only:

- one paragraph on the narrowed scientific target;
- one paragraph on the current gate chain (`P3`, `R1`, `R2`, `M7`, `P4`);
- one paragraph on the present compiled endpoint and blocked non-goals;
- one short reproducibility pointer block.

This summary should not contain:

- new claim wording absent from the manuscript bundle;
- speculative future frontends;
- demo-oriented rhetoric;
- broader systems claims than the current `R2` result supports.

## Draft structure

### 1. Narrow target

Reproduction of a narrow execution-substrate claim: append-only traces, exact
latest-write retrieval, and a small exact executor under explicit boundaries.

### 2. Current gate chain

`P3` freezes the current paper scope, `R1` gives a bounded precision result,
`R2` is mixed, `M7` blocks frontend widening, and `P4` keeps the blog blocked
while allowing a restrained repository landing page.

### 3. Current endpoint

The current compiled endpoint is tiny typed bytecode `D0`, backed by verifier
coverage, exact-trace / exact-final-state agreement, memory-surface companion
diagnostics, and one stress/reference follow-up. It is an endpoint on current
evidence, not a bridge to arbitrary C.

### 4. Reproducibility pointers

Point to:

- `README.md`
- `STATUS.md`
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/manuscript_bundle_draft.md`
- `results/P1_paper_readiness/summary.json`
