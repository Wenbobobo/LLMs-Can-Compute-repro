# Research Notes

- The key leverage is to detect memory divergences without widening the control-flow contract already proven in `M6_typed_bytecode_harness`.
- Append-only trace invariants help identify exactly where heap/stack stamping now appears; the instrumentation should annotate those points rather than rewriting them.
- Metadata should capture access sets (read/write) per instruction so the differential harness can correlate a mnemonic with the exact-final-state change.
