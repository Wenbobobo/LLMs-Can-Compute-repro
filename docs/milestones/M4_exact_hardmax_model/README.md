# M4 Exact Hard-Max Model

Current milestone: causal executor experiments over exact hard-max latest-write
retrieval.

This branch now covers three layers:

- deterministic latest-write decode over extracted trace reads,
- a narrow trainable scorer over stack latest-write candidates,
- and a free-running online executor that uses append-only latest-write
  retrieval to reproduce reference traces.

The learned part is still narrow. It replaces stack-slot retrieval only and
does not yet generate event decisions as a token-level causal model.
