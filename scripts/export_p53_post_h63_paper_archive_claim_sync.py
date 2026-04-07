"""Export the post-H63 paper/archive claim-sync wave for P53."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P53_post_h63_paper_archive_claim_sync"
H63_SUMMARY_PATH = ROOT / "results" / "H63_post_p50_p51_p52_f38_archive_first_closeout_packet" / "summary.json"
H58_SUMMARY_PATH = ROOT / "results" / "H58_post_r62_origin_value_boundary_closeout_packet" / "summary.json"
H43_SUMMARY_PATH = ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"
F38_SUMMARY_PATH = ROOT / "results" / "F38_post_h62_r63_dormant_eligibility_profile_dossier" / "summary.json"
AUDITED_FILE_REQUIREMENTS: dict[Path, list[str]] = {
    ROOT / "docs" / "publication_record" / "README.md": [
        "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
        "P53_post_h63_paper_archive_claim_sync",
        "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
        "P55_post_h63_clean_descendant_promotion_prep",
    ],
    ROOT / "docs" / "publication_record" / "paper_bundle_status.md": [
        "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
        "P53_post_h63_paper_archive_claim_sync",
        "P55_post_h63_clean_descendant_promotion_prep",
        "archive-first partial-falsification closeout framing",
    ],
    ROOT / "docs" / "publication_record" / "review_boundary_summary.md": [
        "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
        "executor-value on the strongest justified lane is closed negative",
        "dormant no-go dossier at `F38`",
    ],
    ROOT / "docs" / "publication_record" / "release_summary_draft.md": [
        "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
        "archive-first freeze is now the default repo meaning",
        "R63 remains dormant",
    ],
    ROOT / "docs" / "publication_record" / "claim_ladder.md": [
        "P53 paper/archive claim sync",
        "P54 Clean-descendant hygiene and artifact slimming",
        "P55 Clean-descendant promotion prep",
        "H64 archive-first freeze packet",
    ],
    ROOT / "docs" / "publication_record" / "claim_evidence_table.md": [
        "H64` is now the current active docs-only packet",
        "P53` is the current paper/archive claim-sync wave",
        "P54` is the current repo-hygiene sidecar",
    ],
    ROOT / "docs" / "publication_record" / "submission_candidate_criteria.md": [
        "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
        "P53_post_h63_paper_archive_claim_sync",
        "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
        "P55_post_h63_clean_descendant_promotion_prep",
    ],
    ROOT / "docs" / "publication_record" / "archival_repro_manifest.md": [
        "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
        "scripts/export_p53_post_h63_paper_archive_claim_sync.py",
        "scripts/export_h64_post_p53_p54_p55_f38_archive_first_freeze_packet.py",
    ],
    ROOT / "docs" / "publication_record" / "submission_packet_index.md": [
        "../milestones/P53_post_h63_paper_archive_claim_sync/",
        "../milestones/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/",
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
    h63_summary = read_json(H63_SUMMARY_PATH)["summary"]
    h58_summary = read_json(H58_SUMMARY_PATH)["summary"]
    h43_summary = read_json(H43_SUMMARY_PATH)["summary"]
    f38_summary = read_json(F38_SUMMARY_PATH)["summary"]
    if h63_summary["selected_outcome"] != "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant":
        raise RuntimeError("P53 expects the landed H63 closeout packet.")
    if h58_summary["selected_outcome"] != "stop_as_mechanism_supported_but_no_bounded_executor_value":
        raise RuntimeError("P53 expects H58 to remain the value-negative closeout.")
    if h43_summary["claim_d_state"] != "supported_here_narrowly":
        raise RuntimeError("P53 expects H43 to remain the paper-grade endpoint.")
    if f38_summary["runtime_authorization"] != "closed":
        raise RuntimeError("P53 expects F38 to keep runtime closed.")

    surface_rows = audit_surfaces()
    checklist_rows = [
        {
            "item_id": "p53_reads_h63",
            "status": "pass",
            "notes": "P53 packages the outward-facing state only after H63 lands.",
        },
        {
            "item_id": "p53_preserves_h58",
            "status": "pass",
            "notes": "P53 preserves H58 as the strongest executor-value closeout.",
        },
        {
            "item_id": "p53_preserves_h43",
            "status": "pass",
            "notes": "P53 preserves H43 as the paper-grade endpoint.",
        },
        {
            "item_id": "p53_preserves_f38",
            "status": "pass",
            "notes": "P53 keeps F38 dormant and non-runtime only.",
        },
        *[
            {
                "item_id": f"p53_surface_{index:02d}",
                "status": row["status"],
                "notes": f"{row['path']} contains the required H64 freeze wording.",
            }
            for index, row in enumerate(surface_rows, start=1)
        ],
    ]
    claim_packet = {
        "supports": [
            "P53 locks paper/archive/review/submission wording to the H64 freeze reading.",
            "P53 preserves narrow mechanism support while keeping the broad headline negative explicit.",
            "P53 preserves H58/H43 as the scientific interpretation anchors while keeping F38 dormant.",
        ],
        "does_not_support": [
            "runtime authorization",
            "same-lane executor-value replay",
            "advisory material as evidence",
        ],
        "distilled_result": {
            "active_stage_at_sync_time": "h63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "current_paper_archive_claim_sync_wave": "p53_post_h63_paper_archive_claim_sync",
            "preserved_prior_paper_archive_sync_wave": "p51_post_h62_paper_facing_partial_falsification_package",
            "selected_outcome": "paper_archive_review_surfaces_locked_to_h64_archive_first_freeze",
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
