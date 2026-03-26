"""Export the post-H59 far-future model/weights horizon log for F35."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F35_post_h59_far_future_model_and_weights_horizon_log"
H59_SUMMARY_PATH = ROOT / "results" / "H59_post_h58_reproduction_gap_decision_packet" / "summary.json"
F34_SUMMARY_PATH = ROOT / "results" / "F34_post_h59_compiled_online_retrieval_reopen_screen" / "summary.json"


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
    h59_summary = read_json(H59_SUMMARY_PATH)["summary"]
    f34_summary = read_json(F34_SUMMARY_PATH)["summary"]
    if h59_summary["selected_outcome"] != "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen":
        raise RuntimeError("F35 expects the landed H59 packet.")
    if f34_summary["later_authorization_gate"] != "no_runtime_lane_open_until_later_explicit_authorization":
        raise RuntimeError("F35 expects the landed F34 no-runtime-lane rule.")

    checklist_rows = [
        {
            "item_id": "f35_starts_after_h59",
            "status": "pass",
            "notes": "F35 is storage only after the landed H59 closeout state.",
        },
        {
            "item_id": "f35_reads_f34_no_runtime_lane_rule",
            "status": "pass",
            "notes": "F35 inherits the same no-runtime-lane-open posture as F34/H60.",
        },
        {
            "item_id": "f35_high_cost_model_route_is_far_future_only",
            "status": "pass",
            "notes": "The model route is stored only as a farther-future idea.",
        },
        {
            "item_id": "f35_programs_into_weights_route_is_far_future_only",
            "status": "pass",
            "notes": "The programs-into-weights route is stored only as a farther-future idea.",
        },
    ]
    claim_packet = {
        "supports": [
            "F35 stores farther-future model and weights routes so they are not forgotten.",
            "F35 keeps those routes out of the current F34 reopen screen.",
            "F35 preserves the current planning-only / archive / stop posture.",
        ],
        "does_not_support": [
            "current execution authorization",
            "automatic reopening of F27, R53, or R54",
            "treating far-future storage as evidence",
        ],
        "distilled_result": {
            "active_stage_at_log_time": "h59_post_h58_reproduction_gap_decision_packet",
            "horizon_log": "f35_post_h59_far_future_model_and_weights_horizon_log",
            "selected_outcome": "far_future_routes_logged_without_current_authorization",
            "high_cost_model_route_status": "high_cost_model_route_far_future_only",
            "programs_into_weights_route_status": "programs_into_weights_route_far_future_only",
            "current_execution_candidate_count": 0,
            "current_downstream_scientific_lane": "planning_only_or_project_stop",
            "later_authorization_gate": "no_runtime_lane_open_until_later_explicit_authorization",
            "next_required_lane": "later_explicit_authorization_or_archive",
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
            {"route_family": "high_cost_model_route", "status": "far_future_only"},
            {"route_family": "programs_into_weights_route", "status": "far_future_only"},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
