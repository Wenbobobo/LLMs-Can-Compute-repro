"""Export the post-H59 different-cost-structure reopen bundle for F33."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F33_post_h59_different_cost_structure_reopen_bundle"
H59_SUMMARY_PATH = ROOT / "results" / "H59_post_h58_reproduction_gap_decision_packet" / "summary.json"
P42_SUMMARY_PATH = ROOT / "results" / "P42_post_h59_gptpro_reinterview_packet" / "summary.json"
CANDIDATE_ORDER = [
    "amortized_or_indexed_trace_retrieval_route",
    "low_level_compiled_or_external_coprocessor_route",
    "transformed_or_trained_executor_route_only_if_cost_model_changes_materially",
]


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
    p42_summary = read_json(P42_SUMMARY_PATH)["summary"]
    if h59_summary["selected_outcome"] != "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen":
        raise RuntimeError("F33 expects the landed H59 reproduction-gap decision.")
    if p42_summary["selected_outcome"] != "self_contained_gptpro_dossier_ready":
        raise RuntimeError("F33 expects the landed P42 GPTPro dossier packet.")

    checklist_rows = [
        {
            "item_id": "f33_starts_after_h59_gap_packet",
            "status": "pass",
            "notes": "F33 opens only after the reproduction-gap packet is explicit.",
        },
        {
            "item_id": "f33_requires_different_cost_structure",
            "status": "pass",
            "notes": "No same-lane reopen is admissible without a materially different cost structure.",
        },
        {
            "item_id": "f33_stores_planning_only_candidate_families",
            "status": "pass",
            "notes": "F33 stores future candidates but does not authorize runtime execution.",
        },
        {
            "item_id": "f33_keeps_project_stop_admissible",
            "status": "pass",
            "notes": "If no candidate survives scrutiny, project stop remains a valid outcome.",
        },
    ]
    claim_packet = {
        "supports": [
            "F33 is the current planning bundle after H59 and stores only admissible future reopen families.",
            "Any later reopen must change the cost structure materially rather than rephrasing R62.",
            "The GPTPro dossier is advisory input into candidate ranking, not scientific evidence.",
        ],
        "does_not_support": [
            "automatic runtime authorization",
            "automatic reopening of F27, R53, or R54",
            "treating current same-lane probing as unfinished business",
        ],
        "distilled_result": {
            "active_stage_at_planning_time": "h59_post_h58_reproduction_gap_decision_packet",
            "planning_bundle": "f33_post_h59_different_cost_structure_reopen_bundle",
            "current_low_priority_wave": "p42_post_h59_gptpro_reinterview_packet",
            "preserved_prior_closeout_certification": "f32_post_h58_closeout_certification_bundle",
            "preserved_prior_publication_sync": "p41_post_h58_publication_and_archive_sync",
            "admissible_reopen_requirement": "materially_different_cost_structure",
            "candidate_order": CANDIDATE_ORDER,
            "project_stop_rule": "stop_if_no_candidate_improves_cost_structure_on_useful_case",
            "next_required_lane": "planning_only_candidate_screen_or_project_stop",
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
            {"source": "h59", "selected_outcome": h59_summary["selected_outcome"]},
            {"source": "p42", "selected_outcome": p42_summary["selected_outcome"]},
            {"source": "f33", "candidate_order": CANDIDATE_ORDER},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
