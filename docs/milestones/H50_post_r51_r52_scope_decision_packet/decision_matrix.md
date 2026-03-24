# H50 Decision Matrix

| Outcome | Meaning | Downstream effect |
| --- | --- | --- |
| `freeze_as_narrow_specialized_executor_only` | the substrate remains exact only in a narrow specialized sense | restore `no_active_downstream_runtime_lane` and stop broadening |
| `allow_planning_only_f27_entry_bundle` | both sufficiency and bounded value are positive enough to justify one later planning bundle only | save `F27` only; do not authorize direct runtime execution |
| `stop_as_exact_without_system_value` | exactness may survive but the internal route does not retain bounded system value | restore `no_active_downstream_runtime_lane` and stop broader investment |
