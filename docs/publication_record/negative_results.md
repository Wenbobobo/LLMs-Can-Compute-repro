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
- `R4` closes the current mechanism question only on the same bounded `D0`
  scope: it does not justify `R5`, does not change the mixed systems result,
  and keeps staged-pointer / provenance artifacts diagnostic-only rather than
  claim-bearing evidence.
- `R7` keeps the same-endpoint runtime bridge negative on current evidence:
  across the preserved `8`-family exact-admitted long-horizon surface, the
  bounded runtime bridge only profiles the top `4` heaviest representatives;
  on those profiled rows accelerated Hull decode is only about `0.973x` of
  linear on median and still about `1980.3x` slower per step than the lowered
  path, so no decode-level bridge closure or `R5` reopen is justified.
- `R9` sharpens that precision caveat on admitted `R8` memory streams without
  overturning it: one admitted stream still shows an immediate
  `single_head` `tie_collapse` at `1x`, recovered only by the default
  decomposition grid, so the follow-up remains companion-only and does not
  justify broader unseen-family or stack-wide robustness.
- `R10` makes the negative same-endpoint systems result more explicit rather
  than less: on representative admitted `R6/R8` rows, exact runtime remains
  about `99.8%` retrieval time with a median exact-versus-lowered ratio around
  `2429.1x`, so current same-endpoint execution still does not support a
  practical runtime-bridge claim or an `R5` reopen.
- `R11` keeps the geometry fast path positive only as a mechanistic primitive:
  the current bounded parity slice stays exact and the standalone cache
  benchmark stays strong, but this still does not support same-endpoint
  executor speedup wording.
- `R12` keeps the current append-only executor story bounded: exact current
  executor exports and bounded `trainable_stack` success do not justify
  unseen-family generalization, a broad neural-executor claim, or activation
  of `R13`.
- `R20` strengthens the mechanism story by failure contrast, not by a broader
  systems closure: the shuffled pointer-like and address-oblivious controls
  both fail on the fixed probe set, but that does not change the same-endpoint
  systems verdict by itself.
- `R21` remains a no-break-observed result rather than a localized executor
  boundary: the bounded `48`-branch grid staying exact does not mean the true
  failure boundary has been found.
- `R22` sharpens that caveat further: the harder `102`-candidate follow-up also
  stays exact, so the true executor boundary is still not localized on current
  evidence.
- `R26` and `R27` extend that caveat into the post-`H21` reopen packet: the
  bounded `22`-candidate first wave and the bounded `12`-candidate extension
  also stay exact, so the true executor boundary remains unresolved even after
  the later reopen wave.
- `R23` is a first-class mixed systems result, not a near-win: pointer-like
  exact stays exact on `25/25` full-suite rows and is far faster than imported
  accelerated, but it remains about `4.16x` slower than the best current
  reference path and still slower than the lowered path on the bounded systems
  criterion.
- `R28` strengthens the mechanism story without overturning that mixed result:
  the contract is supported with partial control isolation, but the bottleneck
  remains non-retrieval dominated and the audit does not convert mechanism
  support into a systems win.
- `H23` therefore keeps frontier review planning-only, and `H25` preserves
  that restraint while ordering the next bounded same-endpoint work through
  `R32` first and deferred `R33` second: the systems story is still not
  materially positive enough for broader systems, frontend, or demo claims,
  and the executor boundary is still not localized.
- `H27` later closes that old same-endpoint recovery line more sharply
  negative: `R32` still does not localize a true boundary, `R33` still does
  not turn the systems story positive, and the old `R29/F3` route remains
  blocked rather than implicitly revived.
- `R36` sharpens the current precision caveat on the active Origin-core bundle:
  selected inflated-horizon float32 `single_head` rows fail by
  `tie_collapse`, bounded decomposition schemes recover those exported rows,
  and that recovery still does not authorize compiled/demo scope lift by
  momentum.
- `R37` remains a narrow existence proof, not a broad compiler result: one tiny
  admitted bytecode subset lowers and executes exactly on the active
  Origin-core substrate, but that does not reopen arbitrary `C`, broader
  language support, or same-endpoint systems claims.
- `R62` extends that value-negative boundary onto native useful-kernel rows:
  even after removing compiler/lowering time from the measured executor
  comparator and running native `sum/count` trace programs directly, the
  accelerated route stays exact on `4/4` rows but remains slower than native
  linear on the longest row of both kernels and stays far outside the external
  scalar comparator's order of magnitude, so `H58` closes the mainline as
  mechanism-supported but value-negative.
- `R39` is narrow same-substrate follow-up evidence, not a broader compiler
  opening: one declared helper-body permutation with target renumbering
  survives on the admitted row and named same-family boundary probe, but that
  does not justify arbitrary control-surface freedom or broader compiler
  support.
- `H34` therefore keeps the compiled-boundary line complete-for-now rather
  than reopening a new same-substrate runtime lane by momentum.
