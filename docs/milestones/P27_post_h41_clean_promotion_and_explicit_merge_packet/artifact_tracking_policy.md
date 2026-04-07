# P27 Artifact Tracking Policy

`P27` keeps large derived artifacts and oversized probes outside accidental
promotion.

The standing example is
`results/R20_d0_runtime_mechanism_ablation_matrix/probe_read_rows.json`. That
raw probe file is not present on the current clean source branch and should
stay outside the `P27` merge set. If a similar oversized probe reappears, do
not smuggle it into `main` through the explicit merge wave. Replace it with a
compact summary or handle it through a separate explicit artifact policy.

Packet-bearing artifacts that do belong in this review set are the compact
control/result outputs for the current clean stack, including:

- `results/P27_post_h41_clean_promotion_and_explicit_merge_packet/`
- `results/H41_post_r42_aggressive_long_arc_decision_packet/`
- `results/F20_post_r42_dual_mode_model_mainline_bundle/`
- `results/R42_origin_append_only_memory_retrieval_contract_gate/`

No `.gitignore` change is authorized inside `P27` alone. If the repository
needs a new ignore rule or alternate large-artifact storage policy, record that
in a separate explicit hygiene packet rather than hiding it inside the merge
wave.
