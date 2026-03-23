# Release Summary Outline

Status: downstream companion to the current `H38`/`H36`-controlled paper
bundle. This file is for future release-facing summaries that must stay
shorter than the manuscript bundle and must not redefine claims.

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
- one paragraph on the current control chain
  (`H28 -> H29 -> R36 -> R37 -> H30 -> H31 -> R38 -> H32 -> H33 -> R39 -> H34 -> H35 -> R40 -> H36 -> H37 -> F16 -> H38 -> P26 -> F17`);
- one paragraph on the present compiled endpoint and blocked non-goals;
- one short reproducibility pointer block.

This summary should not contain:

- new claim wording absent from the manuscript bundle;
- speculative future frontends;
- demo-oriented rhetoric;
- broader systems claims than the current mixed systems evidence supports.

## Draft structure

### 1. Narrow target

Reproduction of a narrow execution-substrate claim: append-only traces, exact
latest-write retrieval, and a small exact executor under explicit boundaries.

### 2. Current control chain

`H38` is the current docs-only decision packet, `H36` is the preserved active
routing/refreeze packet underneath it, `P26` is the completed operational
promotion/artifact audit lane, `F16` is the current candidate-isolation
bundle, `F17` is the current same-substrate exit bundle, and `F15` remains
the current canonical derivative bundle. `H37` and `P25` remain preserved
prior decision/audit supports. `H35` is the preserved prior bounded-scalar
runtime-decision packet, `H34` and `H33` remain the preserved earlier
docs-only control packets, and `R40` plus `R39` are completed same-substrate
evidence rather than routing changes by themselves. Older controls such as
`P3`/`R1`/`R2`/`M7`/`P4` remain preserved historical context rather than the
current routing summary by themselves.

### 3. Current endpoint

The current endpoint is still a narrow same-substrate bytecode line, now
extended through one bounded richer value family: explicit bounded frame
locals plus typed `FLAG` slots. It is backed by the landed
`R37 -> H30 -> H31 -> R38 -> H32 -> H33 -> R39 -> H34 -> H35 -> R40 -> H36 -> H37 -> F16 -> H38 -> P26 -> F17`
packet chain: verifier coverage, exact-trace / exact-final-state agreement on
one tiny lowered subset, one richer control/call family, one declared
helper-body permutation audit, one bounded scalar locals/flags family, one
candidate-isolation pass with `no_candidate_ready`, and one follow-on decision
that still ends in `keep_h36_freeze`. The preserved first `D0` boundary
remains useful historical context, but the active endpoint is the whole narrow
same-substrate line, not a bridge to arbitrary `C`.

### 4. Reproducibility pointers

Point to:

- `README.md`
- `STATUS.md`
- `docs/publication_record/current_stage_driver.md`
- `docs/publication_record/claim_ladder.md`
- `docs/publication_record/manuscript_bundle_draft.md`
- `results/P1_paper_readiness/summary.json`
