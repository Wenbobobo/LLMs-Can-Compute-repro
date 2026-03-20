# V1 Per-File Timing Follow-Up Design

## Goal

Turn the existing `V1` heuristic shortlist into one bounded timing follow-up
 so unattended runs can distinguish "healthy but slow" from "needs deeper
 split" without reopening scientific scope.

## Approach

- keep `scripts/export_v1_full_suite_validation_runtime_audit.py` as the fast
  collect-only and inventory pass;
- add one separate exporter that reads the current `V1` inventory and times a
  bounded subset of likely runtime-heavy files with `pytest -q <file>
  --durations=0`;
- prioritize `model_or_training` files before other categories because they are
  the likeliest cumulative runtime source in the current suite;
- cap the follow-up at a small fixed shortlist so the follow-up itself remains
  bounded and reproducible.

## Scope Lock

- do not change scientific code, claim wording, or standing scientific gates;
- do not treat one bounded timing pass as proof that full `pytest -q` is always
  safe for short unattended windows;
- do not silently discard the slower files from the audit record.

## Intended Outputs

- one machine-readable timing summary for the bounded shortlist;
- one per-file timing table with wall-clock time, pytest summary line, and
  slowest reported test rows;
- one explicit classification: bounded follow-up complete, healthy-but-slow, or
  needs function-level split.

## Acceptance

- the follow-up records a bounded shortlist and its selection rule;
- each selected file reports return status and wall-clock timing;
- the final summary leaves one explicit next operational step for unattended
  runs.
