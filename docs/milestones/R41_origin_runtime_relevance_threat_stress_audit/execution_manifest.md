# Execution Manifest

Future execution order, if a later explicit packet authorizes this lane:

1. lock the baseline to the landed `R40` artifacts;
2. run only the three predeclared candidate ids in
   `candidate_matrix.md`;
3. apply them only to the two fixed `R40` positive rows;
4. emit one local verdict and hand that verdict to a later explicit refreeze
   packet.

Maximum future audit shape:

- `3` candidate ids;
- `2` rows;
- at most `6` candidate-row evaluations before early stop;
- one optional slice packet per row for the easy-part threat.

Required future inputs:

- `results/R40_origin_bounded_scalar_locals_and_flags_gate/summary.json`
- `results/R40_origin_bounded_scalar_locals_and_flags_gate/execution_rows.json`
- `docs/milestones/F13_post_f12_bounded_scalar_value_family_spec/comparator_matrix.md`
- `docs/milestones/F14_post_f13_conditional_reopen_readiness_bundle/threat_model.md`
- `docs/milestones/F14_post_f13_conditional_reopen_readiness_bundle/candidate_perturbation_catalog.md`

Required future outputs:

- one `summary.json`
- one `candidate_rows.json`
- one `threat_measurements.json`
- one `slice_measurements.json` only if slice candidates run
- one `verdict_packet.json`
