"""Export the post-R62 origin value-boundary closeout packet for H58."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H58_post_r62_origin_value_boundary_closeout_packet"
H57_SUMMARY_PATH = ROOT / "results" / "H57_post_h56_last_discriminator_authorization_packet" / "summary.json"
R62_SUMMARY_PATH = ROOT / "results" / "R62_origin_native_useful_kernel_value_discriminator_gate" / "summary.json"


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


def select_outcome(r62_gate: dict[str, object]) -> str:
    verdict = str(r62_gate["lane_verdict"])
    if verdict == "native_useful_kernel_route_retains_bounded_value":
        return "authorize_one_later_narrow_coprocessor_packet"
    if verdict == "native_useful_kernel_discriminator_exactness_broke":
        return "stop_due_to_native_discriminator_break"
    return "stop_as_mechanism_supported_but_no_bounded_executor_value"


def main() -> None:
    h57_summary = read_json(H57_SUMMARY_PATH)["summary"]
    r62_summary = read_json(R62_SUMMARY_PATH)["summary"]["gate"]
    if h57_summary["selected_outcome"] != "authorize_one_last_native_useful_kernel_value_discriminator_gate":
        raise RuntimeError("H58 expects the landed H57 authorization outcome.")

    selected_outcome = select_outcome(r62_summary)
    checklist_rows = [
        {
            "item_id": "h58_reads_h57_authorization_and_r62_gate",
            "status": "pass",
            "notes": "H58 closes the lane only after the explicit H57 authorization and the actual R62 result.",
        },
        {
            "item_id": "h58_stops_scope_lift_on_negative_native_value",
            "status": "pass" if selected_outcome == "stop_as_mechanism_supported_but_no_bounded_executor_value" else "blocked",
            "notes": "Negative bounded-value evidence should close the mainline rather than reopening broader executor growth.",
        },
        {
            "item_id": "h58_restores_no_active_downstream_runtime_lane",
            "status": "pass",
            "notes": "This wave closes explicitly with no active downstream runtime lane.",
        },
        {
            "item_id": "h58_keeps_blocked_future_storage_blocked",
            "status": "pass",
            "notes": "F27, R53, and R54 remain blocked after the closeout.",
        },
    ]
    claim_packet = {
        "supports": [
            "H58 closes the post-H56 last-discriminator wave on the actual R62 result.",
            (
                "The honest closeout is that mechanism support survives while bounded executor value still does not."
                if selected_outcome == "stop_as_mechanism_supported_but_no_bounded_executor_value"
                else "The lane authorizes at most one later narrow coprocessor packet."
            ),
            "H58 restores a no-active-downstream-lane posture after the last discriminator.",
        ],
        "does_not_support": [
            "automatic reopening of broad compiled or language claims",
            "any inference that the negative compiled route was caused solely by compiler overhead",
            "automatic merge or promotion back into dirty root main",
        ],
        "distilled_result": {
            "active_stage": "h58_post_r62_origin_value_boundary_closeout_packet",
            "preserved_prior_docs_only_closeout": "h56_post_r60_r61_useful_kernel_decision_packet",
            "preserved_prior_authorization_packet": "h57_post_h56_last_discriminator_authorization_packet",
            "current_planning_bundle": "f31_post_h56_final_discriminating_value_boundary_bundle",
            "current_low_priority_wave": "p40_post_h56_successor_worktree_and_artifact_hygiene_sync",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "completed_value_discriminator_gate": "r62_origin_native_useful_kernel_value_discriminator_gate",
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
            {"source": "h57", "selected_outcome": h57_summary["selected_outcome"]},
            {
                "source": "r62",
                "lane_verdict": r62_summary["lane_verdict"],
                "selected_h58_outcome": r62_summary["selected_h58_outcome"],
            },
            {"source": "h58", "selected_outcome": selected_outcome},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
