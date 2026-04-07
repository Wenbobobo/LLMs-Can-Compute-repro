"""Export the actual post-R60/R61 useful-kernel decision packet for H56."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H56_post_r60_r61_useful_kernel_decision_packet"
R60_SUMMARY_PATH = ROOT / "results" / "R60_origin_compiled_useful_kernel_carryover_gate" / "summary.json"
R61_SUMMARY_PATH = ROOT / "results" / "R61_origin_compiled_useful_kernel_value_gate" / "summary.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def select_outcome(r60_gate: dict[str, object], r61_gate: dict[str, object]) -> str:
    if int(r60_gate["compiler_work_leakage_break_count"]) > 0:
        return "stop_due_to_compiler_work_leakage"
    if str(r60_gate["lane_verdict"]) != "compiled_useful_kernel_carryover_supported_exactly":
        return "stop_as_compiled_boundary_toy_only"
    if str(r61_gate["lane_verdict"]) == "compiled_useful_kernel_route_retains_bounded_value":
        return "authorize_later_compiled_useful_family_packet"
    return "freeze_minimal_useful_kernel_bridge_supported_without_bounded_value"


def main() -> None:
    r60_summary = read_json(R60_SUMMARY_PATH)["summary"]["gate"]
    r61_summary = read_json(R61_SUMMARY_PATH)["summary"]["gate"]
    selected_outcome = select_outcome(r60_summary, r61_summary)

    checklist_rows = [
        {
            "item_id": "h56_reads_positive_r60_carryover_result",
            "status": "pass"
            if str(r60_summary["lane_verdict"]) == "compiled_useful_kernel_carryover_supported_exactly"
            else "blocked",
            "notes": "H56 must read the actual R60 carryover gate rather than the old planning placeholder.",
        },
        {
            "item_id": "h56_reads_r61_value_result_and_stops_scope_lift_on_negative_value",
            "status": "pass"
            if str(r61_summary["lane_verdict"]) == "compiled_useful_kernel_route_lacks_bounded_value"
            else "blocked",
            "notes": "Negative value at R61 should freeze the bridge rather than authorize broader family lift.",
        },
        {
            "item_id": "h56_preserves_h43_ceiling_and_keeps_f27_r53_r54_blocked",
            "status": "pass",
            "notes": "The closeout remains below the preserved H43 bounded useful-case ceiling.",
        },
        {
            "item_id": "h56_restores_no_active_downstream_runtime_lane",
            "status": "pass",
            "notes": "This wave closes explicitly and does not authorize an active downstream runtime lane.",
        },
    ]
    claim_packet = {
        "supports": [
            "The current compiled-boundary route carries one minimal useful-kernel pair exactly.",
            "The same route does not retain bounded value over simpler baselines once overhead is counted.",
            "The scientifically honest closeout is a narrow freeze without later family authorization.",
        ],
        "does_not_support": [
            "a broader compiled useful-family packet on this evidence",
            "automatic scope lift above bounded useful kernels",
            "arbitrary C or broad Wasm rhetoric",
        ],
        "distilled_result": {
            "active_stage": "h56_post_r60_r61_useful_kernel_decision_packet",
            "preserved_prior_docs_only_closeout": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "preserved_prior_reentry_packet": "h55_post_h54_useful_kernel_reentry_packet",
            "current_planning_bundle": "f30_post_h54_useful_kernel_bridge_bundle",
            "current_low_priority_wave": "p39_post_h54_successor_worktree_hygiene_sync",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": selected_outcome,
            "current_downstream_scientific_lane": "no_active_downstream_runtime_lane",
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
            {"source": "r60", "lane_verdict": r60_summary["lane_verdict"]},
            {"source": "r61", "lane_verdict": r61_summary["lane_verdict"]},
            {"source": "h56", "selected_outcome": selected_outcome},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
