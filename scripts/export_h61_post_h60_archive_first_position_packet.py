"""Export the post-H60 archive-first position packet for H61."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H61_post_h60_archive_first_position_packet"
H60_SUMMARY_PATH = ROOT / "results" / "H60_post_f34_next_lane_decision_packet" / "summary.json"
P45_SUMMARY_PATH = ROOT / "results" / "P45_post_h60_clean_descendant_integration_readiness" / "summary.json"
F36_SUMMARY_PATH = ROOT / "results" / "F36_post_h60_conditional_compiled_online_reopen_qualification_bundle" / "summary.json"
F35_SUMMARY_PATH = ROOT / "results" / "F35_post_h59_far_future_model_and_weights_horizon_log" / "summary.json"
SELECTED_OUTCOME = "archive_first_consolidation_becomes_default_posture"


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
    h60_summary = read_json(H60_SUMMARY_PATH)["summary"]
    p45_summary = read_json(P45_SUMMARY_PATH)["summary"]
    f36_summary = read_json(F36_SUMMARY_PATH)["summary"]
    f35_summary = read_json(F35_SUMMARY_PATH)["summary"]
    if h60_summary["selected_outcome"] != "remain_planning_only_and_prepare_stop_or_archive":
        raise RuntimeError("H61 expects the landed H60 packet.")
    if p45_summary["merge_posture"] != "clean_descendant_only_never_dirty_root_main":
        raise RuntimeError("H61 expects the landed P45 hygiene posture.")
    if f36_summary["selected_outcome"] != "compiled_online_route_qualified_on_paper_only_with_strict_preruntime_gates":
        raise RuntimeError("H61 expects the landed F36 qualification bundle.")
    if f35_summary["current_execution_candidate_count"] != 0:
        raise RuntimeError("H61 expects F35 to remain far-future only.")

    checklist_rows = [
        {
            "item_id": "h61_preserves_h60",
            "status": "pass",
            "notes": "H60 stays the preserved prior active packet.",
        },
        {
            "item_id": "h61_reads_p45_clean_descendant_posture",
            "status": "pass",
            "notes": "Archive-first stays on a clean descendant line rather than routing through dirty root main.",
        },
        {
            "item_id": "h61_reads_f36_qualification_only_bundle",
            "status": "pass",
            "notes": "The one future route remains paper-only and runtime-closed.",
        },
        {
            "item_id": "h61_reads_f35_far_future_storage",
            "status": "pass",
            "notes": "Far-future model and weights routes remain stored but inactive.",
        },
        {
            "item_id": "h61_keeps_runtime_lane_closed",
            "status": "pass",
            "notes": "Archive-first does not open runtime execution.",
        },
    ]
    claim_packet = {
        "supports": [
            "H61 makes archive-first consolidation the default live posture of the repo.",
            "H61 preserves H60 as the prior active packet instead of treating it as superseded noise.",
            "H61 keeps one conditional future route on paper only while preserving planning-only / stop as the downstream lane.",
        ],
        "does_not_support": [
            "runtime authorization",
            "same-lane executor-value reopening",
            "merge through dirty root main",
        ],
        "distilled_result": {
            "active_stage": "h61_post_h60_archive_first_position_packet",
            "preserved_prior_active_packet": "h60_post_f34_next_lane_decision_packet",
            "preserved_prior_reproduction_gap_packet": "h59_post_h58_reproduction_gap_decision_packet",
            "preserved_prior_value_negative_closeout": "h58_post_r62_origin_value_boundary_closeout_packet",
            "preserved_prior_closeout_certification": "f32_post_h58_closeout_certification_bundle",
            "current_reopen_qualification_bundle": "f36_post_h60_conditional_compiled_online_reopen_qualification_bundle",
            "current_repo_hygiene_sidecar": "p45_post_h60_clean_descendant_integration_readiness",
            "current_far_future_horizon_log": "f35_post_h59_far_future_model_and_weights_horizon_log",
            "preserved_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_reopen_family_on_paper": f36_summary["admissible_reopen_family"],
            "selected_outcome": SELECTED_OUTCOME,
            "current_downstream_scientific_lane": "planning_only_or_project_stop",
            "later_authorization_gate": "no_runtime_lane_open_until_later_explicit_authorization",
            "project_default_fallback": "archive_first_then_stop_or_later_explicit_authorization",
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
            {"source": "h60", "selected_outcome": h60_summary["selected_outcome"]},
            {"source": "p45", "merge_posture": p45_summary["merge_posture"]},
            {"source": "f36", "selected_outcome": f36_summary["selected_outcome"]},
            {"source": "f35", "current_execution_candidate_count": f35_summary["current_execution_candidate_count"]},
            {"source": "h61", "selected_outcome": SELECTED_OUTCOME},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
