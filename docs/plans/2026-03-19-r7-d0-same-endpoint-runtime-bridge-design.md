# R7 D0 Same-Endpoint Runtime Bridge Design

## Goal

Measure what decode acceleration buys inside the current exact `D0` endpoint,
without reopening a broader systems lane.

## Intended outputs

- one exact-admitted index sourced from `R6`;
- same-endpoint runtime rows for bytecode, lowered `exec_trace`, linear exact
  decode, and accelerated Hull decode on the heaviest exact-admitted family
  representatives;
- per-family bridge summaries;
- one fixed stop/go assessment explaining whether decode-level speedup is
  material and whether it closes meaningfully toward the lowered path.

## Scope lock

- consume the full exact-admitted `R6` index, but profile only the heaviest
  representatives when the exact long-row runtime surface exceeds unattended
  execution budget;
- no widened suites, no new frontend, no broader systems benchmark matrix;
- a positive runtime signal still does not equal end-to-end systems dominance.

## Acceptance

- any exactness contradiction is surfaced explicitly;
- same-endpoint speedup vs linear decode is quantified on the long rows;
- the stop/go conclusion is machine-readable and conservative.
