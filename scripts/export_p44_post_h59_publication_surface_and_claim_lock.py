"""Export the post-H59 publication-surface and claim-lock audit for P44."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P44_post_h59_publication_surface_and_claim_lock"
H60_SUMMARY_PATH = ROOT / "results" / "H60_post_f34_next_lane_decision_packet" / "summary.json"
F34_SUMMARY_PATH = ROOT / "results" / "F34_post_h59_compiled_online_retrieval_reopen_screen" / "summary.json"
AUDITED_FILE_REQUIREMENTS: dict[Path, list[str]] = {
    ROOT / "README.md": [
        "H60_post_f34_next_lane_decision_packet",
        "F34_post_h59_compiled_online_retrieval_reopen_screen",
        "planning_only_or_project_stop",
    ],
    ROOT / "STATUS.md": [
        "remain_planning_only_and_prepare_stop_or_archive",
        "P44_post_h59_publication_surface_and_claim_lock",
    ],
    ROOT / "docs" / "publication_record" / "README.md": [
        "H60_post_f34_next_lane_decision_packet",
        "P44_post_h59_publication_surface_and_claim_lock",
    ],
    ROOT / "docs" / "publication_record" / "current_stage_driver.md": [
        "H60_post_f34_next_lane_decision_packet",
        "no_runtime_lane_open_until_later_explicit_authorization",
    ],
    ROOT / "docs" / "publication_record" / "claim_evidence_table.md": [
        "narrow positive mechanism result survives",
        "broad headline reproduction did not land",
    ],
    ROOT / "docs" / "publication_record" / "review_boundary_summary.md": [
        "same-lane executor-value microvariants remain inadmissible",
        "compiled-online exact retrieval or attention-coprocessor route remains conditional only",
    ],
    ROOT / "docs" / "publication_record" / "release_summary_draft.md": [
        "default outcome remains planning-only, archive, or explicit stop",
    ],
    ROOT / "docs" / "publication_record" / "release_preflight_checklist.md": [
        "results/H60_post_f34_next_lane_decision_packet/summary.json",
        "results/P44_post_h59_publication_surface_and_claim_lock/summary.json",
    ],
    ROOT / "docs" / "publication_record" / "release_candidate_checklist.md": [
        "results/H60_post_f34_next_lane_decision_packet/summary.json",
        "results/F35_post_h59_far_future_model_and_weights_horizon_log/summary.json",
    ],
    ROOT / "docs" / "publication_record" / "paper_bundle_status.md": [
        "H60_post_f34_next_lane_decision_packet",
        "F35_post_h59_far_future_model_and_weights_horizon_log",
    ],
    ROOT / "docs" / "publication_record" / "archival_repro_manifest.md": [
        "export_h60_post_f34_next_lane_decision_packet.py",
        "export_p44_post_h59_publication_surface_and_claim_lock.py",
    ],
    ROOT / "docs" / "publication_record" / "submission_packet_index.md": [
        "../milestones/H60_post_f34_next_lane_decision_packet/",
        "../milestones/P44_post_h59_publication_surface_and_claim_lock/",
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
    h60_summary = read_json(H60_SUMMARY_PATH)["summary"]
    f34_summary = read_json(F34_SUMMARY_PATH)["summary"]
    if h60_summary["selected_outcome"] != "remain_planning_only_and_prepare_stop_or_archive":
        raise RuntimeError("P44 expects the landed H60 decision.")
    if f34_summary["admissible_reopen_family"] != "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route":
        raise RuntimeError("P44 expects the landed F34 reopen screen.")

    surface_rows = audit_surfaces()
    checklist_rows = [
        {
            "item_id": "p44_reads_h60",
            "status": "pass",
            "notes": "P44 locks outward wording only after the H60 decision lands.",
        },
        {
            "item_id": "p44_reads_f34",
            "status": "pass",
            "notes": "The conditional future route wording should match F34.",
        },
        *[
            {
                "item_id": f"p44_surface_{index:02d}",
                "status": row["status"],
                "notes": f"{row['path']} contains the required lock phrases.",
            }
            for index, row in enumerate(surface_rows, start=1)
        ],
    ]
    claim_packet = {
        "supports": [
            "P44 locks outward wording to the post-H59 archive state and the H60 decision.",
            "P44 keeps the narrow positive explicit while keeping the broad headline negative explicit.",
            "P44 keeps the compiled-online route conditional-only and the default posture planning-only / archive / stop.",
        ],
        "does_not_support": [
            "broad headline reproduction claims",
            "same-lane executor-value reopening",
            "turning far-future ideas into current release wording",
        ],
        "distilled_result": {
            "active_stage_at_lock_time": "h60_post_f34_next_lane_decision_packet",
            "current_publication_lock_wave": "p44_post_h59_publication_surface_and_claim_lock",
            "current_planning_bundle": "f34_post_h59_compiled_online_retrieval_reopen_screen",
            "selected_outcome": "publication_surfaces_locked_to_post_h59_archive_state",
            "current_downstream_scientific_lane": "planning_only_or_project_stop",
            "audited_file_count": len(surface_rows),
            "locked_file_count": sum(row["status"] == "pass" for row in surface_rows),
            "claim_lock_assertions": [
                "narrow positive mechanism result survives",
                "broad headline reproduction did not land",
                "same-lane executor-value microvariants remain inadmissible",
                "compiled-online exact retrieval or attention-coprocessor route remains conditional only",
                "default outcome remains planning-only, archive, or explicit stop",
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
