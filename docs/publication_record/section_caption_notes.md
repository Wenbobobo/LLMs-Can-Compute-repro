# Section and Caption Notes

This file turns the current manuscript section map plus fixed figure/table roles
into caption-ready drafting notes. It is meant to keep later prose inside the
frozen current-scope claim set rather than reopen scope by phrasing drift.

## Global drafting rules

- Each main-text section should open with the narrow claim or boundary it
  actually supports on current evidence.
- Mixed results must use explicit stop/go language such as `not yet`,
  `current-scope only`, or `unsupported beyond the validated suite`.
- `R2` should be written as a gate on widening, not as a teaser for future
  runtime wins.
- `D0` should be written as the current compiled endpoint, not as an early
  placeholder for arbitrary language or runtime claims.
- Appendix companions may strengthen auditability or reproducibility, but they
  must not silently become main-text evidence for a broader claim row.

## Section-level notes

| Section | Opening note | Required evidence beats | Boundary clause | Main item |
| --- | --- | --- | --- | --- |
| Abstract | Open by stating that the project reproduces a narrower, paper-grade endpoint: append-only execution traces plus exact retrieval plus a small exact executor. | Mention the surviving mechanism positives, the narrowed precision boundary, the mixed systems gate, and the no-widening `M7` decision. | Explicitly reject arbitrary C, general LLM computation, and broader systems-superiority framing. | no standalone figure required |
| Introduction and claim ladder | Explain that the source note motivated the work but did not determine the final claim scope. | Establish the paper as a reproduction-plus-boundary study and foreground supported versus unsupported rows. | State that unsupported claims are outputs, not deferred engineering backlog. | claim ladder + supported/unsupported claims table |
| Methods: trace substrate and retrieval | Define append-only traces, exact latest-write retrieval, and the reference execution setting without promising a broader language model thesis. | Tie the mechanism story to `A1` and `B1`, then point forward to executor branches and compiled boundary as downstream tests. | Keep the methods section separate from any suggestion that exact retrieval already yields a finished system story. | likely text-only or compact geometry reference |
| Executor branches and negative controls | Introduce the branch comparison as a test of what survives under free-running exactness, not as a model leaderboard. | Distinguish exact/reference branches from staged and softmax controls; state that negative controls remain informative because they share the task surface. | Do not imply that one negative baseline exhausts all alternative learned executors. | staged regime comparison + negative-control figure |
| Mask dependence and failure provenance | State that the widened staged suite closes the fair positive claim rather than rescuing it. | Use the regime comparison plus provenance follow-up to show that later `step_budget` rows are downstream of earlier semantic divergence. | Do not describe `opcode_shape` or `step_budget` as partially surviving fair regimes. | staged failure taxonomy figure |
| Precision boundary | State the `C3e` boundary in one sentence: single-head fails early on many current streams, decomposition helps on the validated suite, broader robustness remains unsupported. | Quote the current stream/family-level closure from `R1` and keep the table/figure tied to exported summaries. | Avoid open-ended horizon rhetoric or universal scaling language. | precision boundary figure + precision boundary table |
| Systems gate | Present `R2` as the reason widening stops, not as a minor caveat. | Report both sides: geometry remains strongly positive, but current lowered `exec_trace` timing is not yet end-to-end competitive on the positive `D0` suites. | Use `not yet competitive` rather than softening the negative systems result into optimism. | likely paragraph plus optional compact inline table |
| Compiled boundary | Open by stating that the current compiled claim ends at tiny typed bytecode `D0`. | Combine verifier parity, exact trace/final-state agreement, one stress/reference follow-up, and the explicit `M7` no-go decision. | State that these results do not authorize widening to Wasm-like or arbitrary-C claims. | frontend boundary diagram + exact-trace/final-state table |
| Negative results and threats | Frame unsupported claims, failed baselines, staged closure, narrow precision, and mixed systems value as one coherent boundary statement. | Use `negative_results.md`, `threats_to_validity.md`, and `P3` unsupported rows together. | Avoid treating negative results as temporary engineering gaps unless the ledgers already say so. | threats-to-validity table |
| Reproducibility appendix | Describe how to regenerate figures/tables, audit the public-safe bundle, and inspect companion diagnostics. | Point to manifest, paper-ready rendered artifacts, release ledger, and appendix-only diagnostics. | Keep packaging and regeneration details downstream of the scientific argument. | appendix artifact map |

## Caption-ready main-text items

| Item | Caption seed | Required boundary sentence |
| --- | --- | --- |
| Claim ladder + evidence matrix | Supported and unsupported claim rows after tightening the source field note into a paper-grade reproduction boundary. | Unsupported rows include arbitrary C, general LLM computation, and any broader systems-superiority claim. |
| Supported vs unsupported claims table | Supported and unsupported claims treated as first-class outputs of the reproduction rather than omitted failures. | Unsupported areas are not merely deferred implementation work. |
| Staged decode regime comparison | Teacher-forced staged decoding remains exact under stronger legality structure, but fairer structural and `opcode_shape` regimes do not support a free-running positive claim. | `opcode_legal` remains diagnostic and should not be read as the fair endpoint. |
| Provenance-backed staged failure taxonomy | Later `step_budget` failures in the widened staged suite are downstream symptoms of earlier semantic divergence rather than an independent success/failure regime. | The provenance split sharpens the negative closure instead of reopening the staged claim. |
| Real-trace precision boundary figure | On the current exported real-trace families, float32 single-head fails early while decomposition retains exactness on the validated suite. | The figure does not establish universal long-horizon precision robustness beyond the validated suite. |
| Real-trace precision boundary table | Family- and scheme-level boundary rows behind the current precision claim. | Boundary statements remain suite-specific and scheme-specific. |
| Negative-control comparison | Softmax baselines share the task surface yet still fail the exact rollout target that defines the paper's executor boundary. | These failures are informative controls, not a proof that no other learned branch could exist. |
| Frontend boundary diagram | The current compiled endpoint is a tiny typed-bytecode `D0` slice with exact parity on the frozen starter suite. | The diagram does not imply Wasm-like, arbitrary-C, or broader runtime coverage. |
| Exact-trace / final-state success table | Exact agreement summary for the frozen `D0` slice and its current stress/reference companion. | Companion success strengthens the present endpoint but does not authorize frontend widening. |
| Threats-to-validity table | External and internal limits that keep mechanism, systems, and compiled-boundary claims distinct. | Mixed systems results remain part of the argument and cannot be omitted. |

## Items intentionally kept inline or appendix-only

| Item | Current placement | Reason |
| --- | --- | --- |
| `R2` baseline matrix and runtime profile rows | inline paragraph or appendix | The key main-text fact is the mixed gate decision; full timing detail is supporting evidence unless layout later needs a compact table. |
| Memory-surface diagnostics for `D0` | appendix | They strengthen compiled-boundary auditability without defining a broader compiler/runtime claim. |
| Per-stream precision catalogs | appendix | They support auditability and reviewer follow-up; the main text should carry only the distilled family/scheme boundary. |
| Full staged failure digests | appendix | The main text needs the distilled taxonomy and provenance claim, not every raw row. |
| Release-hygiene and public-safe packaging ledgers | appendix | They are required for outward discipline and reproducibility, but they are not claim-bearing main-text evidence. |
