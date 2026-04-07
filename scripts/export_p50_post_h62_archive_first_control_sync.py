"""Export the post-H62 archive-first control sync sidecar for P50."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P50_post_h62_archive_first_control_sync"
H62_SUMMARY_PATH = ROOT / "results" / "H62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet" / "summary.json"
AUDITED_FILE_REQUIREMENTS: dict[Path, list[str]] = {
    ROOT / "README.md": [
        "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
        "P50_post_h62_archive_first_control_sync",
        "archive-first closeout",
    ],
    ROOT / "STATUS.md": [
        "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
        "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant",
        "P50_post_h62_archive_first_control_sync",
    ],
    ROOT / "docs" / "publication_record" / "README.md": [
        "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
        "P50_post_h62_archive_first_control_sync",
        "archive-first closeout",
    ],
    ROOT / "docs" / "publication_record" / "current_stage_driver.md": [
        "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
        "P50_post_h62_archive_first_control_sync",
        "archive-first closeout is now the active route",
    ],
    ROOT / "tmp" / "active_wave_plan.md": [
        "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
        "P50_post_h62_archive_first_control_sync",
        "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant",
    ],
}


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


def audit_surfaces() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path, patterns in AUDITED_FILE_REQUIREMENTS.items():
        text = path.read_text(encoding="utf-8")
        missing = [pattern for pattern in patterns if pattern not in text]
        rows.append(
            {
                "path": display_path(path),
                "status": "pass" if not missing else "blocked",
                "missing_patterns": missing,
            }
        )
    return rows


def main() -> None:
    h62_summary = read_json(H62_SUMMARY_PATH)["summary"]
    if h62_summary["selected_outcome"] != "hygiene_first_scope_decision_keeps_archive_default_and_limits_any_reopen_to_r63_profile_gate":
        raise RuntimeError("P50 expects the landed H62 scope decision packet.")

    surface_rows = audit_surfaces()
    checklist_rows = [
        {
            "item_id": "p50_reads_h62",
            "status": "pass",
            "notes": "P50 starts from the landed H62 archive-default scope decision.",
        },
        *[
            {
                "item_id": f"p50_surface_{index:02d}",
                "status": row["status"],
                "notes": f"{row['path']} contains the required archive-first closeout control wording.",
            }
            for index, row in enumerate(surface_rows, start=1)
        ],
    ]
    claim_packet = {
        "supports": [
            "P50 locks top-level control surfaces to the archive-first closeout posture.",
            "P50 prepares H63 without reopening runtime or same-lane executor-value work.",
            "P50 keeps R63 dormant and non-runtime only on control surfaces.",
        ],
        "does_not_support": [
            "runtime authorization",
            "same-lane executor-value reopening",
            "dirty-root integration",
        ],
        "distilled_result": {
            "active_stage_at_sync_time": "h62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet",
            "current_control_sync_wave": "p50_post_h62_archive_first_control_sync",
            "preserved_prior_active_packet": "h62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet",
            "selected_outcome": "control_surfaces_locked_to_post_h62_archive_first_closeout",
            "current_downstream_scientific_lane": "archive_or_hygiene_stop",
            "audited_file_count": len(surface_rows),
            "locked_file_count": sum(row["status"] == "pass" for row in surface_rows),
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
    snapshot = {"rows": surface_rows}

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
