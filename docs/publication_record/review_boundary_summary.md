# Review Boundary Summary

Status: packet-level summary for reviewers, archivists, and future submission
formatting passes. The authoritative evidence still lives in the manuscript,
appendix, and claim/evidence ledgers.

## Supported claims on the current frozen scope

- deterministic computation can be encoded as an append-only execution trace;
- exact latest-write retrieval over that trace can be implemented with the
  current structured 2D hard-max mechanism;
- those primitives support one small exact executor and a tiny typed-bytecode
  `D0` compiled endpoint on the validated slice;
- the precision result is positive but bounded;
- the systems result is mixed rather than triumphant.

## Explicit non-claims

- no general “LLMs are computers” claim;
- no arbitrary C reproduction claim;
- no broader compiled demos beyond the current `D0` boundary;
- no broad long-horizon precision robustness claim beyond the validated suite;
- no current-scope end-to-end runtime-superiority claim.

## Canonical evidence anchors

- `claim_ladder.md`
- `claim_evidence_table.md`
- `manuscript_bundle_draft.md`
- `negative_results.md`
- `threats_to_validity.md`

## Reopen routing

If review requires materially new evidence, route it through exactly one named
lane in `conditional_reopen_protocol.md`:

- `E1a_precision_patch`
- `E1b_systems_patch`
- `E1c_compiled_boundary_patch`

Review questions that can be answered by wording, packet indexing, or existing
ledgers should stay downstream of the locked bundle rather than reopening it.
