"""Export the post-P47/P48/P49/F37 hygiene-first scope decision packet for H62."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet"
H61_SUMMARY_PATH = ROOT / "results" / "H61_post_h60_archive_first_position_packet" / "summary.json"
P47_SUMMARY_PATH = ROOT / "results" / "P47_post_h61_root_quarantine_and_main_merge_planning" / "summary.json"
P48_SUMMARY_PATH = ROOT / "results" / "P48_post_h61_clean_descendant_promotion_prep" / "summary.json"
P49_SUMMARY_PATH = ROOT / "results" / "P49_post_h61_origin_advisory_sync" / "summary.json"
F37_SUMMARY_PATH = ROOT / "results" / "F37_post_h61_compiled_online_coprocessor_reauthorization_bundle" / "summary.json"
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
    h61_summary = read_json(H61_SUMMARY_PATH)["summary"]
    p47_summary = read_json(P47_SUMMARY_PATH)["summary"]
    p48_summary = read_json(P48_SUMMARY_PATH)["summary"]
    p49_summary = read_json(P49_SUMMARY_PATH)["summary"]
    f37_summary = read_json(F37_SUMMARY_PATH)["summary"]

    prerequisites = [
        h61_summary["selected_outcome"] == "archive_first_consolidation_becomes_default_posture",
        p47_summary["selected_outcome"] == "quarantine_root_and_plan_main_merge_only",
        p48_summary["selected_outcome"] == "clean_descendant_ready_for_later_explicit_promotion",
        p49_summary["selected_outcome"] == "advisory_origin_materials_available_in_clean_line",
        f37_summary["selected_outcome"] == "one_compiled_online_coprocessor_route_specified_but_runtime_closed",
    ]
    all_green = all(prerequisites)

    checklist_rows = [
        {
            "item_id": "h62_preserves_h61",
            "status": "pass" if prerequisites[0] else "blocked",
            "notes": "H61 remains the preserved prior active packet.",
        },
        {
            "item_id": "h62_reads_p47",
            "status": "pass" if prerequisites[1] else "blocked",
            "notes": "The parked root checkout must remain quarantined.",
        },
        {
            "item_id": "h62_reads_p48",
            "status": "pass" if prerequisites[2] else "blocked",
            "notes": "Clean-descendant promotion prep must be explicit before later integration planning.",
        },
        {
            "item_id": "h62_reads_p49",
            "status": "pass" if prerequisites[3] else "blocked",
            "notes": "Advisory materials must be available in the clean line before later planning relies on them.",
        },
        {
            "item_id": "h62_reads_f37",
            "status": "pass" if prerequisites[4] else "blocked",
            "notes": "Only the narrow F37 coprocessor route may survive into later scope planning.",
        },
        {
            "item_id": "h62_runtime_stays_closed",
            "status": "pass",
            "notes": "H62 does not open runtime; any later R63 gate remains non-runtime.",
        },
    ]
    claim_packet = {
        "supports": [
            "H62 makes hygiene-first the gating posture for any later scientific follow-up.",
            "H62 keeps archive/hygiene stop as the default downstream state.",
            "H62 limits any later scientific continuation to one conditional non-runtime R63 profile gate.",
        ],
        "does_not_support": [
            "runtime reopening",
            "merge-main by momentum",
            "broad scientific widening beyond the F37 route",
        ],
        "distilled_result": {
            "active_stage": "h62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet",
            "preserved_prior_active_packet": "h61_post_h60_archive_first_position_packet",
            "current_root_quarantine_planning": "p47_post_h61_root_quarantine_and_main_merge_planning",
            "current_clean_descendant_promotion_prep": "p48_post_h61_clean_descendant_promotion_prep",
            "current_origin_advisory_sync": "p49_post_h61_origin_advisory_sync",
            "current_reauthorization_bundle": "f37_post_h61_compiled_online_coprocessor_reauthorization_bundle",
            "default_downstream_lane": "archive_or_hygiene_stop",
            "conditional_downstream_lane": R63_NAME,
            "all_prerequisites_green": all_green,
            "runtime_authorization": "closed",
            "selected_outcome": "hygiene_first_scope_decision_keeps_archive_default_and_limits_any_reopen_to_r63_profile_gate",
            "next_required_lane": "archive_or_hygiene_stop_unless_later_explicit_r63_profile_authorization",
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
