# F21 Model Bridge Scoreboard

| wave | modes | role | exact dependency | held-out rule |
| --- | --- | --- | --- | --- |
| `R48_origin_dual_mode_useful_case_model_gate` | `compiled_weight_executor`, `trainable_2d_executor` | comparator-only until exact frontend survives | exact `R47` positive required before activation | held-out useful-case family must remain explicit; model-only positives do not replace exact evidence |
| `H47_post_r48_useful_case_bridge_refreeze` | same two admitted modes | interpret comparator results without raising claim ceiling | preserved `R46/R47` exact scoreboard remains decisive | stop if compiled mode fails or if any model result outruns the exact contract |
