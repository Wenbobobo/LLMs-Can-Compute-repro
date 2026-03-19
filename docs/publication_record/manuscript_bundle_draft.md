# Manuscript Bundle Draft

## 1. Abstract

We revisit a field-note claim that large language model mechanisms can behave
like computation, but we freeze the paper around a narrower reproduction target:
append-only execution traces, exact latest-write retrieval, and a small exact
executor under explicit boundaries. On the current evidence bundle, the
mechanism story remains positive at this narrower level: append-only trace
semantics and exact retrieval survive, and a tiny typed-bytecode `D0` slice
achieves exact trace or exact final-state agreement on the frozen starter
suite. The precision story is positive but bounded rather than open-ended.
Float32 single-head fails on 12 of 25 tracked real-trace streams, with 7
failing already at `1x`, while at least one decomposition configuration
remains exact on all 25 tracked streams in the validated suite. The systems
story is mixed. Cached retrieval retains a strong asymptotic advantage on the
geometry benchmark, but the current lowered `exec_trace` path remains about
`1.82x` slower than the best current reference/oracle path on the positive
`D0` suites. We therefore keep the compiled endpoint at tiny typed bytecode
and treat broader claims about arbitrary C, general LLM computation, or
current end-to-end competitiveness as unsupported. Stopping at `D0` is
therefore part of the current scientific conclusion, not an implementation gap
waiting to be filled.

## 2. Introduction and Claim Ladder

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
narrow current-suite boundary. Third, it shows that the first compiled endpoint
remains at tiny typed bytecode `D0`: the current slice is exact and
auditable, but the systems gate is mixed and therefore does not justify
widening to a broader frontend.

The introduction closes by pointing readers to two paired main-text artifacts.
A claim-ladder figure plus evidence matrix orients the narrowed mechanism story
that survives the freeze, while a separate supported-versus-unsupported claims
table keeps the excluded broader readings explicit and auditable. Those
unsupported rows are part of the result rather than placeholders for future
rhetorical widening.

## 3. Methods: Trace Substrate and Exact Retrieval

The methods section is anchored in exact semantics rather than model
performance.

### 3.1 Trace substrate semantics

The core representation is an append-only execution trace whose events expose
the bounded state updates needed for later recovery: stack pops and pushes,
branch decisions, next-program-counter transitions, and latest memory writes.
Under that representation, the relevant executor state is no longer treated as
opaque latent memory. It is exposed as a causal history that can be audited
event by event against exact execution semantics.

### 3.2 Exact retrieval and geometry signal

Once the trace is written in that form, the key read operations in the current
scope become exact causal retrieval problems rather than latent-state
reconstruction. Latest-write memory reads and stack-slot reads are phrased as
2D hard-max retrieval over keys that encode both content address and temporal
priority, and the current brute-force and specialized retrieval paths agree on
the validated examples. The geometry benchmark belongs here only as evidence
that exact retrieval admits a meaningful asymptotic signal. In this draft, that
signal stays explicitly separate from any broader claim that the full current
system is already competitive end to end. In the current paper layout, this
section stays prose-first: the claim-bearing figure/table pairs appear later
where they support boundary claims rather than method-only exposition.

## 4. Executor Branches and Negative Controls

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
impossible combinations at decode time. The negative controls matter for the
same reason: they share the task surface and still fail. The event-level
softmax baseline remains at zero exact rollout despite nonzero teacher-forced
head accuracies. The pointer-space softmax baseline remains at `0.0`
exact-label accuracy, with structural rollout still at `0.0 / 0.0` on the
exported train/held-out slice. These failures make the staged branch's partial
success informative without turning it into a general neural-executor claim.

This section is therefore organized around one regime-comparison figure and one
negative-control comparison. The first shows that exact rollout survives only
under stronger legality structure, and the second shows that nearby softmax
baselines still fail under the same free-running criterion. Read together, they
support a bounded structural claim rather than a general learned-executor
result.

## 5. Mask Dependence and Failure Provenance

The staged follow-up is a closure step rather than a rescue attempt. Once the
widened suite is included, the fair positive interpretation does not survive:
the held-out `opcode_shape` regime no longer supports exact rollout, and the
only exact regime is the stronger `opcode_legal` diagnostic. The provenance
results then narrow the explanation further. The cleaned failure taxonomy
separates direct semantic errors from later runtime failure and shows that many
`step_budget` rows are downstream nontermination after an earlier semantic
divergence. On the `opcode_shape` slice, the root-cause head is consistently
`push_expr_0`, with the remaining failures explained by downstream
consequences rather than a separate hidden regime. The staged story therefore
ends as a sharper negative closure: legality structure still matters, and the
paper says so directly.

A provenance-backed staged failure taxonomy figure carries this section's main
evidence, separating root semantic mistakes from later runtime fallout rather
than implying a hidden positive regime.

