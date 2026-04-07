# Manuscript Stub Notes

This file holds near-prose draft stubs for the most scope-sensitive parts of
the paper bundle. They are not final paper text, but they are intended to be
close enough that later drafting can proceed by editing rather than by
re-deciding claim scope.

## Usage rules

- Keep the wording aligned with the frozen claim/evidence ledgers.
- Treat the mixed `R2` result and the `M7` no-go decision as part of the paper
  contribution, not as language to soften away.
- Do not reuse this text directly for README or blog material unless the
  publication ledgers are updated first.

## Abstract seed

We revisit a field-note claim that large language model mechanisms can behave
like computation, but we freeze the paper around a narrower reproduction target:
append-only execution traces, exact latest-write retrieval, and a small exact
executor under explicit boundaries. On the current public artifact surface, the
mechanism story remains positive at this narrower level: append-only trace
semantics and exact retrieval survive, and the preserved first tiny typed-
bytecode `D0` slice still achieves exact trace or exact final-state agreement
on the frozen starter suite inside a broader current `H43` paper endpoint. The
precision story is positive but bounded rather than open-ended:
float32 single-head fails on 12 of 25 tracked real-trace streams, with 7
failing already at `1x`, while at least one decomposition configuration
remains exact on all 25 tracked streams in the validated suite. The systems
story is mixed: cached retrieval retains a strong asymptotic advantage on the
geometry benchmark, but the current lowered `exec_trace` path remains about
`1.82x` slower than the best current reference/oracle path on the positive
`D0` suites. We therefore keep the preserved first compiled step at tiny typed
bytecode inside the broader current endpoint and still treat broader claims
about arbitrary C, general LLM computation, or current end-to-end
competitiveness as unsupported.

## Introduction opening seed

The motivating source text is valuable because it points toward a concrete
mechanistic idea: computation can be rewritten as an append-only execution
trace, and key read operations can be phrased as exact latest-write retrieval.
What it does not provide is a paper-grade boundary for which parts of that
story actually survive when every claim must be tied to auditable artifacts,
free-running exactness, and explicit negative results. The present work
therefore treats reproduction as a narrowing process rather than a branding
exercise. Its target is not “LLMs are computers” in the broad rhetorical sense,
but a smaller question: which mechanism-level and compiled-boundary claims
remain defensible after the evidence is frozen and mixed or negative results
are kept in view?

Under that narrower reading, the paper makes three contributions. First, it
keeps the append-only trace substrate and exact retrieval story intact on the
current validated scope. Second, it closes two important boundaries instead of
silently skipping them: staged-neural execution remains caveated by legality
structure, and real-trace precision remains positive only within an explicitly
narrow current-suite boundary. Third, it shows that the preserved first
compiled step at tiny typed bytecode `D0` remains exact and auditable inside
the broader current `H43` endpoint, while the systems gate is mixed and
therefore does not justify widening to a broader frontend.

## Methods seed

The methods section should be anchored in exact semantics rather than in model
performance. The core representation is an append-only execution trace whose
events expose the bounded state updates needed for later recovery: stack pops
and pushes, branch decisions, next-program-counter transitions, and latest
memory writes. Under that representation, the key read operations in the
current scope become exact causal retrieval problems rather than opaque latent
state recovery. Latest-write memory reads and stack-slot reads are phrased as
2D hard-max retrieval over keys that encode both content address and temporal
priority, and the current brute-force and specialized retrieval paths agree on
the validated examples. This section should state the mechanism cleanly and
stop there. The geometry benchmark belongs here only as evidence that exact
retrieval admits a meaningful asymptotic signal; it should not be allowed to
blur into a broader claim that the full current system is already competitive
end to end.

## Executor branches and negative controls seed

The executor results are best read as a progression from exactness by
construction toward learned or partially learned decision rules, with the
evaluation criterion fixed throughout: free-running exactness, not local label
fit alone. Exact and induced branches show that the append-only substrate can
support a small executor on the current toy scope. The harder question is what
survives once event decisions are predicted rather than derived. Here the
staged pointer decoder is the strongest learned branch, but its success remains
conditional on legality structure. On the widened staged suite, the fairer
`opcode_shape` regime collapses to `0.0` held-out exact rollout, while
`opcode_legal` remains exact only because stronger legality constraints remove
impossible combinations at decode time. The negative controls are important for
the same reason: they share the task surface and still fail. The event-level
softmax baseline remains at zero exact rollout despite nonzero teacher-forced
head accuracies, and the pointer-space softmax baseline remains at `0.0`
exact-label accuracy with structural rollout still at `0.0 / 0.0` on the
exported train/held-out slice. These failures make the staged branch's partial
success informative without turning it into a general neural-executor claim.

