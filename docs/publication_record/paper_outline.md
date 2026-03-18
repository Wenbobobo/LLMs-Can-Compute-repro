# Paper Outline

Status: manuscript skeleton for the current no-go scope after `M7` and `P4`.

## 1. Abstract

- State the narrow target: append-only execution traces, exact retrieval, and a
  small exact executor.
- Report the surviving positive evidence (`A1`, `B1`, current-scope execution
  branches), the narrowed precision boundary (`R1`), the mixed systems gate
  (`R2`), and the compiled-boundary no-go (`M7`).
- Explicitly reject broader claims about general LLM computation, arbitrary C,
  or demo-first evidence.

## 2. Introduction and Claim Ladder

- Explain why the source field note motivated the work but overstated the final
  scope.
- Present the current claim ladder as the paper's actual target, not a teaser
  for future scope.
- Clarify up front that the paper is a reproduction-plus-boundary study.

## 3. Methods: Trace Substrate and Exact Retrieval

- Define the append-only execution-trace representation and reference
  interpreter semantics.
- Describe exact latest-write retrieval and the geometry benchmark that
  establishes the asymptotic retrieval signal.
- Keep the mechanism framing separate from any broader language/runtime claims.

## 4. Executor Branches and Negative Controls

- Summarize the exact, induced, opcode-conditioned, and staged-neural branches.
- Separate teacher-forced success from free-running exactness.
- Include the direct event-value collapse and softmax baselines as genuine
  negative controls, not as side notes.

## 5. Mask Dependence and Failure Provenance

- Explain why the fair fourth staged regime did not survive the expanded suite.
- Use the provenance follow-up to show that later `step_budget` failures are
  downstream symptoms of earlier semantic mistakes.
- Keep the conclusion narrow: staged success remains caveated by stronger
  legality structure.

## 6. Precision Boundary on Real / Organic Traces

- State the `C3e` boundary in one sentence: where single-head fails, where
  decomposition helps, and what remains unsupported.
- Use the current broadened current-suite framing rather than open-ended
  long-horizon rhetoric.
- Keep figure/table roles tightly tied to the exported `R1` bundle.

## 7. Systems Gate

- Separate asymptotic retrieval value from current-scope end-to-end runtime
  value.
- Report the mixed result plainly: geometry is strongly positive, but the
  lowered path is not yet competitive on the current positive `D0` suites.
- Make this mixed result the reason the paper stops short of a broader runtime
  claim.

## 8. Compiled Boundary

- Present the tiny typed-bytecode `D0` slice as the first compiled boundary.
- Show the verifier, differential harness, memory-surface companion, and
  stress/reference companion as one constrained bundle.
- Explain why `M7` keeps this as the endpoint instead of widening toward a
  Wasm-like or arbitrary-C claim.

## 9. Threats, Unsupported Claims, and Release Discipline

- Consolidate unsupported claims from `P3`.
- Fold `negative_results.md` and `threats_to_validity.md` into one coherent
  boundary statement.
- Explain why the blog remains blocked and why README-level restraint is part of
  the scientific discipline, not just packaging.

## 10. Reproducibility Appendix

- Collect regeneration commands, artifact ledgers, and figure/table source
  paths.
- Keep memory-surface diagnostics and other companion artifacts appendix-level
  unless they directly support a main-text claim.
- Point to the public-safe packaging ledger for outward release boundaries.