## 6. Precision Boundary on Real / Organic Traces

The precision section makes one bounded claim and then stops. On the current
exported real and organic trace families, float32 single-head latest-write
retrieval fails early often enough that broad robustness language is no longer
defensible: 12 of 25 tracked streams fail under the single-head scheme,
and 7 of those fail already at `1x`. At the same time, the results are not
purely negative. At least one decomposition configuration remains exact on all
25 tracked streams in the validated suite, and the failures that do appear are
not arbitrary. The current observed failure mode is still `tie_collapse`, and
the families where decomposition helps most are the memory-heavy streams where
single-head addressing fails early. The correct paper claim is therefore a
narrow positive result with a clear boundary: decomposition materially helps on
the current validated suite, but nothing here supports universal base or
horizon claims across unseen trace families or a broad long-horizon robustness
result.

The main-text support here stays compact: one real-trace boundary figure shows
where failures first appear across schemes, and one boundary table makes the
current `12/25`, `7/25`, and `25/25` claims auditable without opening new
generalization rhetoric.

## 7. Systems Gate

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

In the current layout, this result remains a quantified main-text paragraph
rather than a standalone table. The main text needs the mixed gate decision and
its key timing anchors, while the full baseline matrix and runtime rows stay in
companion artifacts unless a later layout pass specifically promotes a compact
gate table.

## 8. Compiled Boundary

The compiled result is presented as an endpoint, not as a teaser. The current
paper validates a tiny typed-bytecode `D0` slice with deterministic
verification, exact-trace and exact-final-state agreement on the frozen starter
suite, one stress/reference follow-up tied to a standalone Python spec oracle,
and appendix-level memory-surface diagnostics that help audit the boundary
without widening it. This is sufficient for a first compiled boundary claim,
but not for a broader source-language claim. The later no-widening decision is
therefore not an administrative footnote; it is part of the scientific
conclusion. Because the systems gate remains mixed and because the current
evidence bundle already closes the narrow compiled claim, the project stops at
tiny typed bytecode rather than widening toward Wasm-like or arbitrary-C
language coverage.

The main text supports this endpoint with two artifacts: a frontend boundary
diagram that makes the frozen `D0` slice explicit, and an exact-trace/final-state
success table that records what the current starter suite does and does not
validate. Companion appendix material stays clearly downstream of that
endpoint: memory-surface diagnostics and stress/reference rows help audit the
boundary, but they do not widen it.

## 9. Negative Results and Threats

The negative-results section reads as part of the argument rather than as
cleanup. Several tempting broader claims now have explicit contrary evidence or
explicitly missing support: the project does not validate general LLM
computation, arbitrary C reproduction, broader compiled demos, fair-regime
staged-pointer exactness, broad long-horizon precision robustness, or
current-scope end-to-end runtime superiority. These are not all the same kind
of limitation, and the section keeps them distinct. Some are failures of
learned execution under fair decode regimes; some are bounded precision
results; some are systems-level no-go findings; and some are deliberate scope
cuts made to avoid inflating `D0` into a broader language claim. Keeping these
rows explicit is scientifically useful because it prevents the paper from
borrowing rhetorical force from the motivating field note while quietly
dropping the parts that did not survive the evidence freeze. The threats
section then makes the matching external-validity point: the current bundle is
a narrow, auditable endpoint, not a disguised claim about general
language-model computation.

A compact threats-to-validity table makes those boundary rows explicit,
keeping failures of learned execution, finite-precision limits, systems no-go
results, and deliberate scope cuts visible as distinct reasons rather than as a
single undifferentiated limitation paragraph.

## 10. Reproducibility Appendix

The appendix makes the current paper bundle auditable and regenerable without
inflating companion diagnostics into new main-text claims. The guiding rule is
simple: main text carries the distilled claim-bearing evidence, while the
appendix carries regeneration commands, artifact maps, and companion views that
strengthen auditability on the same frozen scope. The current appendix
therefore has three jobs. First, it points readers to the canonical paper-ready
bundle under `results/P1_paper_readiness/`, which contains rendered figures,
table sources, and machine-readable bundle summaries. Second, it records how to
regenerate the public-safe result bundles that matter for the compiled
boundary, paper assembly, and release gate. Third, it keeps companion
diagnostics such as memory-surface views, per-stream precision catalogs, and
full staged failure digests visible and inspectable without letting them mutate
into broader claims. Release-hygiene and packaging ledgers belong here for the
same reason: they make the research engineering process reproducible and
inspectable, but they remain downstream of the scientific argument itself. The
current appendix layout therefore stays anchored in three companion bundles:
the `P1` paper-ready artifact set, the compiled-boundary companion
diagnostics, and the release/readiness ledgers that keep the package
regenerable.
