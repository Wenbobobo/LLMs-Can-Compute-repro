# Post-H38 H40/R42 Activation Design

## Objective

Land one later explicit packet that activates the preserved semantic-boundary
route after `H38`, then execute exactly the first saved gate in that family:

1. `H40_post_h38_semantic_boundary_activation_packet`
2. `R42_origin_append_only_memory_retrieval_contract_gate`

Do not widen to bounded-memory VM execution, restricted Wasm usefulness, or a
same-substrate `R41` reopen in the same wave.

## Route Selection

`F18` already fixes `F9` as the preferred forward family after `H38`, and
`F19` already fixes `R42 -> R43 -> R44` as the saved semantic-boundary gate
ladder. The missing control step is therefore one explicit packet that:

- preserves `H38` as the prior docs-only keep-freeze decision;
- preserves `H36` as the underlying routing/refreeze packet;
- selects `authorize_r42_origin_append_only_memory_retrieval_contract_gate`;
- keeps `R41`, `R43`, and `R44` deferred.

The packet stays docs-only. It does not itself prove a gate result.

## R42 Scope

`R42` remains a retrieval-contract gate, not a VM gate. The fixed task
families are:

- `latest_write_same_address_short`
- `latest_write_same_address_long`
- `stack_slot_depth_short`
- `stack_slot_depth_long`
- `address_reuse_duplicate_and_tie_cases`
- `precision_range_sweep`

Each task must compare brute-force exact retrieval against the accelerated
`HullKVCache` path on the same append-only history. The audit must check both:

- retrieved value exactness;
- maximizer-row identity exactness.

The gate stops at the first mismatch or any need for hidden mutable state.

## Outputs

Land the following artifacts:

- `docs/milestones/H40_post_h38_semantic_boundary_activation_packet/`
- `scripts/export_h40_post_h38_semantic_boundary_activation_packet.py`
- `tests/test_export_h40_post_h38_semantic_boundary_activation_packet.py`
- `results/H40_post_h38_semantic_boundary_activation_packet/summary.json`
- `scripts/export_r42_origin_append_only_memory_retrieval_contract_gate.py`
- `tests/test_export_r42_origin_append_only_memory_retrieval_contract_gate.py`
- `results/R42_origin_append_only_memory_retrieval_contract_gate/`

Refresh the shared control surfaces after the artifacts land:

- `README.md`
- `STATUS.md`
- `docs/publication_record/current_stage_driver.md`
- `docs/milestones/README.md`
- `docs/plans/README.md`
- `docs/claims_matrix.md`
- `tmp/active_wave_plan.md`
- `docs/publication_record/experiment_manifest.md`

## Post-R42 State

If `R42` is positive, do not authorize `R43` by momentum. The next step stays:

later explicit post-`R42` packet -> conditional `R43`

If `R42` breaks exactness on the fixed contract tasks, stop the semantic-
boundary route and record the break directly.
