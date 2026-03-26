"""Export the post-P53/P54/P55/F38 archive-first freeze packet for H64."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet"
H63_SUMMARY_PATH = ROOT / "results" / "H63_post_p50_p51_p52_f38_archive_first_closeout_packet" / "summary.json"
P53_SUMMARY_PATH = ROOT / "results" / "P53_post_h63_paper_archive_claim_sync" / "summary.json"
P54_SUMMARY_PATH = ROOT / "results" / "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming" / "summary.json"
P55_SUMMARY_PATH = ROOT / "results" / "P55_post_h63_clean_descendant_promotion_prep" / "summary.json"
F38_SUMMARY_PATH = ROOT / "results" / "F38_post_h62_r63_dormant_eligibility_profile_dossier" / "summary.json"
R63_NAME = "r63_post_h62_coprocessor_eligibility_profile_gate"


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


def main() -> None:
    h63_summary = read_json(H63_SUMMARY_PATH)["summary"]
    p53_summary = read_json(P53_SUMMARY_PATH)["summary"]
    p54_summary = read_json(P54_SUMMARY_PATH)["summary"]
    p55_summary = read_json(P55_SUMMARY_PATH)["summary"]
    f38_summary = read_json(F38_SUMMARY_PATH)["summary"]

    prerequisites = [
        h63_summary["selected_outcome"] == "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant",
        p53_summary["selected_outcome"] == "paper_archive_review_surfaces_locked_to_h64_archive_first_freeze",
        p54_summary["selected_outcome"] == "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution",
        p55_summary["selected_outcome"] == "clean_descendant_promotion_prep_refreshed_for_h64_archive_first_freeze",
        f38_summary["selected_outcome"] == "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields",
    ]
    all_green = all(prerequisites)

    checklist_rows = [
        {
            "item_id": "h64_preserves_h63",
            "status": "pass" if prerequisites[0] else "blocked",
            "notes": "H63 remains the preserved prior active packet under H64.",
        },
        {
            "item_id": "h64_reads_p53",
            "status": "pass" if prerequisites[1] else "blocked",
            "notes": "Paper/archive claim surfaces must already be synchronized by P53.",
        },
        {
            "item_id": "h64_reads_p54",
            "status": "pass" if prerequisites[2] else "blocked",
            "notes": "Hygiene and artifact policy must already be synchronized by P54.",
        },
        {
            "item_id": "h64_reads_p55",
            "status": "pass" if prerequisites[3] else "blocked",
            "notes": "Promotion-prep and handoff surfaces must already be synchronized by P55.",
        },
        {
            "item_id": "h64_reads_f38",
            "status": "pass" if prerequisites[4] else "blocked",
            "notes": "The only future family must remain dormant and ineligible at F38.",
        },
        {
            "item_id": "h64_runtime_stays_closed",
            "status": "pass",
            "notes": "H64 does not authorize runtime; any future R63 remains non-runtime unless a later packet says otherwise.",
        },
    ]
    claim_packet = {
        "supports": [
            "H64 makes archive-first freeze the active repo route above the preserved H63 packet.",
            "H64 keeps archive/hygiene stop as the default downstream state.",
            "H64 keeps R63 dormant and non-runtime only rather than converting it into authorization.",
        ],
        "does_not_support": [
            "runtime reopening",
            "same-lane executor-value reopening",
            "integration through dirty root main",
        ],
        "distilled_result": {
            "active_stage": "h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "preserved_prior_active_packet": "h63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "current_paper_archive_claim_sync_wave": "p53_post_h63_paper_archive_claim_sync",
            "current_repo_hygiene_sidecar": "p54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
            "current_promotion_prep_wave": "p55_post_h63_clean_descendant_promotion_prep",
            "current_dormant_future_dossier": "f38_post_h62_r63_dormant_eligibility_profile_dossier",
            "default_downstream_lane": "archive_or_hygiene_stop",
            "conditional_downstream_lane": R63_NAME,
            "all_prerequisites_green": all_green,
            "runtime_authorization": "closed",
            "selected_outcome": "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant",
            "next_required_lane": "archive_or_hygiene_stop_with_only_optional_planning_only_r63_profile_spec",
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
        "rows": [
            {"field": "default_downstream_lane", "value": "archive_or_hygiene_stop"},
            {"field": "conditional_downstream_lane", "value": R63_NAME},
            {"field": "all_prerequisites_green", "value": all_green},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
