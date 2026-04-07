# Decision Matrix

| Outcome | Meaning |
| --- | --- |
| `authorize_compiled_boundary_reentry_through_r58_first` | preserve `H52`, keep `H43` visible, set `R58` as the only next runtime candidate, keep `R59 -> H54` downstream only, and keep `F27/R53/R54` blocked |
| `keep_h52_terminal_and_stop_before_compiled_boundary` | preserve `H52` as terminal for the current repo state and keep `no_active_downstream_runtime_lane` restored |
