"""Export the P5 public-surface sync audit for the current paper lane."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P5_public_surface_sync"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_inputs() -> dict[str, str]:
    return {
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "manuscript_text": read_text(ROOT / "docs" / "publication_record" / "manuscript_bundle_draft.md"),
        "layout_log_text": read_text(ROOT / "docs" / "publication_record" / "layout_decision_log.md"),
        "p5_status_text": read_text(ROOT / "docs" / "milestones" / "P5_paper_draft_assembly" / "status.md"),
        "p5_todo_text": read_text(ROOT / "docs" / "milestones" / "P5_paper_draft_assembly" / "todo.md"),
    }


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def contains_none(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() not in lowered for needle in needles)


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 6) -> list[str]:
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


def build_sync_checklist(
    *,
    readme_text: str,
    status_text: str,
    publication_readme_text: str,
    release_summary_text: str,
    manuscript_text: str,
    layout_log_text: str,
    p5_status_text: str,
    p5_todo_text: str,
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "readme_keeps_narrow_scope",
            "status": "pass"
            if contains_all(readme_text, ["does **not** claim that general llms are computers", "arbitrary c"])
            else "blocked",
            "notes": "README keeps the narrow-scope guardrails explicit.",
        },
        {
            "item_id": "readme_tracks_current_paper_phase",
            "status": "pass"
            if contains_all(readme_text, ["layout-tightening and release-readiness pass", "manuscript-freeze candidacy"])
            else "blocked",
            "notes": "README now describes the post-P6 freeze/preflight handoff rather than the earlier layout-in-progress phase.",
        },
        {
            "item_id": "status_tracks_current_paper_phase",
            "status": "pass"
            if contains_all(
                status_text,
                ["layout-tightening and release-readiness pass is now complete", "manuscript-freeze candidacy", "release_summary_draft.md"],
            )
            else "blocked",
            "notes": "STATUS records the completed P6 phase and the downstream short-summary source.",
        },
        {
            "item_id": "publication_record_readme_tracks_downstream_source",
            "status": "pass"
            if contains_all(publication_readme_text, ["release_summary_draft.md", "approved as the source"])
            else "blocked",
            "notes": "Publication record README names the approved short-update source explicitly.",
        },
        {
            "item_id": "release_summary_stays_downstream",
            "status": "pass"
            if contains_all(
                release_summary_text,
                [
                    "This repository reproduces a narrow execution-substrate claim",
                    "Current paper-facing follow-up",
                    "manuscript-freeze candidacy",
                ],
            )
            and contains_none(release_summary_text, ["Status: short downstream summary"])
            else "blocked",
            "notes": "The release summary stays narrow and current without falling back to an internal status preamble.",
        },
        {
            "item_id": "manuscript_tracks_section_draft_state",
            "status": "pass"
            if contains_all(
                manuscript_text,
                [
                    "## 1. Abstract",
                    "## 10. Reproducibility Appendix",
                    "later no-widening decision",
                ],
            )
            and contains_none(manuscript_text, ["Status: paper-shaped manuscript section draft"])
            else "blocked",
            "notes": "The manuscript now reads as a section-ordered draft instead of carrying a phase-status preamble.",
        },
        {
            "item_id": "layout_log_records_release_summary_reuse",
            "status": "pass"
            if contains_all(layout_log_text, ["release-summary reuse", "README-adjacent short updates"])
            else "blocked",
            "notes": "The layout decision log still records release-summary reuse as an explicit decision.",
        },
        {
            "item_id": "p5_ledger_tracks_recent_sync",
            "status": "pass"
            if contains_all(
                p5_status_text,
                ["`P5` acceptance is now satisfied", "release-readiness phase"],
            )
            and contains_all(
                p5_todo_text,
                ["callout-alignment pass", "layout/readiness milestone scaffold"],
            )
            else "blocked",
            "notes": "The P5 milestone ledger records closure and the explicit handoff to the next layout/readiness phase.",
        },
    ]


def build_surface_snapshot(inputs: dict[str, str]) -> list[dict[str, object]]:
    snapshots = [
        {
            "path": "README.md",
            "needles": ["layout-tightening and release-readiness pass", "manuscript-freeze candidacy", "does **not** claim"],
        },
        {
            "path": "STATUS.md",
            "needles": ["layout-tightening and release-readiness pass is now complete", "manuscript-freeze candidacy", "release_summary_draft.md"],
        },
        {
            "path": "docs/publication_record/README.md",
            "needles": ["release_summary_draft.md", "approved as the source"],
        },
        {
            "path": "docs/publication_record/release_summary_draft.md",
            "needles": [
                "This repository reproduces a narrow execution-substrate claim",
                "## Current paper-facing follow-up",
                "manuscript-freeze candidacy",
            ],
        },
        {
            "path": "docs/publication_record/manuscript_bundle_draft.md",
            "needles": ["## 1. Abstract", "## 10. Reproducibility Appendix", "later no-widening decision"],
        },
        {
            "path": "docs/publication_record/layout_decision_log.md",
            "needles": ["Release-summary reuse", "README-adjacent short updates"],
        },
        {
            "path": "docs/milestones/P5_paper_draft_assembly/status.md",
            "needles": ["`P5` acceptance is now satisfied", "release-readiness phase"],
        },
        {
            "path": "docs/milestones/P5_paper_draft_assembly/todo.md",
            "needles": ["callout-alignment pass", "layout/readiness milestone scaffold"],
        },
    ]
    rows: list[dict[str, object]] = []
    for row in snapshots:
        input_key = {
            "README.md": "readme_text",
            "STATUS.md": "status_text",
            "docs/publication_record/README.md": "publication_readme_text",
            "docs/publication_record/release_summary_draft.md": "release_summary_text",
            "docs/publication_record/manuscript_bundle_draft.md": "manuscript_text",
            "docs/publication_record/layout_decision_log.md": "layout_log_text",
            "docs/milestones/P5_paper_draft_assembly/status.md": "p5_status_text",
            "docs/milestones/P5_paper_draft_assembly/todo.md": "p5_todo_text",
        }[str(row["path"])]
        rows.append(
            {
                "path": row["path"],
                "matched_lines": extract_matching_lines(inputs[input_key], needles=list(row["needles"])),
            }
        )
    return rows


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "p6_complete_freeze_candidate_pending",
        "release_summary_role": "approved_downstream_short_update_source",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "start manuscript-freeze candidacy and release preflight while keeping current claim/artifact boundaries fixed"
            if not blocked_items
            else "resolve the blocked public-surface sync items before another outward wording update"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_sync_checklist(**inputs)
    surface_snapshot = build_surface_snapshot(inputs)
    summary = build_summary(checklist_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "p5_public_surface_sync_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "surface_snapshot.json",
        {
            "experiment": "p5_public_surface_sync_snapshot",
            "environment": environment.as_dict(),
            "rows": surface_snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p5_public_surface_sync",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/release_summary_draft.md",
                "docs/publication_record/manuscript_bundle_draft.md",
                "docs/publication_record/layout_decision_log.md",
                "docs/milestones/P5_paper_draft_assembly/status.md",
                "docs/milestones/P5_paper_draft_assembly/todo.md",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# P5 Public Surface Sync",
                "",
                "Machine-readable audit of whether the current public surface stays aligned with the",
                "completed `P6` layout/readiness state and the approved downstream release summary.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `surface_snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
