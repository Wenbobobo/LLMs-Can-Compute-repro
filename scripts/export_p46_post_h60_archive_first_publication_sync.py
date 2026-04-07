"""Export the post-H60 archive-first publication sync audit for P46."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P46_post_h60_archive_first_publication_sync"
H61_SUMMARY_PATH = ROOT / "results" / "H61_post_h60_archive_first_position_packet" / "summary.json"
F36_SUMMARY_PATH = ROOT / "results" / "F36_post_h60_conditional_compiled_online_reopen_qualification_bundle" / "summary.json"
AUDITED_FILE_REQUIREMENTS: dict[Path, list[str]] = {
    ROOT / "README.md": [
        "H61_post_h60_archive_first_position_packet",
        "P45_post_h60_clean_descendant_integration_readiness",
        "F36_post_h60_conditional_compiled_online_reopen_qualification_bundle",
        "P46_post_h60_archive_first_publication_sync",
    ],
    ROOT / "STATUS.md": [
        "archive_first_consolidation_becomes_default_posture",
        "planning_only_or_project_stop",
    ],
    ROOT / "docs" / "publication_record" / "README.md": [
        "H61_post_h60_archive_first_position_packet",
        "archive-first consolidation",
        "partial falsification",
    ],
    ROOT / "docs" / "publication_record" / "current_stage_driver.md": [
        "H61_post_h60_archive_first_position_packet",
        "archive-first consolidation",
    ],
    ROOT / "docs" / "publication_record" / "claim_evidence_table.md": [
        "executor-value partial falsification",
        "archive-first consolidation is now the default live posture",
    ],
    ROOT / "docs" / "publication_record" / "review_boundary_summary.md": [
        "same-lane executor-value reopen remains closed",
        "only compiled-online exact retrieval or attention-coprocessor route survives on paper",
    ],
    ROOT / "docs" / "publication_record" / "release_summary_draft.md": [
        "archive-first consolidation is now the default repo meaning",
        "narrow mechanistic reproduction plus executor-value partial falsification",
    ],
    ROOT / "docs" / "publication_record" / "conditional_reopen_protocol.md": [
        "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route",
        "qualification-only dossier",
        "no runtime lane opens from this protocol by itself",
    ],
    ROOT / "docs" / "publication_record" / "paper_bundle_status.md": [
        "H61_post_h60_archive_first_position_packet",
        "archive-first partial-falsification framing",
    ],
    ROOT / "docs" / "publication_record" / "archival_repro_manifest.md": [
        "export_h61_post_h60_archive_first_position_packet.py",
        "export_p45_post_h60_clean_descendant_integration_readiness.py",
        "export_f36_post_h60_conditional_compiled_online_reopen_qualification_bundle.py",
        "export_p46_post_h60_archive_first_publication_sync.py",
    ],
    ROOT / "docs" / "publication_record" / "submission_packet_index.md": [
        "../milestones/H61_post_h60_archive_first_position_packet/",
        "../milestones/P45_post_h60_clean_descendant_integration_readiness/",
        "../milestones/F36_post_h60_conditional_compiled_online_reopen_qualification_bundle/",
        "../milestones/P46_post_h60_archive_first_publication_sync/",
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
    h61_summary = read_json(H61_SUMMARY_PATH)["summary"]
    f36_summary = read_json(F36_SUMMARY_PATH)["summary"]
    if h61_summary["selected_outcome"] != "archive_first_consolidation_becomes_default_posture":
        raise RuntimeError("P46 expects the landed H61 active packet.")
    if f36_summary["selected_outcome"] != "compiled_online_route_qualified_on_paper_only_with_strict_preruntime_gates":
        raise RuntimeError("P46 expects the landed F36 qualification bundle.")

    surface_rows = audit_surfaces()
    checklist_rows = [
        {
            "item_id": "p46_reads_h61",
            "status": "pass",
            "notes": "P46 locks outward wording only after H61 makes archive-first the live posture.",
        },
        {
            "item_id": "p46_reads_f36",
            "status": "pass",
            "notes": "Future-route wording should match the F36 qualification-only bundle.",
        },
        *[
            {
                "item_id": f"p46_surface_{index:02d}",
                "status": row["status"],
                "notes": f"{row['path']} contains the required archive-first lock phrases.",
            }
            for index, row in enumerate(surface_rows, start=1)
        ],
    ]
    claim_packet = {
        "supports": [
            "P46 locks outward wording to archive-first consolidation plus executor-value partial falsification framing.",
            "P46 keeps the one future route qualification-only and later-explicit only.",
            "P46 removes stale multi-patch reopen wording from the live control surface.",
        ],
        "does_not_support": [
            "broad headline reproduction claims",
            "same-lane executor-value reopening",
            "runtime authorization by publication wording alone",
        ],
        "distilled_result": {
            "active_stage_at_lock_time": "h61_post_h60_archive_first_position_packet",
            "current_publication_sync_wave": "p46_post_h60_archive_first_publication_sync",
            "current_reopen_qualification_bundle": "f36_post_h60_conditional_compiled_online_reopen_qualification_bundle",
            "selected_outcome": "publication_surfaces_locked_to_archive_first_partial_falsification_state",
            "current_downstream_scientific_lane": "planning_only_or_project_stop",
            "audited_file_count": len(surface_rows),
            "locked_file_count": sum(row["status"] == "pass" for row in surface_rows),
            "claim_lock_assertions": [
                "narrow mechanistic reproduction plus executor-value partial falsification",
                "archive-first consolidation is the default live posture",
                "same-lane executor-value reopen remains closed",
                "only compiled-online exact retrieval or attention-coprocessor route survives on paper",
                "no runtime lane opens from publication wording",
            ],
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
    snapshot = {
        "rows": surface_rows,
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
