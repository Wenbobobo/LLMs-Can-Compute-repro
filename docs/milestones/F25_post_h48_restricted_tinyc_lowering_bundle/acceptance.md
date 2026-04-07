# F25 Acceptance

- the bundle remains planning-only;
- `H48` remains the current active docs-only packet;
- `H43` remains the current paper-grade endpoint;
- `R49_origin_useful_case_numeric_scaling_gate` remains the completed current
  numeric-scaling gate rather than an active lane;
- `R50_origin_restricted_tinyc_lowering_gate` is the only next runtime
  candidate fixed here;
- `H49_post_r50_tinyc_lowering_decision_packet` is the only explicit follow-up
  packet fixed here;
- the admitted surface stays limited to bounded `i32` scalars, declared static
  buffers, structured loops/branches, fixed-range table updates, and one
  top-level kernel function;
- heap, alias-heavy pointers, recursion, float, IO, hidden mutable state,
  library calls, multi-function programs, and arbitrary `C` wording remain
  excluded; and
- no new runtime lane or scope lift is authorized beyond `R50`.
