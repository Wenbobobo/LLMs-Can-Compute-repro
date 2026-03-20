# R12 Append-Only Executor Long-Horizon Design

## Goal

Push append-only/latest-write execution farther on the same fixed endpoint and
check whether free-running exact execution still holds under longer horizons
and harder trace organizations.

## Why this is the main reopened science lane

The repository's actual scientific target is narrower than the blog headline:
append-only traces, latest-write retrieval, and exact execution on the same
endpoint. `R12` is therefore the main reopened lane because it directly tests
whether that mechanism survives beyond the already completed `R6/R8` packet.

## Expected reads

- `src/exec_trace/dsl.py`
- `src/exec_trace/interpreter.py`
- `src/exec_trace/replay.py`
- `src/exec_trace/memory.py`
- `src/model/free_running_executor.py`
- `src/model/exact_hardmax.py`
- `results/R3_d0_exact_execution_stress_gate/summary.json`
- `results/R4_mechanistic_retrieval_closure/summary.json`

## Acceptance

- one bounded longer-horizon append-only executor artifact exists;
- exact-trace and exact-final-state agreement remain explicit where they hold;
- failures, if any, are localized to retrieval, horizon, or trace-organization
  causes rather than left as generic “did not scale.”
