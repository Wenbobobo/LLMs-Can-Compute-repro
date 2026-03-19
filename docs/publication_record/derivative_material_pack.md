# Derivative Material Pack

Status: downstream-only preparation material for future paper, README, and
still-blocked blog maintenance. The manuscript bundle remains authoritative.

## What survived reproduction

- Append-only execution traces remain a valid substrate on the current frozen
  toy-to-compiled scope.
- Exact latest-write retrieval over that trace remains supported with the
  structured 2D hard-max mechanism.
- The current executor story survives at a narrow endpoint: one small exact
  executor plus a tiny typed-bytecode `D0` compiled boundary.
- The paper bundle is locked tightly enough that claim/evidence ownership,
  appendix boundaries, and public-surface sync can be audited mechanically.

## What remained blocked

- General “LLMs are computers” framing remains unsupported.
- Arbitrary C reproduction remains unsupported.
- Broader compiled demos and frontend widening remain blocked by the current
  `M7` no-widening boundary.
- Broad long-horizon precision robustness remains unsupported beyond the
  current validated suite.
- Current-scope end-to-end systems superiority remains unsupported because the
  systems gate is mixed.

## Figure and table shortlist for future derivatives

- Claim ladder + supported/unsupported claims pair for the top-level boundary.
- Real-trace precision boundary figure/table pair for the bounded precision
  story.
- Frontend boundary diagram + exact-trace/final-state table for the current
  compiled endpoint.
- Threats-to-validity table for the explicit blocked or mixed rows.

## FAQ-style notes

### Why stop at `D0`?

Because the current compiled evidence is exact only on the tiny typed-bytecode
boundary and the systems gate is still mixed. Stopping here is part of the
current conclusion, not an omitted implementation step.

### Why keep the blog blocked?

Because a broader derivative narrative can outrun the locked manuscript bundle
much more easily than the restrained public surface. The blog remains
downstream-only until the explicit release rules are satisfied in full.

### Why keep negative results so prominent?

Because the reproduction is valuable precisely to the extent that it narrows
the surviving mechanism and blocks unsupported extrapolation.
