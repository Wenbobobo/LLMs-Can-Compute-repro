"""Export paper-bundle status summaries from the synchronized publication ledgers."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]


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
    candidate = ROOT / path_text
    return candidate.exists()


def build_figure_table_status() -> dict[str, object]:
    paper_bundle_path = ROOT / "docs" / "publication_record" / "paper_bundle_status.md"
    text = read_text(paper_bundle_path)
    tables = parse_markdown_tables(text)
    if len(tables) < 2:
        raise ValueError("paper_bundle_status.md must contain figure and table status tables.")

    figures = [
        {
            "item": row["Item"],
            "status": row["Status"],
            "notes": row["Notes"],
        }
        for row in tables[0]
    ]
    table_rows = [
        {
            "item": row["Item"],
            "status": row["Status"],
            "notes": row["Notes"],
        }
        for row in tables[1]
    ]
    status_counts = Counter(item["status"] for item in [*figures, *table_rows])
    return {
        "source": paper_bundle_path.relative_to(ROOT).as_posix(),
        "figures": figures,
        "tables": table_rows,
        "summary": {
            "figure_count": len(figures),
            "table_count": len(table_rows),
            "by_status": [{"status": key, "count": value} for key, value in sorted(status_counts.items())],
        },
    }


def build_claim_bundle_completeness() -> dict[str, object]:
    claim_ladder_path = ROOT / "docs" / "publication_record" / "claim_ladder.md"
    claim_rows = parse_markdown_tables(read_text(claim_ladder_path))
    if not claim_rows:
        raise ValueError("claim_ladder.md must contain at least one markdown table.")

    rows = []
    completeness_counter: Counter[str] = Counter()
    for row in claim_rows[0]:
        evidence_paths = extract_backtick_paths(get_first_present_value(row, "Best evidence"))
        next_target_paths = extract_backtick_paths(
            get_first_present_value(row, "Next evidence target", "Boundary note")
        )
        evidence_checks = [
            {"path": path, "exists": path_exists(path)}
            for path in evidence_paths
        ]
        if not evidence_checks:
            completeness = "no_evidence_listed"
        elif all(item["exists"] for item in evidence_checks):
            completeness = "complete"
        elif any(item["exists"] for item in evidence_checks):
            completeness = "partial"
        else:
            completeness = "missing"
        completeness_counter[completeness] += 1
        rows.append(
            {
                "claim_layer": get_first_present_value(row, "Claim layer"),
                "current_status": get_first_present_value(row, "Current status"),
                "best_evidence": evidence_checks,
                "next_evidence_target": next_target_paths,
                "completeness": completeness,
            }
        )

    return {
        "source": claim_ladder_path.relative_to(ROOT).as_posix(),
        "claims": rows,
        "summary": {
            "claim_count": len(rows),
            "by_completeness": [
                {"completeness": key, "count": value}
                for key, value in sorted(completeness_counter.items())
            ],
        },
    }


def build_summary(figure_table_status: dict[str, object], claim_bundle_completeness: dict[str, object]) -> dict[str, object]:
    blocked_items = [
        item["item"]
        for item in [*figure_table_status["figures"], *figure_table_status["tables"]]
        if item["status"] != "ready"
    ]
    incomplete_claims = [
        row["claim_layer"]
        for row in claim_bundle_completeness["claims"]
        if row["completeness"] != "complete"
    ]
    return {
        "figure_table_status_summary": figure_table_status["summary"],
        "claim_bundle_completeness_summary": claim_bundle_completeness["summary"],
        "blocked_or_partial_items": blocked_items,
        "incomplete_claims": incomplete_claims,
    }


def main() -> None:
    environment = detect_runtime_environment()
    figure_table_status = build_figure_table_status()
    claim_bundle_completeness = build_claim_bundle_completeness()
    summary = build_summary(figure_table_status, claim_bundle_completeness)

    out_dir = ROOT / "results" / "P1_paper_readiness"
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "figure_table_status.json").write_text(
        json.dumps(
            {
                "experiment": "p1_figure_table_status",
                "environment": environment.as_dict(),
                **figure_table_status,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "claim_bundle_completeness.json").write_text(
        json.dumps(
            {
                "experiment": "p1_claim_bundle_completeness",
                "environment": environment.as_dict(),
                **claim_bundle_completeness,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "summary.json").write_text(
        json.dumps(
            {
                "experiment": "p1_paper_bundle_summary",
                "environment": environment.as_dict(),
                **summary,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(out_dir.as_posix())


if __name__ == "__main__":
    main()
