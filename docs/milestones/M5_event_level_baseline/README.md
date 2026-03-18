# M5 Event-Level Baseline

Goal: give the standard softmax baseline one last structural chance by moving
it from flat token traces to the shared factorized event target.

Current outcome:
- The baseline now uses the same event target as the richer `M4` branch.
- Teacher-forced exact-label accuracy remains very low.
- Exact free-running rollout is still zero on both train and held-out groups.
