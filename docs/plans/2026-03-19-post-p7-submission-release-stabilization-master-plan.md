# Post-P7 Submission/Release Stabilization Master Plan

## Summary

The repository is no longer in an open evidence-wave phase. `P7` closed the
current paper-facing work as a freeze-candidate checkpoint, and `H1` removed
historical ambiguity around older unchecked rows. The next stage therefore
starts from a fixed claim/evidence bundle and should focus on submission-grade
locking, release hygiene, and explicit governance for any future reopen.

The scientific scope stays fixed:

- append-only execution traces;
- exact latest-write retrieval on that trace;
- bounded precision on the exported real/organic trace suite;
- tiny typed-bytecode `D0` as the current compiled endpoint.

The next stage splits into four lanes:

- `P8_submission_candidate_and_bundle_lock`
- `H2_release_hygiene_and_audit_promotion`
- `P9_release_candidate_and_public_surface_freeze`
- `E1_conditional_evidence_reopen_protocol`

## Execution Order

1. Record this master plan and create milestone scaffolds before any wider doc
   edits.
2. Complete `H2` first so that later bundle-lock and release work has a new
   machine-audited standing gate.
3. Run `P8` next on the frozen manuscript bundle, appendix minimum package, and
   paper-facing ledgers.
4. Run `P9` only after `P8` and `H2` are green; keep blog work blocked.
5. Enter `E1` only if an explicit audit or bundle conflict triggers a real
   reopen condition.

## Parallel Protocol

- `wt-paper`: manuscript, appendix, and publication ledgers for `P8`.
- `wt-hygiene`: audits, manifests, and release-control machinery for `H2`.
- `wt-release`: README / STATUS / release summary / blog gate work for `P9`.
- `main`: integration, validation, commit, and push only.

Each worker must leave:

- updated `status.md`;
- updated `todo.md`;
- updated `artifact_index.md`;
- any new artifact or audit result;
- the minimum validation needed for its lane.

## Integration Gate

Integrate only when all touched lanes satisfy:

1. no claim wording conflict with the current manuscript bundle;
2. `results/P1_paper_readiness/summary.json` still reports `10/10` ready items;
3. `results/P5_public_surface_sync/summary.json` reports zero blocked items;
4. `results/P5_callout_alignment/summary.json` reports zero blocked rows;
5. the new `H2` bundle-lock audit reports zero blocked items;
6. `pytest -q` passes;
7. `git diff --check` passes.

## Default Assumptions

- No new evidence wave is open by default.
- No frontend widening is authorized.
- Blog work remains blocked and derivative-only.
- Any reopen must be named, narrow, and routed through `E1`.
