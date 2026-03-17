# M3 Trace Executor Results

## Exported Trace Artifacts

- `countdown_4_trace.json`: stack-only countdown example
- `latest_write_trace.json`: overwrite-and-read example for last-write-wins memory
- `memory_accumulator_trace.json`: bounded RAM example with multiple slots

## Current Meaning

These artifacts demonstrate that the reference interpreter emits deterministic
append-only traces whose final state can be reconstructed exactly by replay.

The bounded RAM extension currently supports:

- immediate-address `STORE`,
- immediate-address `LOAD`,
- zero-initialized reads for unwritten addresses,
- latest-write reconstruction from the trace alone.

This is still a reference-semantics branch. No learned executor has been added
yet.
