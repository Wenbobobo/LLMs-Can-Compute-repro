"""Export the post-H58 closeout certification bundle for F32."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F32_post_h58_closeout_certification_bundle"
H58_SUMMARY_PATH = ROOT / "results" / "H58_post_r62_origin_value_boundary_closeout_packet" / "summary.json"


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
    if h58_summary["selected_outcome"] != "stop_as_mechanism_supported_but_no_bounded_executor_value":
        raise RuntimeError("F32 expects the landed H58 value-negative closeout outcome.")

    checklist_rows = [
        {
            "item_id": "f32_reads_landed_h58_closeout",
            "status": "pass",
            "notes": "F32 starts only after the H58 closeout packet lands on the real R62 result.",
        },
        {
            "item_id": "f32_certifies_same_lane_stop",
            "status": "pass",
            "notes": "The current executor-value lane is certified as closed rather than parked.",
        },
        {
            "item_id": "f32_requires_different_cost_structure_for_reopen",
            "status": "pass",
            "notes": "Any future reopen must change the cost structure materially.",
        },
        {
            "item_id": "f32_keeps_blocked_future_storage_blocked",
            "status": "pass",
            "notes": "F27, R53, and R54 remain blocked by default after certification.",
        },
    ]
    claim_packet = {
        "supports": [
            "F32 certifies H58 as a real stop boundary for the current executor-value lane.",
            "The current branch still preserves narrow mechanism support and H43 as a paper-grade endpoint.",
            "Later work must route through a materially different cost structure or stop.",
        ],
        "does_not_support": [
            "same-lane executor-value probing by momentum",
            "automatic reopening of transformed or trainable entry",
            "automatic merge or promotion back into dirty root main",
        ],
        "distilled_result": {
            "active_stage_at_certification_time": "h58_post_r62_origin_value_boundary_closeout_packet",
            "planning_bundle": "f32_post_h58_closeout_certification_bundle",
            "certified_stop": "same_lane_reopen_not_admissible_without_new_cost_structure",
            "preserved_current_closeout": "h58_post_r62_origin_value_boundary_closeout_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "next_docs_only_packet": "h59_post_h58_reproduction_gap_decision_packet",
            "next_publication_sidecar": "p41_post_h58_publication_and_archive_sync",
            "next_low_priority_wave": "p42_post_h59_gptpro_reinterview_packet",
            "next_planning_bundle": "f33_post_h59_different_cost_structure_reopen_bundle",
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
            {
                "source": "f32",
                "certified_stop": "same_lane_reopen_not_admissible_without_new_cost_structure",
            },
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
