"""Export the outward-release gate bundle for P4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P4_blog_release_gate"


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_markdown_tables(text: str) -> list[list[dict[str, str]]]:
    tables: list[list[str]] = []
    current: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("|") and line.endswith("|"):
            current.append(line)
            continue
        if current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)

    parsed: list[list[dict[str, str]]] = []
    for lines in tables:
        if len(lines) < 2:
            continue
        headers = [cell.strip() for cell in lines[0].strip("|").split("|")]
        rows: list[dict[str, str]] = []
        for line in lines[2:]:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) != len(headers):
                continue
            rows.append(dict(zip(headers, cells, strict=True)))
        parsed.append(rows)
    return parsed


def load_release_inputs() -> dict[str, object]:
    return {
        "p3_summary": read_json(ROOT / "results" / "P3_paper_freeze_and_evidence_mapping" / "summary.json"),
        "p3_unsupported_claims": read_json(
            ROOT / "results" / "P3_paper_freeze_and_evidence_mapping" / "unsupported_claims.json"
        ),
        "m7_decision": read_json(ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json"),
        "artifact_release_ledger": parse_markdown_tables(
            read_text(ROOT / "docs" / "milestones" / "P2_public_research_packaging" / "artifact_release_ledger.md")
        )[0],
        "gitignore_text": read_text(ROOT / ".gitignore"),
        "readme_text": read_text(ROOT / "README.md"),
        "blog_outline_text": read_text(ROOT / "docs" / "publication_record" / "blog_outline.md"),
    }


def has_required_gitignore_entries(text: str) -> tuple[bool, list[str]]:
    required = ["docs/Origin/", "docs/origin/", "tmp/"]
    missing = [entry for entry in required if entry not in text]
    return not missing, missing


def blog_outline_is_downstream(text: str) -> bool:
    lowered = text.lower()
    return "blocked" in lowered and (
        "derived from it rather than define it" in lowered
        or "systems and public-release gates" in lowered
        or "broader blog prose should wait" in lowered
    )


def build_release_checklist(
    *,
    p3_summary: dict[str, object],
    m7_decision: dict[str, object],
    artifact_release_ledger: list[dict[str, str]],
    gitignore_text: str,
    readme_text: str,
    blog_outline_text: str,
) -> list[dict[str, object]]:
    p3 = p3_summary["summary"]
    m7 = m7_decision["summary"]
    ledger_paths = {row["Artifact bundle"] for row in artifact_release_ledger}
    ledger_has_required_rows = {
        "results/M6_typed_bytecode_harness/": "`results/M6_typed_bytecode_harness/`" in ledger_paths,
        "results/M6_memory_surface_followup/": "`results/M6_memory_surface_followup/`" in ledger_paths,
        "results/M6_stress_reference_followup/": "`results/M6_stress_reference_followup/`" in ledger_paths,
        "results/P1_paper_readiness/": "`results/P1_paper_readiness/`" in ledger_paths,
        "docs/publication_record/": "`docs/publication_record/`" in ledger_paths,
        "docs/Origin/": "`docs/Origin/`" in ledger_paths,
        "results/M7_frontend_candidate_decision/": "`results/M7_frontend_candidate_decision/`" in ledger_paths,
        "results/P4_blog_release_gate/": "`results/P4_blog_release_gate/`" in ledger_paths,
    }
    gitignore_ok, missing_gitignore = has_required_gitignore_entries(gitignore_text)
    readme_has_scope_guard = "does **not** claim that general LLMs are computers" in readme_text and "arbitrary C" in readme_text
    blog_is_downstream = blog_outline_is_downstream(blog_outline_text)
    blog_authorized = bool(m7["public_demo_authorized"])

    return [
        {
            "item_id": "paper_scope_frozen",
            "status": "pass"
            if not p3["blocked_figure_or_table_items"] and not p3["claims_missing_complete_best_evidence"]
            else "blocked",
            "notes": "P3 already has no blocked figure/table items and no claims missing complete best-evidence paths.",
        },
        {
            "item_id": "frontend_scope_decided",
            "status": "pass"
            if m7["decision_status"] == "stay_on_tiny_typed_bytecode" and not m7["frontend_widening_authorized"]
            else "blocked",
            "notes": "M7 now records an explicit no-go for frontend widening on current evidence.",
        },
        {
            "item_id": "restricted_material_excluded",
            "status": "pass" if gitignore_ok else "blocked",
            "notes": "Required ignore entries present."
            if gitignore_ok
            else f"Missing ignore entries: {', '.join(missing_gitignore)}.",
        },
        {
            "item_id": "public_safe_artifact_ledger",
            "status": "pass" if all(ledger_has_required_rows.values()) else "blocked",
            "notes": "P2 artifact ledger includes the current public-safe core, decision, and gate bundles."
            if all(ledger_has_required_rows.values())
            else "P2 artifact ledger is missing one or more current public-safe bundles.",
            "missing_rows": [path for path, present in ledger_has_required_rows.items() if not present],
        },
        {
            "item_id": "readme_keeps_narrow_scope",
            "status": "pass" if readme_has_scope_guard else "blocked",
            "notes": "README still states the narrow scope and rejects broad general-LLM / arbitrary-C claims."
            if readme_has_scope_guard
            else "README no longer states the narrow-scope guardrails clearly enough.",
        },
        {
            "item_id": "blog_outline_stays_downstream",
            "status": "pass" if blog_is_downstream else "blocked",
            "notes": "Blog outline is still derived from the paper bundle rather than driving it."
            if blog_is_downstream
            else "Blog outline wording no longer keeps the blog downstream of the paper bundle.",
        },
        {
            "item_id": "blog_release_authorized",
            "status": "blocked" if not blog_authorized else "pass",
            "notes": "Blog remains blocked because M7 does not authorize a broader outward narrative."
            if not blog_authorized
            else "Blog is authorized by the current decision bundle.",
        },
    ]


def build_claim_artifact_audit(
    *,
    p3_unsupported_claims: dict[str, object],
    m7_decision: dict[str, object],
) -> list[dict[str, object]]:
    rows = [
        {
            "claim_id": "public_landing_page_narrow_scope",
            "label": "narrow execution-substrate reproduction",
            "surface": "README.md",
            "release_posture": "allowed_now",
            "evidence_paths": [
                "README.md",
                "results/P3_paper_freeze_and_evidence_mapping/summary.json",
                "results/M7_frontend_candidate_decision/decision_summary.json",
            ],
            "notes": "The landing page is acceptable as a restrained research entry point because it stays inside the frozen paper scope.",
        }
    ]
    for row in p3_unsupported_claims["rows"]:
        evidence_paths = [
            "results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json",
            *[str(path) for path in row["source_docs"]],
        ]
        if "frontend" in str(row["claim_id"]) or "runtime" in str(row["claim_id"]):
            evidence_paths.append("results/M7_frontend_candidate_decision/decision_summary.json")
        rows.append(
            {
                "claim_id": row["claim_id"],
                "label": row["label"],
                "surface": "future blog / outward summary",
                "release_posture": "blocked",
                "evidence_paths": sorted(dict.fromkeys(evidence_paths)),
                "notes": row["reason"],
            }
        )
    rows.append(
        {
            "claim_id": "blog_release_gate",
            "label": "broader public blog narrative",
            "surface": "blog",
            "release_posture": "blocked",
            "evidence_paths": [
                "docs/publication_record/blog_outline.md",
                "results/M7_frontend_candidate_decision/decision_summary.json",
            ],
            "notes": "Current public posture remains README-first and paper-first; the blog is not yet authorized.",
        }
    )
    return rows


def build_summary(
    *,
    checklist_rows: list[dict[str, object]],
    claim_audit_rows: list[dict[str, object]],
    m7_decision: dict[str, object],
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    blocked_claims = [row["claim_id"] for row in claim_audit_rows if row["release_posture"] == "blocked"]
    m7 = m7_decision["summary"]
    return {
        "release_status": "blog_blocked_readme_only" if not m7["public_demo_authorized"] else "blog_authorized",
        "blog_authorized": bool(m7["public_demo_authorized"]),
        "readme_posture": "restrained_research_landing_page_allowed",
        "checklist_item_count": len(checklist_rows),
        "checklist_pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "checklist_blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "claim_audit_row_count": len(claim_audit_rows),
        "blocked_claim_count": len(blocked_claims),
        "required_before_blog": list(m7["revisit_prerequisites"]),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_release_inputs()
    checklist_rows = build_release_checklist(
        p3_summary=inputs["p3_summary"],
        m7_decision=inputs["m7_decision"],
        artifact_release_ledger=inputs["artifact_release_ledger"],
        gitignore_text=str(inputs["gitignore_text"]),
        readme_text=str(inputs["readme_text"]),
        blog_outline_text=str(inputs["blog_outline_text"]),
    )
    claim_audit_rows = build_claim_artifact_audit(
        p3_unsupported_claims=inputs["p3_unsupported_claims"],
        m7_decision=inputs["m7_decision"],
    )
    summary = build_summary(
        checklist_rows=checklist_rows,
        claim_audit_rows=claim_audit_rows,
        m7_decision=inputs["m7_decision"],
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "release_checklist.json",
        {
            "experiment": "p4_blog_release_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "claim_artifact_audit.json",
        {
            "experiment": "p4_claim_artifact_audit",
            "environment": environment.as_dict(),
            "rows": claim_audit_rows,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p4_blog_release_gate",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                ".gitignore",
                "docs/milestones/P2_public_research_packaging/artifact_release_ledger.md",
                "docs/publication_record/blog_outline.md",
                "results/P3_paper_freeze_and_evidence_mapping/summary.json",
                "results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json",
                "results/M7_frontend_candidate_decision/decision_summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# P4 Blog Release Gate",
                "",
                "Current outward-release gate for deciding whether the repo can support a broader blog narrative.",
                "",
                "Decision:",
                "- README may stay as a restrained research landing page;",
                "- restricted source material remains excluded;",
                "- blog release stays blocked on the current M7 no-go decision.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `release_checklist.json`",
                "- `claim_artifact_audit.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
