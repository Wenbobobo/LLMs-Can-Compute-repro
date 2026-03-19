# Appendix Boundary Map

This file fixes which artifacts stay in the appendix so later drafting does not
inflate companion diagnostics into main-text claims.

## Minimum appendix package

These items are required for the current freeze candidate and should remain the
canonical appendix spine:

| Artifact family | Status | Why it belongs there | Guardrail |
| --- | --- | --- | --- |
| `D0` memory-surface diagnostics | required | They audit the compiled boundary without widening it. | Do not present them as broader compiler or runtime evidence. |
| `D0` stress/reference companion rows | required | They strengthen confidence in the frozen endpoint while staying outside the main-text starter-suite table. | Do not treat companion success as a warrant for frontend widening. |
| Regeneration and public-safe release ledgers | required | The freeze candidate must remain auditable and outwardly disciplined. | Keep packaging details downstream of the claim/evidence map. |

## Allowed optional appendix material

These companions may stay linked in the appendix when they help auditability,
but they are not freeze blockers by themselves:

| Artifact family | Status | Why it belongs there | Guardrail |
| --- | --- | --- | --- |
| Per-stream precision catalogs | optional | They are useful for re-analysis, but the main text already carries the distilled precision boundary. | Do not turn them into a broader scaling claim. |
| Full staged failure digests and provenance rows | optional | They help trace the negative closure without forcing new prose or layout churn. | Raw rows should support the distilled failure taxonomy, not compete with it. |
| Full `P1` rendered tables and layout helpers | optional | They support paper assembly and reproducibility more than they advance the scientific argument. | Keep the canonical machine-readable source as the primary reference. |

## Out-of-scope appendix material

These items stay out of the current freeze candidate:

- a standalone systems gate table or the full `R2` runtime matrix in main text;
- broader compiled demos or any frontend widening beyond `D0`;
- any appendix branch that would read as a new evidence wave rather than as a
  companion to an already-frozen claim.

## Main-text boundary

The main text should only carry material that directly supports one of the
frozen current-scope claim rows:

- `A1` append-only trace substrate;
- `B1` exact 2D hard-max retrieval;
- `C2h` staged mask-dependence closure;
- `C3e` broadened but still narrow precision boundary;
- `D0` tiny typed-bytecode boundary.

Everything else should remain appendix-level unless a later scope change is
explicitly recorded first in the ledgers.
