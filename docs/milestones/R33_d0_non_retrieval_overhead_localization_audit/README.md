# R33 D0 Non-Retrieval Overhead Localization Audit

Executed bounded post-`H26` systems-audit lane on the fixed tiny typed-bytecode
`D0` endpoint.

`R33` consumed the deferred systems-audit lane preserved by `H26` and executed
it from the clean `wip/r33-next` worktree. The lane stayed on the current
positive `D0` suite, kept the comparator set fixed, and did not widen endpoint,
suite, or comparator scope by momentum.

The realized first-pass outcome is now machine-readable in
`results/R33_d0_non_retrieval_overhead_localization_audit/summary.json`:

- `lane_verdict = suite_stable_noncompetitive_after_localization`;
- `audit_scope = stratified_first_pass`;
- `executed_case_count = 12`;
- `exact_case_count = 12`;
- `component_accounting_match_count = 12`;
- `global_dominant_component = state_update_bookkeeping_seconds`.

`R33` therefore closes as a bounded same-endpoint attribution result:
bookkeeping dominates non-retrieval overhead across every audited suite, while
`pointer_like_exact` remains noncompetitive against the fixed same-endpoint
references. The next step is `H27`, which freezes this sharper post-`R33`
systems reading and preserves blocked future lanes explicitly.
