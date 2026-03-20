# R13 Small-Model Executor Reactivation Design

## Goal

Keep one bounded trainable lane available if the reopened deterministic work
needs a bridge or comparator, without letting the stage collapse back into a
softmax-baseline-first project.

## When to use it

Use `R13` only if `R11/R12` leave one of two bounded gaps:

1. the deterministic executor fails on a narrow horizon or trace regime and a
   small trainable model could help localize whether the issue is structural or
   implementation-level;
2. the reopened stage needs a compact trainable reference to show that the
   mechanism is not merely a brittle one-off path.

## Expected reads

- `src/model/neural_event_executor.py`
- `src/model/trainable_latest_write.py`
- `src/exec_trace/datasets.py`
- current `M4`/`M5` residual milestone docs and negative controls

## Acceptance

- `R13` stays explicitly conditional and bounded;
- any training run remains downstream of the deterministic reopened core;
- outputs are interpreted as bridge/comparator evidence, not as a new mainline
  claim layer.
