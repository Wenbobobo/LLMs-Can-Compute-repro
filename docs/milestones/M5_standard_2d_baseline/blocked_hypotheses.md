# Blocked Hypotheses

- "Teacher-forced token accuracy near 70% on held-out eval is already a useful
  executor."
  Blocked by `training_run.json`, which shows zero exact free-running rollout
  on the current eval groups.
- "The current union-vocabulary workaround is a fair long-horizon baseline."
  Blocked because it prevents OOV crashes but does not resolve the underlying
  serialization issue.
- "Factorized numeric tokenization by itself fixes the baseline."
  Blocked because the new comparison improves vocabulary stability and delays
  first error, but exact rollout still remains zero.
