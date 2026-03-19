# Negative Results

- Direct event-value decoding currently shows a clear teacher-forced vs
  free-running gap.
- The staged pointer `M4` branch is not a fully unconstrained neural executor:
  held-out structural rollout is still `0.0`, and the intermediate
  `opcode_shape` regime improves substantially without fully closing the gap.
- On the broader `M4-D` suite, held-out `opcode_shape` collapses to `0.0`
  exact rollout while `opcode_legal` remains exact; the cleaned failure
  taxonomy splits between `push_expr_0` memory-value mismatches and
  `step_budget` nontermination, so the only stable closure is a stronger
  caveat, not a stronger fair-regime success claim.
- The provenance follow-up strengthens that caveat further: the exported
  `step_budget` rows are downstream symptoms of earlier semantic errors rather
  than an independent positive/negative regime signal.
- The event-level standard softmax baseline remains at zero exact rollout even
  after moving off flat token traces.
- The pointer-space softmax baseline also remains at zero exact-label accuracy
  and zero held-out exact rollout under the valid structural and `opcode_shape`
  regimes; exact rollout reappears only if stronger `opcode_legal` masks are
  allowed to collapse the DSL skeleton.
- Real-trace precision evidence is still narrow: the current offset suite is
  stronger than before, but it is not a broad long-horizon robustness claim.
- In the broader `M4-E` suite, the new high-address memory streams all fail at
  `1x` under float32 single-head, and the deeper exported stack stream first
  fails at `4x`; observed failure type remains `tie_collapse`.
- `E1a` keeps that boundary narrow on the same current suite: `12/25`
  tracked streams fail under float32 single-head, `7/25` already at `1x`, and
  the weaker coarse-bucket control also fails broadly, so decomposition is
  useful but not universal.
- The current `D0` slice is intentionally narrow. Exact agreement on this tiny
  typed-bytecode boundary, plus its appendix-level memory-surface companion,
  does not validate broader compiler or language claims.
- The first explicit `R2` systems gate is mixed rather than triumphant:
  geometry still shows a strong asymptotic cache-vs-bruteforce gain, but on
  the current positive `D0` suites the lowered `exec_trace` path is still
  slower per step than the best current bytecode/spec reference path, so no
  current-scope end-to-end competitiveness claim is justified yet.
- `E1b` improves attribution without changing that conclusion: the current gap
  is now broken out by program, suite, and history bridge, but no same-scope
  runtime row yet overturns the mixed gate or authorizes frontend widening.
