# R3 D0 Exact Execution Stress Gate

Goal: test whether exact free-running execution on the current tiny typed
bytecode `D0` endpoint survives a bounded harder suite without widening scope.

Current state:

- completed on the same `D0` endpoint with `7/7` admitted rows still exact;
- linear versus accelerated Hull decode parity stays exact on all admitted
  lowered rows;
- only the immediate precision companion activated, with `4` longer memory
  streams entering the float32 horizon screen and `E1c` remaining inactive.

Scope:

- extend the exact suite only with longer control-flow, deeper mixed
  stack-memory, and longer indirect-memory stress rows;
- keep `linear` and `Hull` decode parity explicit;
- run precision follow-up only on boundary-bearing rows.

Non-goals:

- no frontend widening;
- no broad long-horizon robustness claim;
- no systems optimization churn.
