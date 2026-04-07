# 2026-03-25 Post-H58 Closeout And Reopen Criteria Analysis

## Summary

`H58` closed the current executor-value mainline after `R62` showed that even
native useful-kernel trace programs remain value-negative on the current
append-only executor path. This analysis records what the repository now
supports, what it falsifies relative to the public Percepta framing, and what
would count as a genuinely different future reopen rather than momentum.

The short version is:

- the append-only trace substrate is real;
- exact retrieval-backed execution is real on narrow admitted surfaces;
- the current bounded executor-value story is not;
- broad "LLMs become computers" framing remains unsupported here; and
- future work is justified only if the cost structure changes materially, not
  if we merely re-encode another small executor surface under the same runtime.

## Origin Interpretation

The public field note and the three stored discussions all converge on the same
scientific reading:

- the serious claim is not "general LLM computation";
- the serious claim is that computation can be rewritten as an append-only
  execution trace with a small number of retrieval-heavy state reads;
- those reads may admit low-dimensional geometric acceleration, especially for
  hard-max `2D` heads; and
- a narrow executor or coprocessor might therefore live inside a
  transformer-compatible runtime.

The stored discussion notes also impose the right discipline:

- treat arbitrary `C`, broad Wasm, million-step reliability, and practical
  systems superiority as separate claims, not one package;
- prefer falsifiable mechanism questions over flashy demos; and
- stop early when the evidence says the current route is value-negative.

That interpretation matches the landed repository much better than the public
headline.

## What Is Supported Here

The current evidence stack supports the following narrow but real claims.

1. Append-only execution traces are a valid computational substrate here.
   `R34`, `R35`, `R42`, `R43`, `R44`, and the associated closeout packets show
   that state can be reconstructed from prior writes and structured control
   history without hidden mutable state.
2. The geometric retrieval story is real as a mechanism.
   The `2D` hard-max route and later primitive/semantic-boundary audits
   established exact retrieval behavior on the admitted tasks and traces.
3. A narrow exact executor is real.
   The stack-VM, bounded-memory, restricted useful-case, tiny-`C`, mechanism,
   compiled-boundary, and useful-kernel bridge waves all showed exact free-run
   execution on their admitted rows.
4. The project has already exceeded "toy geometry only" status.
   `H43` remains a real paper-grade endpoint for bounded useful-case execution,
   and `H58` preserves that endpoint rather than overturning it.

So the mechanistic core is not empty. The project already has a meaningful
positive reproduction boundary.

## What Is Disconfirmed Here

The stronger value and systems story is now repeatedly negative.

1. Same-endpoint runtime superiority already failed earlier on `R7`, `R10`,
   `R23`, and `R28`.
2. Mechanism-first value failed on `R57`.
3. Compiled useful-kernel bounded value failed on `R61`.
4. Native useful-kernel bounded value failed on `R62`, which is the strongest
   current falsifier because compiler/lowering time was removed from the
   measured comparator.

`R62` matters more than the earlier value-negative packets because it answers
the most generous remaining version of the current question: even after
collapsing the runtime down to native `sum/count` trace programs, accelerated
execution is still slower than the simpler native linear route on the longest
row of both kernels and remains far outside the external scalar comparator's
order of magnitude.

That means the current executor-value mainline is not merely "not yet proven".
It is actively disconfirmed on the best route this branch justified.

## Distance To An Influential Reproduction Or Falsification

For positive reproduction of the broad Percepta narrative, the project is still
far away. The missing pieces are not cosmetic:

- no broad arbitrary-`C` or broad Wasm support;
- no demonstrated million-step exactness under a cleanly specified broad
  semantics boundary;
- no evidence that the current internal route is practically preferable to a
  simpler external interpreter/runtime; and
- no evidence that the constrained executor path can coexist with broad
  language-model behavior without paying a major capability cost.

For influential falsification of the broad narrative, the project is much
closer. The current evidence already supports an honest, defensible statement:

> A narrow append-only trace executor with exact retrieval-backed execution is
> real, but bounded executor value is not established and the current internal
> accelerated routes remain slower than simpler baselines even after the
> compiler/lowering contribution is removed.

That is already stronger than "we failed to reproduce the blog". It isolates
which layers survived and which layers did not.

## When A Reopen Is Legitimate

A future reopen is justified only if it introduces a genuinely different cost
structure. On current evidence, that means at least one of the following must
change materially:

1. Runtime implementation layer:
   replace the current Python-level retrieval path with a low-level compiled,
   batched, or otherwise materially different kernel where query/update cost is
   not dominated by the same object-level overheads.
2. Horizon regime:
   run in a trace-length regime where asymptotic crossover could plausibly
   dominate before numerical precision collapses, rather than reusing another
   short narrow surface.
3. Architectural contract:
   change the executor contract so that the retrieval path is amortized or
   compiled into a materially different forward process, rather than measuring
   the same per-step interpreted route on a new micro-suite.

Anything weaker should be treated as the same scientific lane in new clothes.

## What Does Not Justify A Reopen

The following do not justify reopening science:

- another docs-only packet without a new cost model;
- another narrow surface under the same runtime path;
- another trainable or transformed comparator branch while the exact route is
  still value-negative;
- broader rhetorical scope such as arbitrary `C`, broad Wasm, or "LLMs are
  computers"; and
- demo-first work whose main novelty is presentation rather than mechanism.

In particular, `F27`, `R53`, and `R54` should remain blocked by default. The
current evidence does not justify reviving transformed or trainable entry.

## Recommended Next Actions

Recommended now:

1. Treat `H58` as a real closeout, not a staging point.
2. Use the current branch for consolidation only:
   paper-facing synthesis, negative-result sharpening, and archive-quality
   closeout material.
3. If more science is desired, create a fresh planning packet that names one
   concrete low-level cost-model experiment and gives it strict stop rules.

Not recommended now:

- continuing executor-value experiments on the same runtime by momentum;
- widening semantics first; or
- switching to trainable/transformed entry to escape a landed negative result.

## Execution Rules For Any Later Work

- save the new plan before execution starts;
- branch from a clean successor worktree under `D:/zWenbo/AI/wt/...`;
- use `uv` and reuse the project virtualenv pattern;
- keep dirty root `main` out of scientific execution;
- keep large raw artifacts out of git; and
- stop immediately if the new route cannot articulate a different cost
  structure up front.

## Provenance Note

This analysis was constrained by the landed repository evidence plus read-only
consultation of the root-repository `docs/origin/` materials. Those origin
files were not copied into this clean worktree, so this document records their
scientific interpretation rather than treating them as part of the live control
surface.
