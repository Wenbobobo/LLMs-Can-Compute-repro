# H4 Reproduction Mainline Return Design

## Goal

Move the active stage back to the reproduction mainline while preserving the
current narrow claim boundary and the locked submission/release checkpoint as
the baseline.

## Why now

The repo finished a useful documentation and packet-consolidation wave, but
the user explicitly re-prioritized the scientific mainline: paper/blog polish
should remain downstream, while the next active work should tighten the
precision and systems story on the already frozen scope.

## Intended outputs

- one saved master plan in `tmp/`;
- one updated `current_stage_driver.md` naming `H4`, `E1a`, `E1b`, conditional
  `E1c`, and `H5`;
- synchronized `README.md`, `STATUS.md`, publication-record entry docs, and
  short release summary;
- one `H4` milestone scaffold;
- one machine-readable guard export for the new stage wording.

## Acceptance

- the repo no longer presents `H3/P10/P11/F1` as the live stage packet;
- the active stage is explicitly a bounded scientific-return packet;
- the repo still blocks arbitrary C, general “LLMs are computers” language,
  and frontend widening;
- the new `H4` guard export passes.
