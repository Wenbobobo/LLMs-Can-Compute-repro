# Integration Log

## 2026-03-19 — public-surface sync to `main`

### Scope

- synced the `P5` manuscript-assembly batch from `wip/p3-paper-freeze` back to
  `main` by fast-forward;
- carried over the new publication-record assets:
  - `manuscript_bundle_draft.md`
  - `appendix_stub_notes.md`
  - `caption_candidate_notes.md`
  - `layout_decision_log.md`
  - `figure_table_narrative_roles.md`
  - `section_caption_notes.md`
  - `manuscript_stub_notes.md`
- carried over the public-surface wording refresh for `README.md` and
  `STATUS.md`;
- carried over the refreshed `P1` readiness exports with the `D0`
  exact-trace/final-state table normalized to current-scope `ready`.

### Validation

- `git diff --check` passed on `main`;
- `uv run pytest -q` passed on `main` with `129 passed, 1 warning`.

### Outcome

- `main` is no longer behind the active paper scope;
- the repository front page, status page, `P1` readiness exports, and
  publication ledgers now tell the same current-scope story;
- the next paper-lane work can move back to drafting strategy instead of
  emergency public-surface catch-up.
