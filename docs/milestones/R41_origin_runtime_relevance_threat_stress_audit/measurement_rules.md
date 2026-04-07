# Measurement Rules

Baseline:

- reuse the landed `R40` source, lowering, and accelerated free-running
  artifacts as the fixed baseline packet.

Every future candidate must record:

- source-reference exactness;
- lowered-interpreter exactness;
- accelerated free-running trace match;
- accelerated free-running final-state match;
- stack read count;
- memory read count;
- call read count.

The slice candidate must additionally record:

- one predeclared retrieval-critical slice;
- one predeclared local-easy slice;
- the same measurements above per slice.

Interpretation rule:

- helper-overencoding candidates only count if source meaning and lowered
  semantics stay fixed while the accelerated runtime story changes locally;
- easy-part-only candidates only count if the easy slice absorbs the observed
  gain while the paired retrieval-critical slice fails to show the same kind of
  relief on the same row;
- if the stress requires a new family, new opcode, or new substrate, it is not
  a valid `R41` measurement.

Allowed future verdict labels:

- `keep_h36_freeze`
- `mixed_nonunique`
- `runtime_relevance_threat_isolated`
