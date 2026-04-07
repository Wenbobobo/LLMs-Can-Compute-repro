"""Export the post-H62 paper-facing partial-falsification package for P51."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P51_post_h62_paper_facing_partial_falsification_package"
H62_SUMMARY_PATH = ROOT / "results" / "H62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet" / "summary.json"
P50_SUMMARY_PATH = ROOT / "results" / "P50_post_h62_archive_first_control_sync" / "summary.json"
F37_SUMMARY_PATH = ROOT / "results" / "F37_post_h61_compiled_online_coprocessor_reauthorization_bundle" / "summary.json"
AUDITED_FILE_REQUIREMENTS: dict[Path, list[str]] = {
    ROOT / "docs" / "publication_record" / "paper_bundle_status.md": [
        "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
        "archive-first partial-falsification closeout framing",
        "F38_post_h62_r63_dormant_eligibility_profile_dossier",
    ],
    ROOT / "docs" / "publication_record" / "review_boundary_summary.md": [
        "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
        "dormant no-go dossier at `F38`",
        "executor-value on the strongest justified lane is closed negative",
    ],
    ROOT / "docs" / "publication_record" / "release_summary_draft.md": [
        "archive-first closeout is now the default repo meaning",
        "R63 remains dormant",
        "paper-facing partial falsification",
    ],
    ROOT / "docs" / "publication_record" / "claim_ladder.md": [
        "P51 paper-facing partial-falsification package",
        "F38 dormant R63 eligibility dossier",
        "H63 archive-first closeout packet",
    ],
    ROOT / "docs" / "publication_record" / "claim_evidence_table.md": [
        "H63 is now the current active docs-only packet",
        "F38 is the current dormant future dossier",
        "P51 is the current paper-facing partial-falsification package",
    ],
    ROOT / "docs" / "publication_record" / "archival_repro_manifest.md": [
        "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
        "scripts/export_p51_post_h62_paper_facing_partial_falsification_package.py",
        "scripts/export_f38_post_h62_r63_dormant_eligibility_profile_dossier.py",
    ],
    ROOT / "docs" / "publication_record" / "submission_packet_index.md": [
        "../milestones/P51_post_h62_paper_facing_partial_falsification_package/",
        "../milestones/F38_post_h62_r63_dormant_eligibility_profile_dossier/",
        "../milestones/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/",
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
    p50_summary = read_json(P50_SUMMARY_PATH)["summary"]
    f37_summary = read_json(F37_SUMMARY_PATH)["summary"]
    if h62_summary["default_downstream_lane"] != "archive_or_hygiene_stop":
        raise RuntimeError("P51 expects H62 to keep archive/hygiene stop as the default downstream state.")
    if p50_summary["selected_outcome"] != "control_surfaces_locked_to_post_h62_archive_first_closeout":
        raise RuntimeError("P51 expects the landed P50 control sync wave.")
    if f37_summary["runtime_authorization"] != "closed":
        raise RuntimeError("P51 expects F37 to keep runtime closed.")

    surface_rows = audit_surfaces()
    checklist_rows = [
        {
            "item_id": "p51_reads_h62",
            "status": "pass",
            "notes": "P51 packages the paper-facing state only after H62 locks archive-first as the default lane.",
        },
        {
            "item_id": "p51_reads_p50",
            "status": "pass",
            "notes": "P51 assumes the control surfaces are already synchronized by P50.",
        },
        {
            "item_id": "p51_reads_f37",
            "status": "pass",
            "notes": "Future-route wording must stay inside the strict F37 non-runtime contract.",
        },
        *[
            {
                "item_id": f"p51_surface_{index:02d}",
                "status": row["status"],
                "notes": f"{row['path']} contains the required paper-facing closeout wording.",
            }
            for index, row in enumerate(surface_rows, start=1)
        ],
    ]
    claim_packet = {
        "supports": [
            "P51 packages archive-first partial falsification as the strongest honest paper-facing reading.",
            "P51 keeps the narrow positive mechanism result explicit while keeping the broader headline negative explicit.",
            "P51 keeps F38 dormant and non-runtime rather than hinting at a reopened science lane.",
        ],
        "does_not_support": [
            "runtime-superiority claims",
            "broad Wasm or arbitrary C claims",
            "advisory material as evidence",
        ],
        "distilled_result": {
            "active_stage_at_package_time": "h62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet",
            "current_paper_facing_package_wave": "p51_post_h62_paper_facing_partial_falsification_package",
            "preserved_prior_publication_sync_wave": "p46_post_h60_archive_first_publication_sync",
            "selected_outcome": "paper_surfaces_locked_to_archive_first_partial_falsification_closeout",
            "audited_file_count": len(surface_rows),
            "locked_file_count": sum(row["status"] == "pass" for row in surface_rows),
            "future_route_posture": "dormant_non_runtime_only",
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
