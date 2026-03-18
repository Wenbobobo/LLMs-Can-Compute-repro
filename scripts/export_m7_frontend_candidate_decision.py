"""Export the frontend-candidate decision bundle for M7."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "M7_frontend_candidate_decision"


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_gate_inputs() -> dict[str, object]:
    return {
        "p3_summary": read_json(ROOT / "results" / "P3_paper_freeze_and_evidence_mapping" / "summary.json"),
        "p3_unsupported_claims": read_json(
            ROOT / "results" / "P3_paper_freeze_and_evidence_mapping" / "unsupported_claims.json"
        ),
        "r1_summary": read_json(ROOT / "results" / "R1_precision_mechanism_closure" / "summary.json"),
        "r2_summary": read_json(ROOT / "results" / "R2_systems_baseline_gate" / "summary.json"),
    }


def classify_minimal_widening_status(*, r2_gate_status: str, paper_scope_ready: bool) -> str:
    if not paper_scope_ready:
        return "blocked"
    if r2_gate_status == "positive_current_scope":
        return "revisit"
    return "blocked"


def build_candidate_matrix(
    *,
    p3_summary: dict[str, object],
    p3_unsupported_claims: dict[str, object],
    r1_summary: dict[str, object],
    r2_summary: dict[str, object],
) -> list[dict[str, object]]:
    p3 = p3_summary["summary"]
    r1 = r1_summary["summary"]
    r2_gate = r2_summary["gate_summary"]
    unsupported_rows = p3_unsupported_claims["rows"]
    unsupported_ids = {str(row["claim_id"]) for row in unsupported_rows}
    paper_scope_ready = not p3["blocked_figure_or_table_items"] and not p3["claims_missing_complete_best_evidence"]
    minimal_widening_status = classify_minimal_widening_status(
        r2_gate_status=str(r2_gate["gate_status"]),
        paper_scope_ready=bool(paper_scope_ready),
    )

    return [
        {
            "candidate_id": "stay_on_tiny_typed_bytecode",
            "label": "Stay on tiny typed bytecode",
            "decision": "selected" if paper_scope_ready else "hold",
            "claim_delta": "none",
            "systems_readiness": "acceptable",
            "paper_scope_alignment": "preserves the frozen paper-grade claim set",
            "blocked_by": [],
            "rationale": [
                "P3 already freezes the current paper scope without missing best-evidence paths.",
                (
                    f"R1 closes as `{r1['claim_update']}`: decomposition is useful on the current validated suite, "
                    "but the result is still a boundary statement."
                ),
                (
                    f"R2 remains `{r2_gate['gate_status']}`, so frontend widening would outrun the current systems evidence."
                ),
            ],
        },
        {
            "candidate_id": "minimal_frontend_widening",
            "label": "Approve one minimal next frontend candidate",
            "decision": minimal_widening_status,
            "claim_delta": "would require a new scope statement plus another evidence-mapping pass",
            "systems_readiness": "not_ready" if minimal_widening_status == "blocked" else "revisit_after_new_scope",
            "paper_scope_alignment": "would widen the current endpoint beyond the frozen D0 boundary",
            "blocked_by": [
                "current-scope systems gate is not yet positive",
                "current unsupported-claim ledger still blocks broader compiled-demo wording",
            ]
            if minimal_widening_status == "blocked"
            else [
                "any revisit would still need a fresh scope definition and a new systems pass",
            ],
            "rationale": [
                (
                    "Minimal widening is not selected by default because the current repository already has a complete "
                    "paper-safe endpoint."
                ),
                (
                    "The unsupported-claim ledger still includes broader compiled-demo widening and current-scope "
                    "runtime superiority."
                )
                if "unsupported_broad_compiled_demo_widening" in unsupported_ids
                else "The current frozen scope does not need extra frontend breadth to support its claims.",
            ],
        },
        {
            "candidate_id": "demo_first_public_widening",
            "label": "Promote a broader demo-first frontend now",
            "decision": "rejected",
            "claim_delta": "would overstate the present scientific scope",
            "systems_readiness": "not_ready",
            "paper_scope_alignment": "conflicts with the paper-first gate",
            "blocked_by": [
                "unsupported general-LLM and arbitrary-C claims remain explicit no-go areas",
                "blog/demo narrative is downstream of paper-grade evidence",
            ],
            "rationale": [
                "The current project goal is a narrow execution-substrate reproduction, not a presentation-first demo.",
                "A broader demo would blur the distinction between mechanism evidence and broader language/runtime claims.",
            ],
        },
    ]


def build_decision_summary(
    *,
    p3_summary: dict[str, object],
    r1_summary: dict[str, object],
    r2_summary: dict[str, object],
    candidate_matrix: list[dict[str, object]],
) -> dict[str, object]:
    p3 = p3_summary["summary"]
    r1 = r1_summary["summary"]
    r2_gate = r2_summary["gate_summary"]
    selected = next(row for row in candidate_matrix if row["decision"] == "selected")
    return {
        "decision_id": "m7_frontend_candidate_decision",
        "selected_candidate_id": selected["candidate_id"],
        "selected_candidate_label": selected["label"],
        "decision_status": "stay_on_tiny_typed_bytecode",
        "frontend_widening_authorized": False,
        "public_demo_authorized": False,
        "paper_scope_ready": not p3["blocked_figure_or_table_items"] and not p3["claims_missing_complete_best_evidence"],
        "gating_facts": [
            f"P3 blocked figure/table items: {len(p3['blocked_figure_or_table_items'])}.",
            f"P3 missing-complete-best-evidence claims: {len(p3['claims_missing_complete_best_evidence'])}.",
            (
                f"R1 claim update: {r1['claim_update']}; single-head failure streams: "
                f"{r1['single_head_failure_stream_count']}/{r1['stream_count']}."
            ),
            (
                f"R2 gate: {r2_gate['gate_status']}; lowered path ratio vs best reference: "
                f"{float(r2_gate['lowered_ratio_vs_best_reference']):.4f}."
            ),
        ],
        "claim_impact": [
            "The current D0 bundle remains the explicit compiled endpoint for the paper-grade claim set.",
            "Future frontend widening is not automatic; it now requires a new scope decision plus stronger systems evidence.",
            "Blog/demo prose remains downstream of this no-go decision rather than a reason to override it.",
        ],
        "revisit_prerequisites": [
            "another systems pass that makes widened execution competitive on the chosen scope",
            "an explicit new claim/evidence mapping update for any widened frontend",
            "a public-safe narrative that does not collapse D0 into arbitrary language or runtime claims",
        ],
        "blocked_hypotheses": [
            "broader frontend is the automatic next step",
            "current geometry advantage alone justifies widening",
            "compiled demos are needed before the present paper scope is complete",
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_gate_inputs()
    candidate_matrix = build_candidate_matrix(**inputs)
    decision_summary = build_decision_summary(
        p3_summary=inputs["p3_summary"],
        r1_summary=inputs["r1_summary"],
        r2_summary=inputs["r2_summary"],
        candidate_matrix=candidate_matrix,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "candidate_matrix.json",
        {
            "experiment": "m7_frontend_candidate_matrix",
            "environment": environment.as_dict(),
            "rows": candidate_matrix,
        },
    )
    write_json(
        OUT_DIR / "decision_summary.json",
        {
            "experiment": "m7_frontend_candidate_decision",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/P3_paper_freeze_and_evidence_mapping/summary.json",
                "results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json",
                "results/R1_precision_mechanism_closure/summary.json",
                "results/R2_systems_baseline_gate/summary.json",
                "docs/milestones/M6_frontend_spec/",
                "docs/milestones/M6_compiled_programs_and_demos/",
            ],
            "summary": decision_summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# M7 Frontend Candidate Decision",
                "",
                "Current decision bundle for whether any frontend widening is justified after P3/R1/R2.",
                "",
                "Decision:",
                "- stay on the current tiny typed-bytecode endpoint;",
                "- do not authorize frontend widening on the current systems evidence;",
                "- keep blog/demo narrative downstream of this restraint.",
                "",
                "Artifacts:",
                "- `decision_summary.json`",
                "- `candidate_matrix.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
