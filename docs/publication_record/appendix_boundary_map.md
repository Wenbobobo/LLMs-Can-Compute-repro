# Appendix Boundary Map

This file fixes which artifacts stay in the appendix so later drafting does not
inflate companion diagnostics into main-text claims.

| Artifact family | Placement | Why it belongs there | When it may move | Guardrail |
| --- | --- | --- | --- | --- |
| Memory-surface diagnostics for `D0` | appendix | They strengthen the current compiled boundary but do not define a new claim layer by themselves. | Only if a future paper version makes memory-surface behavior part of a main-text claim. | Do not present them as broader compiler or runtime evidence. |
| Full `P1` rendered tables and layout helpers | appendix | They support paper assembly and reproducibility more than they advance the core scientific argument. | They may be excerpted into main text only if the section map explicitly requires them. | Keep the canonical machine-readable source as the primary reference. |
| Stress/reference companion rows beyond the main `D0` summary | appendix | They deepen confidence in the frozen boundary without widening it. | Only if a future revision needs a more detailed `D0` table in main text. | Do not treat companion success as a warrant for frontend widening. |
| Per-stream precision catalogs | appendix | They are useful for auditability and re-analysis, but the main text should carry only the distilled boundary. | Only if a specific stream family becomes central to a revised claim. | Main text must still state the boundary at the family/scheme level. |
| Full staged failure digests and provenance rows | appendix | The paper needs the distilled failure taxonomy, not every raw row, in the main narrative. | Only if a reviewer-facing revision needs direct row-level evidence in-line. | Raw rows should support the distilled negative closure, not compete with it. |
| Public-safe packaging ledger and regeneration commands | appendix | They are necessary for reproduction and release discipline, but secondary to the scientific storyline. | Never as a claim-bearing main-text section. | Keep packaging details downstream of the claim/evidence map. |

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
