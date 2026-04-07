"""Export the post-P50/P51/P52/F38 archive-first closeout packet for H63."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H63_post_p50_p51_p52_f38_archive_first_closeout_packet"
H62_SUMMARY_PATH = ROOT / "results" / "H62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet" / "summary.json"
P50_SUMMARY_PATH = ROOT / "results" / "P50_post_h62_archive_first_control_sync" / "summary.json"
P51_SUMMARY_PATH = ROOT / "results" / "P51_post_h62_paper_facing_partial_falsification_package" / "summary.json"
P52_SUMMARY_PATH = ROOT / "results" / "P52_post_h62_clean_descendant_hygiene_and_merge_prep" / "summary.json"
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
    h62_summary = read_json(H62_SUMMARY_PATH)["summary"]
    p50_summary = read_json(P50_SUMMARY_PATH)["summary"]
    p51_summary = read_json(P51_SUMMARY_PATH)["summary"]
    p52_summary = read_json(P52_SUMMARY_PATH)["summary"]
    f38_summary = read_json(F38_SUMMARY_PATH)["summary"]

    prerequisites = [
        h62_summary["selected_outcome"] == "hygiene_first_scope_decision_keeps_archive_default_and_limits_any_reopen_to_r63_profile_gate",
        p50_summary["selected_outcome"] == "control_surfaces_locked_to_post_h62_archive_first_closeout",
        p51_summary["selected_outcome"] == "paper_surfaces_locked_to_archive_first_partial_falsification_closeout",
        p52_summary["selected_outcome"] == "clean_descendant_hygiene_and_merge_prep_locked_without_dirty_root_merge",
        f38_summary["selected_outcome"] == "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields",
    ]
    all_green = all(prerequisites)

    checklist_rows = [
        {
            "item_id": "h63_preserves_h62",
            "status": "pass" if prerequisites[0] else "blocked",
            "notes": "H62 remains the preserved prior active packet under H63.",
        },
        {
            "item_id": "h63_reads_p50",
            "status": "pass" if prerequisites[1] else "blocked",
            "notes": "Control surfaces must already be synchronized by P50.",
        },
        {
            "item_id": "h63_reads_p51",
            "status": "pass" if prerequisites[2] else "blocked",
            "notes": "Paper-facing packaging must already be synchronized by P51.",
        },
        {
            "item_id": "h63_reads_p52",
            "status": "pass" if prerequisites[3] else "blocked",
            "notes": "Hygiene and merge-prep posture must already be synchronized by P52.",
        },
        {
            "item_id": "h63_reads_f38",
            "status": "pass" if prerequisites[4] else "blocked",
            "notes": "The only future family must remain dormant and ineligible at F38.",
        },
        {
            "item_id": "h63_runtime_stays_closed",
            "status": "pass",
            "notes": "H63 does not authorize runtime; any future R63 remains non-runtime unless a later packet says otherwise.",
        },
    ]
    claim_packet = {
        "supports": [
            "H63 makes archive-first closeout the active repo route above the preserved H62 packet.",
            "H63 keeps archive/hygiene stop as the default downstream state.",
            "H63 keeps R63 dormant and non-runtime only rather than converting it into authorization.",
        ],
        "does_not_support": [
            "runtime reopening",
            "same-lane executor-value reopening",
            "integration through dirty root main",
        ],
        "distilled_result": {
            "active_stage": "h63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "preserved_prior_active_packet": "h62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet",
            "current_control_sync_wave": "p50_post_h62_archive_first_control_sync",
            "current_paper_facing_package_wave": "p51_post_h62_paper_facing_partial_falsification_package",
            "current_repo_hygiene_sidecar": "p52_post_h62_clean_descendant_hygiene_and_merge_prep",
            "current_dormant_future_dossier": "f38_post_h62_r63_dormant_eligibility_profile_dossier",
            "default_downstream_lane": "archive_or_hygiene_stop",
            "conditional_downstream_lane": R63_NAME,
            "all_prerequisites_green": all_green,
            "runtime_authorization": "closed",
            "selected_outcome": "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant",
            "next_required_lane": "archive_or_hygiene_stop_with_only_dormant_r63_reassessment_on_paper",
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