## Mask dependence and failure provenance seed

The staged follow-up should be written as a closure step, not as a rescue
attempt. Once the widened suite is included, the fair positive interpretation
does not survive: the held-out `opcode_shape` regime no longer supports exact
rollout, and the only exact regime is the stronger `opcode_legal` diagnostic.
The natural temptation would be to explain the remaining gap as vague learning
headroom or to introduce a softer intermediate regime. The provenance results
argue against both moves. The cleaned failure taxonomy separates direct
semantic errors from later runtime failure and shows that many `step_budget`
rows are downstream nontermination after an earlier semantic divergence. On the
`opcode_shape` slice, the root-cause head is consistently `push_expr_0`, with
the remaining failures explained by downstream consequences rather than a
separate hidden regime. This turns the staged story into a sharper negative
closure: legality structure still matters, and the paper should say so plainly.

## Precision boundary seed

The precision section should make one bounded claim and then stop. On the
current exported real and organic trace families, float32 single-head latest-
write retrieval fails early often enough that broad robustness language is no
longer defensible: 12 of 25 tracked streams fail under the single-head scheme,
and 7 of those fail already at `1x`. At the same time, the results are not
purely negative. At least one decomposition configuration remains exact on all
25 tracked streams in the validated suite, and the failures that do appear are
not arbitrary. The current observed failure mode is still `tie_collapse`, and
the families where decomposition helps most are the memory-heavy streams where
single-head addressing fails early. The correct paper claim is therefore a
narrow positive-with-boundary statement: decomposition materially helps on the
current validated suite, but nothing here supports universal base or horizon
claims across unseen trace families or a broad long-horizon robustness result.

## Systems gate section stub

The systems result is deliberately reported as a gate rather than as a victory
lap. On the positive side, the original mechanism intuition still has genuine
system-level content: on the current geometry benchmark, cached retrieval is
faster than brute-force history search at every tested history size and yields
speedups from about `42.8x` to `249.2x` as history grows. That asymptotic
signal, however, is not the same thing as present end-to-end competitiveness on
the compiled scope that the paper actually validates. When measured on the
current positive `D0` suites, the lowered `exec_trace` path still has a median
cost of roughly `6458 ns/step`, compared with about `6028 ns/step` for the
bytecode path and `3540 ns/step` for the best current reference/oracle path.
The correct conclusion is therefore mixed and operational: the specialized
retrieval mechanism is real, but on the present validated scope it does not yet
justify broader frontend widening or a general system-superiority claim.

## Compiled boundary section stub

The compiled result should be presented as an endpoint, not as a teaser. The
current paper validates a tiny typed-bytecode `D0` slice with deterministic
verification, exact-trace and exact-final-state agreement on the frozen starter
suite, one stress/reference follow-up tied to a standalone Python spec oracle,
and appendix-level memory-surface diagnostics that help audit the boundary
without widening it. This is sufficient for a first compiled boundary claim,
but not for a broader source-language claim. The subsequent `M7` decision is
therefore not an administrative footnote; it is part of the scientific
conclusion. Because the systems gate remains mixed and because the current
evidence bundle already closes the narrow compiled claim, the project stops at
tiny typed bytecode rather than widening toward Wasm-like or arbitrary-C
language coverage.

## Negative results and threats seed

The negative-results section should read as part of the argument rather than as
cleanup. Several tempting broader claims now have explicit contrary evidence or
explicitly missing support: the project does not validate general LLM
computation, arbitrary C reproduction, broader compiled demos, fair-regime
staged-pointer exactness, broad long-horizon precision robustness, or
current-scope end-to-end runtime superiority. These are not all the same kind
of limitation, and the section should keep them distinct. Some are failures of
learned execution under fair decode regimes; some are bounded precision
results; some are systems-level no-go findings; and some are deliberate scope
cuts made to avoid inflating `D0` into a broader language claim. Keeping these
rows explicit is scientifically useful because it prevents the paper from
borrowing rhetorical force from the motivating field note while quietly
dropping the parts that did not survive the evidence freeze. The threats
section should then make the matching external-validity point: the current
bundle is a narrow, auditable endpoint, not a disguised claim about general
language-model computation.
