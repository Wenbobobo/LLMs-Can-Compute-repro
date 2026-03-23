# H35 Todo

- keep the two-outcome fork explicit:
  `authorize_one_bounded_scalar_family_runtime_gate` versus
  `keep_no_runtime_lane_under_h34_for_now`;
- keep `R40_origin_bounded_scalar_locals_and_flags_gate` as the only named
  runtime lane authorized here;
- keep the runtime scope explicit: frame-only bounded locals and typed flags on
  the current opcode surface;
- keep `R41_origin_runtime_relevance_threat_stress_audit` deferred until a
  later explicit post-`H36` packet;
- preserve `R29`, `F3`, broader compiler rhetoric, restricted-Wasm wording,
  and hybrid/planner bridge claims as blocked by default.
