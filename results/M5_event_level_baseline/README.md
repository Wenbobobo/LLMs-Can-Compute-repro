# M5 Event-Level Baseline

- `training_run.json` records the final event-level standard softmax baseline.
- This branch shares the factorized event target with the richer `M4` decoder.
- Current signal: teacher-forced exact-label accuracy remains very low and
  exact free-running rollout is still zero, so this branch currently serves as
  a negative control.
