"""Export the P5 manuscript callout-alignment audit."""

from __future__ import annotations

import json
from pathlib import Path

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P5_callout_alignment"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 8) -> list[str]:
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(needle in lowered for needle in lowered_needles):
            if line not in seen:
                hits.append(line)
                seen.add(line)
        if len(hits) >= max_lines:
            break
    return hits


def load_inputs() -> dict[str, str]:
    return {
        "manuscript_text": read_text(ROOT / "docs" / "publication_record" / "manuscript_bundle_draft.md"),
        "caption_text": read_text(ROOT / "docs" / "publication_record" / "caption_candidate_notes.md"),
        "roles_text": read_text(ROOT / "docs" / "publication_record" / "figure_table_narrative_roles.md"),
        "section_map_text": read_text(ROOT / "docs" / "publication_record" / "manuscript_section_map.md"),
    }


def build_alignment_rows(
    *,
    manuscript_text: str,
    caption_text: str,
    roles_text: str,
    section_map_text: str,
) -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "introduction_claim_pair",
            "status": "pass"
            if contains_all(
                manuscript_text,
                ["claim-ladder figure", "supported-versus-unsupported claims table"],
            )
            and contains_all(
                caption_text,
                ["Claim ladder + evidence matrix", "Supported vs unsupported claims table"],
            )
            and contains_all(
                roles_text,
                ["Claim ladder + evidence matrix", "Supported vs unsupported claims"],
            )
            and contains_all(section_map_text, ["| Introduction |", "claim_ladder.md", "unsupported_claims.json"])
            else "blocked",
            "notes": "The introduction should keep the claim-ladder figure and the supported/unsupported table paired and explicit.",
        },
        {
            "row_id": "precision_boundary_pair",
            "status": "pass"
            if contains_all(
                manuscript_text,
                ["real-trace boundary figure", "boundary table"],
            )
            and contains_all(
                caption_text,
                ["Real-trace precision boundary figure", "Real-trace precision boundary table"],
            )
            and contains_all(
                roles_text,
                ["Real-trace precision boundary", "Real-trace precision boundary table"],
            )
            and contains_all(section_map_text, ["| Precision boundary |", "m4_real_trace_boundary_figure.svg"])
            else "blocked",
            "notes": "The precision section should keep the figure/table pair aligned across manuscript, captions, and roles.",
        },
        {
            "row_id": "compiled_boundary_pair",
            "status": "pass"
            if contains_all(
                manuscript_text,
                ["frontend boundary diagram", "starter suite does and does not validate"],
            )
            and contains_all(
                caption_text,
                ["Frontend boundary diagram", "Exact-trace / final-state success table"],
            )
            and contains_all(
                roles_text,
                ["Frontend boundary diagram", "Exact-trace / final-state success table"],
            )
            and contains_all(
                section_map_text,
                ["| Compiled boundary |", "m6_frontend_boundary_diagram.svg", "exact_trace_final_state_table.md"],
            )
            else "blocked",
            "notes": "The compiled-boundary section should keep the diagram/table pair explicit and main-text scoped.",
        },
        {
            "row_id": "compiled_boundary_companion_split",
            "status": "pass"
            if contains_all(
                manuscript_text,
                ["Companion appendix material stays clearly downstream", "they do not widen it"],
            )
            and contains_all(
                caption_text,
                ["companion evidence outside the main table", "do not authorize broader compiled demos"],
            )
            and contains_all(
                roles_text,
                ["stress/reference and memory-surface rows remain companion evidence outside the table"],
            )
            else "blocked",
            "notes": "Starter-suite main-text evidence and companion compiled-boundary evidence should remain explicitly separated.",
        },
        {
            "row_id": "threats_table_alignment",
            "status": "pass"
            if contains_all(
                manuscript_text,
                ["threats-to-validity table"],
            )
            and contains_all(
                caption_text,
                ["Threats-to-validity table"],
            )
            and contains_all(
                roles_text,
                ["Threats-to-validity table"],
            )
            and contains_all(section_map_text, ["| Negative results and threats |"])
            else "blocked",
            "notes": "Threats should remain tied to one explicit main-text table across the paper-facing ledgers.",
        },
    ]
    return rows


def build_snapshot(inputs: dict[str, str]) -> list[dict[str, object]]:
    lookup = {
        "docs/publication_record/manuscript_bundle_draft.md": (
            "manuscript_text",
            [
                "claim-ladder figure",
                "supported-versus-unsupported claims table",
                "real-trace boundary figure",
                "frontend boundary diagram",
                "threats-to-validity table",
            ],
        ),
        "docs/publication_record/caption_candidate_notes.md": (
            "caption_text",
            [
                "Claim ladder + evidence matrix",
                "Real-trace precision boundary figure",
                "Frontend boundary diagram",
                "Exact-trace / final-state success table",
                "Threats-to-validity table",
            ],
        ),
        "docs/publication_record/figure_table_narrative_roles.md": (
            "roles_text",
            [
                "Claim ladder + evidence matrix",
                "Exact-trace / final-state success table",
                "Real-trace precision boundary",
                "Threats-to-validity table",
            ],
        ),
        "docs/publication_record/manuscript_section_map.md": (
            "section_map_text",
            [
                "| Introduction |",
                "| Precision boundary |",
                "| Compiled boundary |",
                "| Negative results and threats |",
            ],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append(
            {
                "path": path,
                "matched_lines": extract_matching_lines(inputs[input_key], needles=needles),
            }
        )
    return rows


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_rows = [row["row_id"] for row in rows if row["status"] != "pass"]
    return {
        "alignment_scope": "p5_main_text_callout_and_caption_pairs",
        "row_count": len(rows),
        "pass_count": sum(row["status"] == "pass" for row in rows),
        "blocked_count": sum(row["status"] != "pass" for row in rows),
        "blocked_rows": blocked_rows,
        "recommended_next_action": (
            "keep the current main-text artifact pairings fixed through the P8 submission-candidate bundle lock"
            if not blocked_rows
            else "resolve the blocked manuscript/caption/callout alignment rows before broader prose edits"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    rows = build_alignment_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "p5_callout_alignment_checklist",
            "environment": environment.as_dict(),
            "rows": rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "p5_callout_alignment_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p5_callout_alignment",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/publication_record/manuscript_bundle_draft.md",
                "docs/publication_record/caption_candidate_notes.md",
                "docs/publication_record/figure_table_narrative_roles.md",
                "docs/publication_record/manuscript_section_map.md",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# P5 Callout Alignment",
                "",
                "Machine-readable audit that the current manuscript draft, caption notes,",
                "figure/table narrative roles, and section map remain aligned on the main-text",
                "artifact pairs that carry the paper's current scope.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
