# Downstream Route Order

Control order after `F20/H41`:

1. explicit merge/hygiene wave: `P27_post_h41_clean_promotion_and_explicit_merge_packet`
2. exact gate: `R43_origin_bounded_memory_small_vm_execution_gate`
3. coequal model gate: `R45_origin_dual_mode_model_mainline_gate`
4. later route-selection packet: `H42_post_r43_route_selection_packet`
5. conditional useful-case gate: `R44_origin_restricted_wasm_useful_case_execution_gate`

Evidence order:

1. exact `R43` remains decisive;
2. `R45` is interpreted against the exact contract rather than ahead of it;
3. `R44` still requires later explicit routing after `R43`.
