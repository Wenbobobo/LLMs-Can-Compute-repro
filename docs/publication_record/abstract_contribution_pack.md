# Abstract and Contribution Pack

Status: downstream-only derivative material. The authoritative paper-facing
source remains `manuscript_bundle_draft.md`.

## Venue-agnostic abstract

This repository revisits a field-note claim that transformer-like mechanisms
can support computation, but freezes the result at a narrower and auditable
endpoint. On the current validated scope, deterministic computation can be
encoded as an append-only execution trace, exact latest-write retrieval can be
implemented with structured 2D hard-max retrieval, and those primitives support
one small exact executor plus a tiny typed-bytecode `D0` compiled boundary. The
positive result is therefore mechanistic rather than sweeping. The precision
story is bounded rather than broad: float32 single-head fails on `12/25`
tracked real/organic trace streams, with `7/25` failing already at `1x`, while
at least one decomposition remains exact on all `25/25` tracked streams in the
validated suite. The systems story is mixed rather than triumphant: the current
geometry benchmark retains a strong asymptotic retrieval advantage, but the
lowered `exec_trace` path remains about `1.82x` slower than the best current
reference/oracle path on positive `D0` suites. We therefore stop at the current
tiny typed-bytecode boundary and keep arbitrary C, broad “LLMs are computers”
framing, frontend widening, and current-scope end-to-end systems-superiority
claims explicitly unsupported.

## Short abstract

We reproduce a narrow execution-substrate claim rather than a broad “LLMs are
computers” thesis. On the current scope, append-only traces, exact 2D
latest-write retrieval, and a tiny typed-bytecode `D0` executor remain
supported, while precision stays bounded, the systems gate stays mixed, and
broader compiled or general-computation claims remain blocked.

## Contribution summary

1. Freeze the public field-note narrative into a paper-grade claim boundary:
   append-only traces, exact retrieval, bounded precision, and `D0` as the
   current compiled endpoint.
2. Preserve the strongest positive mechanism result while keeping negative and
   mixed outcomes explicit rather than downstreaming them into future work.
3. Separate mechanism value from system value: exact retrieval remains
   technically meaningful even though the current lowered path is not yet
   current-scope runtime-competitive.
4. Turn the reproduction effort into an auditable bundle with explicit
   manuscript, appendix, claim/evidence, threat, and negative-result ledgers.

## Non-contribution reminders

- This pack does not authorize broader compiled demos.
- This pack does not upgrade the current `D0` boundary into arbitrary C.
- This pack does not relax the current blocked-blog rule.
- Any stronger precision, systems, or compiled-boundary claim still requires a
  named `E1` patch lane.
