# H51 Decision Matrix

| Outcome | Meaning | Downstream effect |
| --- | --- | --- |
| `authorize_origin_mechanism_reentry_through_r55_first` | preserve negative `H50` on the broader route but explicitly test the narrower mechanism chain | set `R55` as the only next runtime candidate and keep `R56/R57/H52` sequenced conditionally |
| `keep_h50_stop_state_as_terminal` | treat negative `H50` as a complete stop for all later work | restore `no_active_downstream_runtime_lane` and stop the branch |
| `reactivate_f27_trainable_or_transformed_entry` | reopen transformed or trainable planning after negative `H50` | reactivate `F27`; this outcome is non-selected here |
