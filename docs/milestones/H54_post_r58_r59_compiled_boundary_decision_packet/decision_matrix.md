# Decision Matrix

| Outcome | Meaning |
| --- | --- |
| `freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value` | preserve `H52`, preserve `H43`, record exact `R58/R59` support on the admitted suite, restore `no_active_downstream_runtime_lane`, and keep `F27/R53/R54` blocked |
| `stop_before_restricted_compiled_boundary` | preserve `H52` as the correct terminal state and stop without claiming compiled-boundary support |
| `stop_due_to_compiler_work_leakage` | record that the wave leaked into broader compiler or frontend scope and stop negatively |
