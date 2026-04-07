"""Export the post-H58 reproduction-gap decision packet for H59."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H59_post_h58_reproduction_gap_decision_packet"
H58_SUMMARY_PATH = ROOT / "results" / "H58_post_r62_origin_value_boundary_closeout_packet" / "summary.json"
F32_SUMMARY_PATH = ROOT / "results" / "F32_post_h58_closeout_certification_bundle" / "summary.json"


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
    h58_summary = read_json(H58_SUMMARY_PATH)["summary"]
    f32_summary = read_json(F32_SUMMARY_PATH)["summary"]
    if h58_summary["selected_outcome"] != "stop_as_mechanism_supported_but_no_bounded_executor_value":
        raise RuntimeError("H59 expects the landed H58 closeout outcome.")
    if f32_summary["certified_stop"] != "same_lane_reopen_not_admissible_without_new_cost_structure":
        raise RuntimeError("H59 expects the F32 certified stop boundary.")

    selected_outcome = "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen"
    checklist_rows = [
        {
            "item_id": "h59_reads_h58_and_f32",
            "status": "pass",
            "notes": "H59 depends on both the landed H58 closeout and the F32 certification.",
        },
        {
            "item_id": "h59_preserves_h43_as_paper_grade_endpoint",
            "status": "pass",
            "notes": "The useful-case exact endpoint remains H43 rather than being erased by later negative lanes.",
        },
        {
            "item_id": "h59_states_reproduction_gap_explicitly",
            "status": "pass",
            "notes": "The current branch is honest about the remaining gap to the broad public headline.",
        },
        {
            "item_id": "h59_requires_different_cost_structure_for_reopen",
            "status": "pass",
            "notes": "Later work must change the cost model materially or stop.",
        },
    ]
    claim_packet = {
        "supports": [
            "Narrow append-only retrieval-backed execution survives as a real positive result.",
            "The current executor-value lane is disconfirmed on the strongest currently justified route.",
            "Future work should be planning-only unless a materially different cost structure is named.",
        ],
        "does_not_support": [
            "broad 'LLMs are computers' claims",
            "automatic reopening of the same runtime lane",
            "treating value-negative native useful-kernel evidence as a partial positive systems result",
        ],
        "distilled_result": {
            "active_stage": "h59_post_h58_reproduction_gap_decision_packet",
            "preserved_prior_docs_only_closeout": "h58_post_r62_origin_value_boundary_closeout_packet",
            "preserved_prior_closeout_certification": "f32_post_h58_closeout_certification_bundle",
            "current_planning_bundle": "f33_post_h59_different_cost_structure_reopen_bundle",
            "current_low_priority_wave": "p42_post_h59_gptpro_reinterview_packet",
            "preserved_prior_publication_sync": "p41_post_h58_publication_and_archive_sync",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": selected_outcome,
            "impactful_reproduction_distance": "broad_headline_not_reproduced_current_lane_value_disconfirmed",
            "current_downstream_scientific_lane": "planning_only_or_project_stop",
            "blocked_future_storage": [
                "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
                "r53_origin_transformed_executor_entry_gate",
                "r54_origin_trainable_executor_comparator_gate",
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
        "rows": [
            {"source": "h58", "selected_outcome": h58_summary["selected_outcome"]},
            {"source": "f32", "certified_stop": f32_summary["certified_stop"]},
            {"source": "h59", "selected_outcome": selected_outcome},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
