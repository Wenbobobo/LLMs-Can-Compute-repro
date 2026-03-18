# Status

Provisioned on 2026-03-18 to capture the publication readiness effort immediately after `P1_paper_readiness`.

- ledger-first discipline is in place: every packaging update appends to root
  `STATUS.md` with precise claim references;
- python 3.12 + `uv run scripts/export_p1_paper_readiness.py` anchors the reproducibility instructions;
- the current `P1` bundle now already includes the `D0` memory-surface
  appendix companion, so `P2` can shift from “bootstrap packaging” to
  “public-safe release bookkeeping”;
- the release ledger now also includes
  `results/M6_stress_reference_followup/`, so the current `D0` public-safe
  artifact set is synchronized;
- the release ledger now also includes the `M7` decision bundle and the `P4`
  release gate, so the current public-safe posture is explicit rather than
  implied;
- the `H0` release-hygiene snapshot now records a clean main worktree after the
  split was applied and pushed, so the next packaging work is downstream
  manuscript / release assembly rather than repo cleanup;
- the blog remains locked after the completed `M7` / `P4` no-go outcome, but
  the future blog/paper outline is documented here for quick reference.
