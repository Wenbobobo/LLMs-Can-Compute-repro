# Reviewer Boundary Note

Status: downstream-only reviewer-facing summary. The authoritative evidence
bundle remains the manuscript, appendix, and claim/evidence ledgers.

## What this repository claims on the current frozen scope

- Deterministic computation can be encoded as an append-only execution trace.
- Exact latest-write retrieval over that trace can be implemented with the
  current structured 2D hard-max mechanism.
- Those primitives support one small exact executor, a narrow restricted
  useful-case paper endpoint, and a preserved first tiny typed-bytecode `D0`
  compiled step on the current validated slice.
- The current precision result is positive but bounded.
- The current systems result is mixed rather than triumphant.

## What this repository does not claim

- General LLM computation.
- Arbitrary C reproduction.
- Broader compiled demos beyond the preserved first `D0` compiled step.
- Broad long-horizon robustness beyond the current validated suite.
- Current-scope end-to-end runtime superiority.

## Evidence routing

- Mechanism and boundary claims route through `claim_ladder.md`,
  `claim_evidence_table.md`, and `manuscript_bundle_draft.md`.
- Mixed and blocked rows route through `negative_results.md` and
  `threats_to_validity.md`.
- Public-facing short summaries route downstream from
  `release_summary_draft.md`, not the other way around.

## If a reviewer asks for more evidence

- Precision-boundary strengthening belongs in `E1a_precision_patch`.
- Systems-value strengthening belongs in `E1b_systems_patch`.
- Compiled-boundary strengthening belongs in `E1c_compiled_boundary_patch`.

Requests in those categories should be treated as explicit reopen candidates,
not as reasons to silently widen the current manuscript wording.
