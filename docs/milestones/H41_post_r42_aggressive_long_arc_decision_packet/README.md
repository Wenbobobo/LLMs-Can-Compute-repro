# H41 Post-R42 Aggressive Long-Arc Decision Packet

Executed docs-only aggressive long-arc decision packet after the completed
`R42` retrieval-contract gate.

`H41` does not replace `H36` as the preserved active routing/refreeze packet.
Instead, it interprets the completed `H40 -> R42` state explicitly and chooses
exactly one of two outcomes:

- selected outcome:
  `authorize_r43_exact_mainline_and_coequal_r45_model_lane`;
- non-selected alternative:
  `hold_at_r42_and_continue_planning_only`;
- named exact next runtime candidate on the selected branch:
  `r43_origin_bounded_memory_small_vm_execution_gate`;
- named coequal model lane on the selected branch:
  `r45_origin_dual_mode_model_mainline_gate`.

The packet records that `R42` kept the semantic-boundary route alive on fixed
retrieval-contract tasks, `F20` fixed the exact-versus-model evidence boundary,
and one later explicit packet is therefore allowed to authorize exact
bounded-memory execution plus a coequal downstream model lane without
reopening `R41` or activating `R44` by momentum.
