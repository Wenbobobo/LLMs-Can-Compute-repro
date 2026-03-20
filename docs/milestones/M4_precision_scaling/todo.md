# TODO

Legacy note: the remaining unchecked rows are tracked in
`docs/milestones/H1_legacy_backlog_reconciliation/classification_matrix.md`
and are not active on the current frozen paper scope by default.

- [x] Add scheme-aware precision sweeps
- [x] Compare single-head vs decomposition under float32 latest-write
- Follow-up moved to `R3_d0_exact_execution_stress_gate`: rerun the same
  schemes only on new real mixed-trace reads that become boundary-bearing under
  the active `D0` stress suite.
- Follow-up moved to `R3_d0_exact_execution_stress_gate`: test larger horizons
  and alternative bases only where they sharpen a current boundary rather than
  reopening an open-ended sweep.
- Dormant follow-up: decide whether a richer decomposition is needed only if
  the bounded `R3` suite shows the current schemes are insufficient.
