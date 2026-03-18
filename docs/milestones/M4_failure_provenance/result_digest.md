# Result Digest

- `results/M4_failure_provenance/summary.json` shows that the negative closure
  from `C2h` survives provenance analysis.
- On held-out `opcode_shape`, every failure still roots in `push_expr_0`:
  some rows fail immediately as direct memory-value mistakes, while the rest
  first make that same semantic mistake and only later manifest as
  nontermination.
- No new decode regime is justified by this export.
