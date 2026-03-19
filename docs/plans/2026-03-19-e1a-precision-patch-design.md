# E1a Precision Patch Design

## Trigger

The frozen precision wording is narrow, but the current evidence surface does
not yet expose one compact lane-local bundle that shows all three facts at
once:

1. single-head float32 failures are common on the tracked suite;
2. at least one decomposition remains exact on all tracked streams;
3. weaker decomposition settings still fail on part of the broadened organic
   slice.

Without that third slice, bounded wording can still be read too generously.

## Goal

Package the current bounded-precision story into one smaller reopen bundle that
sharpens the current-suite boundary without adding new trace families or
relabeling the result as universal robustness.

## Intended outputs

- one `E1a` milestone scaffold;
- one lane-local export producing stream-first-failure rows, family boundary
  rows, explicit weak negative-control rows, and claim-impact wording;
- synchronized precision ledgers under the same `C3d/C3e` boundary.

## Scope lock

- current validated trace families only;
- no new program families;
- no systems or compiled-boundary work;
- no claim of general long-horizon precision robustness.

## Acceptance

- `C3d/C3e` remain bounded current-suite positives rather than universal
  positives;
- the weak decomposition negative control is explicit in machine-readable form;
- the systems gate and `D0` boundary remain unchanged.
