"""Export the post-H61 Origin advisory sync wave for P49."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P49_post_h61_origin_advisory_sync"
H61_SUMMARY_PATH = ROOT / "results" / "H61_post_h60_archive_first_position_packet" / "summary.json"
P42_MILESTONE_README = ROOT / "docs" / "milestones" / "P42_post_h59_gptpro_reinterview_packet" / "README.md"
REQUIRED_FILES = [
    ROOT / "docs" / "Origin" / "Can LLMs Be Computers- - Percepta.md",
    ROOT / "docs" / "Origin" / "Discuss1.md",
    ROOT / "docs" / "Origin" / "Discuss2.md",
    ROOT / "docs" / "Origin" / "Discuss3Pro.md",
    ROOT / "docs" / "Origin" / "QA1.md",
    ROOT / "docs" / "Origin" / "QA2.md",
]


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def main() -> None:
    h61_summary = read_json(H61_SUMMARY_PATH)["summary"]
    if h61_summary["selected_outcome"] != "archive_first_consolidation_becomes_default_posture":
        raise RuntimeError("P49 expects the landed H61 packet.")
    if not P42_MILESTONE_README.exists():
        raise RuntimeError("P49 expects the preserved P42 advisory milestone scaffold.")

    rows = []
    for path in REQUIRED_FILES:
        rows.append(
            {
                "path": display_path(path),
                "status": "pass" if path.exists() else "blocked",
            }
        )

    checklist_rows = [
        {
            "item_id": "p49_reads_h61",
            "status": "pass",
            "notes": "P49 syncs advisory text after H61 lands the archive-first posture.",
        },
        {
            "item_id": "p49_preserves_p42_advisory_status",
            "status": "pass",
            "notes": "The preserved GPTPro dossier remains advisory-only rather than claim-bearing.",
        },
        *[
            {
                "item_id": f"p49_advisory_file_{index:02d}",
                "status": row["status"],
                "notes": f"{row['path']} should be available in the clean descendant line.",
            }
            for index, row in enumerate(rows, start=1)
        ],
    ]
    claim_packet = {
        "supports": [
            "P49 brings text-only Origin and GPTPro advisory materials into the clean line.",
            "P49 removes the need to consult the parked root checkout for these planning inputs.",
            "P49 keeps advisory material explicitly outside the evidence stack.",
        ],
        "does_not_support": [
            "turning advisory discussions into experimental evidence",
            "syncing larger raw assets in this packet",
            "reopening runtime by dossier drift",
        ],
        "distilled_result": {
            "active_stage_at_sync_time": "h61_post_h60_archive_first_position_packet",
            "current_origin_advisory_sync_wave": "p49_post_h61_origin_advisory_sync",
            "preserved_prior_advisory_wave": "p42_post_h59_gptpro_reinterview_packet",
            "synced_text_file_count": len(REQUIRED_FILES),
            "advisory_sync_state": "synced" if all(row["status"] == "pass" for row in rows) else "incomplete",
            "evidence_status": "advisory_only",
            "selected_outcome": "advisory_origin_materials_available_in_clean_line",
            "next_required_lane": "compiled_online_reauthorization_bundle_or_h62_scope_decision",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {"rows": rows}

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
