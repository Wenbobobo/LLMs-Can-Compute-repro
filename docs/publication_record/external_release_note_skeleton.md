# External Release Note Skeleton

Status: downstream-only skeleton. This file is not itself approval for a new
release wave, blog post, or broader public narrative.

## One-paragraph skeleton

This repository reproduces a narrow execution-substrate claim rather than a
broad “LLMs are computers” thesis. On the current validated scope, append-only
execution traces, exact latest-write retrieval, and a bounded restricted-Wasm /
tiny-`C` useful-case ladder on the narrow Origin-core line remain supported,
with the preserved first `D0` compiled boundary kept as historical support
underneath. Precision stays bounded, the systems gate stays mixed, and broader
compiled or general-computation claims remain blocked.

## Allowed callouts

- append-only trace substrate
- exact latest-write retrieval
- bounded restricted-Wasm / tiny-`C` useful-case ladder
- preserved first tiny typed-bytecode `D0` boundary
- bounded precision with explicit failure counts
- mixed systems result with explicit limitations

## Blocked callouts

- general “LLMs are computers”
- arbitrary C reproduction
- broader compiled demos
- current-scope end-to-end runtime superiority
- claims that a blog/demo is equivalent to evidence

## Required links when reused

- `README.md`
- `STATUS.md`
- `docs/publication_record/submission_packet_index.md`
- `docs/publication_record/claim_ladder.md`

## Use rule

Reuse this skeleton only after `release_candidate_checklist.md` and
`results/release_preflight_checklist_audit/summary.json` are both green. The
blog remains blocked unless `blog_release_rules.md` is also satisfied in full.
