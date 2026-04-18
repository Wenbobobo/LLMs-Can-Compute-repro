"""Export the paper-freeze claim and artifact mapping for P3."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import re

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P3_paper_freeze_and_evidence_mapping"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


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


def extract_backtick_paths(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def get_first_present_value(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        if key in row:
            return row[key]
    raise KeyError(keys[0])


def path_exists(path_text: str) -> bool:
    if any(token in path_text for token in "*?[]"):
        return any(ROOT.glob(path_text))
    return (ROOT / path_text).exists()


def parse_claim_evidence_bullets(text: str) -> dict[str, list[dict[str, object]]]:
    current_section = None
    results: dict[str, list[dict[str, object]]] = defaultdict(list)
    bullet_pattern = re.compile(r"^- `([^`]+)` — `([^`]+)`$")
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("## "):
            current_section = line[3:].strip().lower().replace(" ", "_")
            index += 1
            continue
        match = bullet_pattern.match(line.strip())
        if match and current_section:
            claim_id, path_text = match.groups()
            description_lines: list[str] = []
            index += 1
            while index < len(lines):
                next_line = lines[index]
                if next_line.startswith("- `") or next_line.startswith("## "):
                    break
                stripped = next_line.strip()
                if stripped:
                    description_lines.append(stripped)
                index += 1
            results[current_section].append(
                {
                    "claim_id": claim_id,
                    "path": path_text,
                    "path_exists": path_exists(path_text),
                    "description": " ".join(description_lines),
                }
            )
            continue
        index += 1
    return dict(results)


def build_claim_scope_rows() -> list[dict[str, object]]:
    claim_ladder_path = ROOT / "docs" / "publication_record" / "claim_ladder.md"
    tables = parse_markdown_tables(read_text(claim_ladder_path))
    if not tables:
        raise ValueError("claim_ladder.md must contain at least one markdown table.")

    rows = []
    for row in tables[0]:
        best_evidence_paths = extract_backtick_paths(get_first_present_value(row, "Best evidence"))
        next_target_paths = extract_backtick_paths(
            get_first_present_value(row, "Next evidence target", "Boundary note")
        )
        rows.append(
            {
                "claim_layer": get_first_present_value(row, "Claim layer"),
                "current_status": get_first_present_value(row, "Current status"),
                "best_evidence": [
                    {"path": path, "exists": path_exists(path)}
                    for path in best_evidence_paths
                ],
                "next_evidence_target": [
                    {"path": path, "exists": path_exists(path)}
                    for path in next_target_paths
                ],
            }
        )
    return rows


def build_figure_table_freeze() -> dict[str, object]:
    paper_bundle_path = ROOT / "docs" / "publication_record" / "paper_bundle_status.md"
    tables = parse_markdown_tables(read_text(paper_bundle_path))
    if len(tables) < 2:
        raise ValueError("paper_bundle_status.md must contain figure and table status tables.")

    figures = [
        {"item": row["Item"], "status": row["Status"], "notes": row["Notes"], "section": "mandatory_figures"}
        for row in tables[0]
    ]
    tables_rows = [
        {"item": row["Item"], "status": row["Status"], "notes": row["Notes"], "section": "mandatory_tables"}
        for row in tables[1]
    ]
    status_counter = Counter(item["status"] for item in [*figures, *tables_rows])
    appendix_items = [
        item["item"]
        for item in [*figures, *tables_rows]
        if "appendix" in item["notes"].lower()
    ]
    return {
        "figures": figures,
        "tables": tables_rows,
        "summary": {
            "by_status": [{"status": key, "count": value} for key, value in sorted(status_counter.items())],
            "appendix_linked_items": appendix_items,
        },
    }


def build_unsupported_claims() -> list[dict[str, object]]:
    return [
        {
            "claim_id": "unsupported_general_llm_computation",
            "label": "general LLM computation",
            "reason": "The repository validates a narrow execution substrate rather than a broad claim about general LLMs becoming computers.",
            "source_docs": [
                "README.md",
                "docs/publication_record/threats_to_validity.md",
                "docs/publication_record/blog_outline.md",
            ],
        },
        {
            "claim_id": "unsupported_arbitrary_c",
            "label": "arbitrary C reproduction",
            "reason": "The preserved first compiled boundary is a tiny typed bytecode inside the broader current H43 paper endpoint and should not be inflated into arbitrary-C coverage.",
            "source_docs": [
                "README.md",
                "docs/publication_record/threats_to_validity.md",
                "docs/publication_record/negative_results.md",
            ],
        },
        {
            "claim_id": "unsupported_broad_compiled_demo_widening",
            "label": "broader compiled demos",
            "reason": "Frontend widening remains blocked pending `R2` and an explicit `M7` decision.",
            "source_docs": [
                "docs/publication_record/claim_ladder.md",
                "docs/milestones/M6_compiled_programs_and_demos/status.md",
                "docs/milestones/M7_frontend_candidate_decision/status.md",
            ],
        },
        {
            "claim_id": "unsupported_fair_regime_staged_pointer_success",
            "label": "fair-regime staged-pointer exactness",
            "reason": "The strongest staged-pointer result still depends on stronger legality structure, and the fairer regimes remain negative or caveated.",
            "source_docs": [
                "docs/publication_record/negative_results.md",
                "docs/publication_record/threats_to_validity.md",
            ],
        },
        {
            "claim_id": "unsupported_broad_long_horizon_precision_robustness",
            "label": "broad long-horizon precision robustness",
            "reason": "Current finite-precision evidence is still a current-suite boundary statement rather than a general long-horizon robustness result.",
            "source_docs": [
                "docs/publication_record/threats_to_validity.md",
                "docs/publication_record/negative_results.md",
            ],
        },
        {
            "claim_id": "unsupported_current_scope_end_to_end_runtime_superiority",
            "label": "current-scope end-to-end runtime superiority",
            "reason": "The first systems gate is mixed: geometry is strongly positive, but current-scope lowered execution is not yet faster than the best reference/oracle path.",
            "source_docs": [
                "results/R2_systems_baseline_gate/summary.json",
                "docs/publication_record/negative_results.md",
            ],
        },
    ]


def build_summary(
    *,
    claim_scope_rows: list[dict[str, object]],
    evidence_map: dict[str, list[dict[str, object]]],
    figure_table_freeze: dict[str, object],
    unsupported_claims: list[dict[str, object]],
) -> dict[str, object]:
    blocked_items = [
        item["item"]
        for item in [*figure_table_freeze["figures"], *figure_table_freeze["tables"]]
        if item["status"] != "ready" and item["status"] != "ready on current scope"
    ]
    incomplete_claims = [
        row["claim_layer"]
        for row in claim_scope_rows
        if not row["best_evidence"] or not all(item["exists"] for item in row["best_evidence"])
    ]
    current_evidence = evidence_map.get("current_evidence", [])
    planned_targets = evidence_map.get("planned_next_evidence_targets", [])
    return {
        "claim_row_count": len(claim_scope_rows),
        "current_evidence_entry_count": len(current_evidence),
        "planned_target_entry_count": len(planned_targets),
        "unsupported_claim_count": len(unsupported_claims),
        "blocked_figure_or_table_items": blocked_items,
        "claims_missing_complete_best_evidence": incomplete_claims,
    }


def main() -> None:
    environment = detect_runtime_environment()
    claim_scope_rows = build_claim_scope_rows()
    evidence_map = parse_claim_evidence_bullets(
        read_text(ROOT / "docs" / "publication_record" / "claim_evidence_table.md")
    )
    figure_table_freeze = build_figure_table_freeze()
    unsupported_claims = build_unsupported_claims()
    summary = build_summary(
        claim_scope_rows=claim_scope_rows,
        evidence_map=evidence_map,
        figure_table_freeze=figure_table_freeze,
        unsupported_claims=unsupported_claims,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "claim_scope_rows.json").write_text(
        json.dumps(
            {
                "experiment": "p3_claim_scope_rows",
                "environment": environment.as_dict(),
                "rows": claim_scope_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT_DIR / "artifact_map.json").write_text(
        json.dumps(
            {
                "experiment": "p3_artifact_map",
                "environment": environment.as_dict(),
                "sections": evidence_map,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT_DIR / "figure_table_freeze.json").write_text(
        json.dumps(
            {
                "experiment": "p3_figure_table_freeze",
                "environment": environment.as_dict(),
                **figure_table_freeze,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT_DIR / "unsupported_claims.json").write_text(
        json.dumps(
            {
                "experiment": "p3_unsupported_claims",
                "environment": environment.as_dict(),
                "rows": unsupported_claims,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT_DIR / "summary.json").write_text(
        json.dumps(
            {
                "experiment": "p3_paper_freeze_summary",
                "environment": environment.as_dict(),
                "summary": summary,
                "next_gate_docs": [
                    "docs/milestones/R1_precision_mechanism_closure/",
                    "docs/milestones/R2_systems_baseline_gate/",
                    "docs/milestones/M7_frontend_candidate_decision/",
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# P3 Paper Freeze and Evidence Mapping",
                "",
                "Machine-readable claim/artifact freeze bundle for the current paper-first scope.",
                "",
                "Artifacts:",
                "- `claim_scope_rows.json`",
                "- `artifact_map.json`",
                "- `figure_table_freeze.json`",
                "- `unsupported_claims.json`",
                "- `summary.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
